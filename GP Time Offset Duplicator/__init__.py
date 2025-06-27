bl_info = {
    "name": "GP Time Offset Duplicator",
    "author": "@blastframe, @sketchysquirrelanimation",
    "version": (1, 0, 20),
    "blender": (3, 6, 0),
    "location": "3D Viewport > Sidebar > GP Time Offset Tools",
    "description": (
        "Duplicates the active Grease Pencil frame influenced by the Time Offset "
        "modifier to a new frame for editing (compatible with GP v2 & GP v3)."
    ),
    "category": "Grease Pencil",
}

import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, BoolProperty
from bpy.utils import register_class, unregister_class


# ------------------------------------------------------------------------
# Generic helpers
# ------------------------------------------------------------------------


def gp_version_props():
    """Return a dict of GP-specific identifiers for the running Blender version."""
    if bpy.app.version >= (4, 3, 0):  # GP v3
        return {
            "object_type": "GREASEPENCIL",
            "time_offset_modifier_type": "GREASE_PENCIL_TIME",
            "edit_mode": "EDIT",
            "layer_name_attr": "name",
            "frames_copy_mode": "BY_NUMBER",  # v3 copy( from_frame_number, to_frame_number )
            "select_all_op": "grease_pencil.select_all",
            "is_v3": True,
        }
    # GP v2
    return {
        "object_type": "GPENCIL",
        "time_offset_modifier_type": "GP_TIME",
        "edit_mode": "EDIT_GPENCIL",
        "layer_name_attr": "info",
        "frames_copy_mode": "BY_OBJECT",  # v2 copy( frame )
        "select_all_op": "gpencil.select_all",
        "is_v3": False,
    }


def get_or_create_frame(layer, frame_number):
    """Return the frame at frame_number on layer, or None if it doesn't exist."""
    if bpy.app.version >= (4, 3, 0):  # GP v3
        return layer.get_frame_at(frame_number)
    for fr in layer.frames:
        if fr.frame_number == frame_number:
            return fr
    return None


def get_target_layer_items(_self, context):
    """Enum items callback – list existing layers plus a 'New +' entry."""
    items = []
    obj = context.active_object
    if obj and obj.type in {"GPENCIL", "GREASEPENCIL"}:
        name_attr = gp_version_props()["layer_name_attr"]
        for lay in obj.data.layers:
            layer_name = getattr(lay, name_attr)
            items.append((layer_name, layer_name, f"Use layer “{layer_name}”"))
    if (
        "NEW_LAYER",
        "New +",
        "Create a new layer for the duplicated frame",
    ) not in items:
        items.append(
            ("NEW_LAYER", "New +", "Create a new layer for the duplicated frame")
        )
    return items


# ------------------------------------------------------------------------
# Operator
# ------------------------------------------------------------------------


class GP_OT_DuplicateTimeOffsetFrame(Operator):
    """Duplicate the drawing shown by a Time Offset modifier to a new frame."""

    bl_idname = "gp.duplicate_time_offset_frame"
    bl_label = "Duplicate Time Offset Frame"
    bl_options = {"REGISTER", "UNDO"}

    target_layer_enum: EnumProperty(
        name="Target Layer",
        items=get_target_layer_items,
        description="Destination layer for the duplicated drawing",
    )
    create_blank_keyframe: BoolProperty(
        name="Create Blank Keyframe",
        description="When using a new layer, create a blank keyframe on the source layer to hide its original drawing",
        default=True,
    )

    def execute(self, context):
        gp = gp_version_props()

        obj = context.active_object
        if not obj or obj.type != gp["object_type"]:
            self.report({"ERROR"}, "Select a Grease Pencil object first.")
            return {"CANCELLED"}

        # Locate the Time Offset modifier & the active layer
        time_mod = next(
            (m for m in obj.modifiers if m.type == gp["time_offset_modifier_type"]),
            None,
        )
        if not time_mod:
            self.report({"ERROR"}, "No Time Offset modifier found.")
            return {"CANCELLED"}

        offset_frame = time_mod.offset
        gp_data = obj.data
        src_layer = gp_data.layers.active
        if not src_layer:
            self.report({"ERROR"}, "No active Grease Pencil layer.")
            return {"CANCELLED"}

        # Pick / create destination layer
        if self.target_layer_enum == "NEW_LAYER":
            dst_layer = gp_data.layers.new(name="Hand-Drawn Frames")
        else:
            dst_layer = gp_data.layers.get(self.target_layer_enum)
            if not dst_layer:
                self.report({"ERROR"}, "Target layer not found.")
                return {"CANCELLED"}

        # Next available frame number
        new_frame_number = (
            max(
                (fr.frame_number for lay in gp_data.layers for fr in lay.frames),
                default=0,
            )
            + 1
        )

        # Source frame
        src_frame = get_or_create_frame(src_layer, offset_frame)

        original_active = gp_data.layers.active
        gp_data.layers.active = dst_layer

        try:
            if src_frame:
                if gp["frames_copy_mode"] == "BY_NUMBER":
                    new_frame = dst_layer.frames.copy(
                        from_frame_number=offset_frame,
                        to_frame_number=new_frame_number,
                    )
                else:  # GP v2 method
                    new_frame = dst_layer.frames.copy(src_frame)
                    new_frame.frame_number = new_frame_number
            else:
                new_frame = dst_layer.frames.new(new_frame_number)
        except RuntimeError as err:
            self.report(
                {"WARNING"},
                "frames.copy() failed – duplicating strokes manually.",
            )
            new_frame = dst_layer.frames.new(new_frame_number)
            if src_frame:
                if gp["is_v3"]:
                    src_draw = src_frame.drawing
                    dst_draw = new_frame.drawing
                    for s in src_draw.strokes:
                        dst_draw.add_strokes([len(s.points)])
                        dst_stroke = dst_draw.strokes[-1]
                        dst_stroke.material_index = s.material_index
                        dst_stroke.cyclic = s.cyclic
                        for i, src_pt in enumerate(s.points):
                            dst_pt = dst_stroke.points[i]
                            dst_pt.position = src_pt.position
                            dst_pt.radius = src_pt.radius
                            dst_pt.opacity = src_pt.opacity
                else:
                    for s in src_frame.strokes:
                        dst_stroke = new_frame.strokes.new()
                        dst_stroke.points.add(len(s.points))
                        for i, src_pt in enumerate(s.points):
                            dst_pt = dst_stroke.points[i]
                            dst_pt.co = src_pt.co.copy()
                            dst_pt.pressure = src_pt.pressure
                        dst_stroke.material_index = s.material_index
        finally:
            gp_data.layers.active = original_active

        # If NEW_LAYER is chosen and blank keyframe creation is enabled,
        # ensure the source layer has a blank keyframe at the offset frame.
        if self.target_layer_enum == "NEW_LAYER" and self.create_blank_keyframe:
            src_key = get_or_create_frame(src_layer, offset_frame)
            if src_key:
                if hasattr(src_key, "drawing") and src_key.drawing:
                    # Clear all strokes to make the keyframe blank.
                    src_key.drawing.strokes.clear()
            else:
                src_layer.frames.new(offset_frame)

        time_mod.offset = new_frame_number
        time_mod.keyframe_insert(data_path="offset", frame=context.scene.frame_current)
        time_mod.show_viewport = False

        context.scene.frame_current = new_frame_number
        bpy.ops.object.mode_set(mode=gp["edit_mode"])

        op_path = gp["select_all_op"].split(".")
        op = bpy.ops
        for part in op_path:
            op = getattr(op, part)
        op(action="SELECT")

        self.report(
            {"WARNING"},
            f"Time offset disabled for {context.object.name}. Please re-enable it after editing.",
        )
        return {"FINISHED"}

    def invoke(self, context, _event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, _context):
        self.layout.use_property_split = True
        self.layout.prop(self, "target_layer_enum")


def get_time_offset_modifier(obj):
    # --- Detect GP version and choose data path --------------------------------
    if bpy.app.version >= (4, 3, 0):  # GP v3 – unified modifier stack
        mods = obj.modifiers
        type_name = "GREASE_PENCIL_TIME"
    else:  # GP v2 – dedicated GP modifiers
        mods = getattr(obj, "grease_pencil_modifiers", [])
        type_name = "GP_TIME"

    # --- Find the first Time Offset modifier -----------------------------------
    time_mod = next((m for m in mods if m.type == type_name), None)
    return time_mod


# ------------------------------------------------------------------------
# UI hook
# ------------------------------------------------------------------------


def draw_timeoffset_buttons(self, context):
    if context.object and (
        context.object.type in {"GPENCIL", "GREASEPENCIL"}
        or context.space_data.mode == "GPENCIL"
    ):
        time_mod = get_time_offset_modifier(context.object)
        if time_mod is None:
            return

        row = self.layout.row(align=True)
        row.operator(
            GP_OT_DuplicateTimeOffsetFrame.bl_idname,
            text="",
            icon="MOD_TIME",
        )
        row.prop(
            time_mod,
            "show_viewport",
            text="",
            icon=(
                "RESTRICT_VIEW_ON" if time_mod.show_viewport else "RESTRICT_VIEW_OFF"
            ),
        )


# ------------------------------------------------------------------------
# Registration
# ------------------------------------------------------------------------


def register():
    register_class(GP_OT_DuplicateTimeOffsetFrame)
    bpy.types.DOPESHEET_HT_header.append(draw_timeoffset_buttons)


def unregister():
    unregister_class(GP_OT_DuplicateTimeOffsetFrame)
    bpy.types.DOPESHEET_HT_header.remove(draw_timeoffset_buttons)


if __name__ == "__main__":
    register()
