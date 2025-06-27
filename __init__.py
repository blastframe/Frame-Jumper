bl_info = {
    "name": "Frame Jumper",
    "author": "@blastframe, @sketchysquirrelanimation",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "Dopesheet Header",
    "description": (
        "Duplicates the active Grease Pencil frame or creates a blank keyframe - based on the frame referenced by the Time Offset modifier - to produce a new, editable frame."
    ),
    "doc_url": "https://blastframe.com/docs/graphkit/",
    "tracker_url": "https://blastframe.com/contact/",
    "category": "Grease Pencil",
}

import bpy
from bpy.types import Operator, AddonPreferences, DOPESHEET_HT_header
from bpy.props import EnumProperty, BoolProperty
from bpy.utils import register_class, unregister_class
from .icons.custom_icons import get_icon

# ------------------------------------------------------------------------
# Generic helpers
# ------------------------------------------------------------------------


def gp_version_props():
    """Return a dict of GP-specific identifiers for the running Blender version."""
    if bpy.app.version >= (4, 3, 0):  # GP v3
        return {
            "object_type": "GREASEPENCIL",
            "time_offset_modifier_type": "GREASE_PENCIL_TIME",
            "draw_mode": "PAINT_GREASE_PENCIL",
            "edit_mode": "EDIT",
            "sculpt_mode": "SCULPT_GREASE_PENCIL",
            "vertex_mode": "VERTEX_GREASE_PENCIL",
            "weight_mode": "WEIGHT_GREASE_PENCIL",
            "layer_name_attr": "name",
            "frames_copy_mode": "BY_NUMBER",  # v3 copy( from_frame_number, to_frame_number )
            "select_all_op": "grease_pencil.select_all",
            "is_v3": True,
        }
    # GP v2
    return {
        "object_type": "GPENCIL",
        "time_offset_modifier_type": "GP_TIME",
        "draw_mode": "PAINT_GPENCIL",
        "edit_mode": "EDIT_GPENCIL",
        "sculpt_mode": "SCULPT_GPENCIL",
        "vertex_mode": "VERTEX_GPENCIL",
        "weight_mode": "WEIGHT_GPENCIL",
        "layer_name_attr": "info",
        "frames_copy_mode": "BY_OBJECT",  # v2 copy( frame )
        "select_all_op": "gpencil.select_all",
        "is_v3": False,
    }


def get_frame(layer, frame_number):
    """Gets an existing frame or creates a new one, handling GPv2 and GPv3 differences."""
    if bpy.app.version >= (4, 3, 0):
        new_frame = layer.get_frame_at(frame_number)
        return new_frame
    else:
        for f in layer.frames:
            if f.frame_number == frame_number:
                return f


def get_target_layer_items(_self, context):
    """Enum items callback - list existing layers plus a 'New +' entry."""
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


def refresh():
    """Updates/redraws the main animation-related UI areas."""
    for area in bpy.context.screen.areas:
        if area.type in {
            "VIEW_3D",
            "DOPESHEET_EDITOR",
            "GRAPH_EDITOR",
            "NLA_EDITOR",
            "OUTLINER",
            "PROPERTIES",
        }:
            for region in area.regions:
                if (area.type == "VIEW_3D" and region.type == "UI") or (
                    area.type != "VIEW_3D" and region.type in {"WINDOW", "CHANNELS"}
                ):
                    region.tag_redraw()


# --------------------------------------------------------------------
#  Safe, one-liner helper to read the add-on preference
# --------------------------------------------------------------------
def get_debug_mode() -> bool:
    """Return the 'debug_mode' flag from this add-on’s preferences."""

    # ⓐ  the module name *is* the add-on ID when it sits in __init__.py
    addon_id = "framejumper"

    prefs = None
    for a in bpy.context.preferences.addons:
        if addon_id in a.module:
            prefs = a
            break

    # ⓒ  prefs is None if the add-on is disabled or wasn’t found
    debug = getattr(prefs, "preferences", None)
    debug = getattr(debug, "debug_mode", False)

    if debug:
        print("[GP-TOD]  Debug mode is ON")

    return debug


# ------------------------------------------------------------------------
# Operator
# ------------------------------------------------------------------------


class BLASTFRAME_OT_duplicate_time_offset_frame(Operator):
    """Duplicate the drawing shown by a Time Offset modifier to a new frame."""

    bl_idname = "gp.duplicate_time_offset_frame"
    bl_label = "Duplicate Time Offset Frame"
    bl_options = {"REGISTER", "UNDO"}

    target_layer_enum: EnumProperty(
        name="Target Layer",
        items=get_target_layer_items,
        description="Destination layer for the new drawing",
    )
    create_blank_keyframe: BoolProperty(
        name="Create Blank Keyframe",
        description="Create a new blank keyframe",
        default=True,
    )
    create_blank_keyframe_on_source: BoolProperty(
        name="Create Blank Keyframe on Source Layer",
        description="When using a new layer, create a blank keyframe on the source layer to hide its original drawing",
        default=True,
    )

    def execute(self, context):
        gp = gp_version_props()

        # Retrieve addon preferences:
        debug_mode = get_debug_mode()

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
        src_frame = get_frame(src_layer, offset_frame)

        original_active = gp_data.layers.active
        gp_data.layers.active = dst_layer

        if not self.create_blank_keyframe:
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
                    "frames.copy() failed - duplicating strokes manually.",
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

        # If the user chose to create a new layer ("NEW_LAYER") and requested that a blank keyframe
        # be created on the original source layer (to hide its original drawing), then we process that here.
        if (
            self.target_layer_enum == "NEW_LAYER"
            and self.create_blank_keyframe_on_source
        ):
            # Try to retrieve an existing keyframe on the source layer at the modifier's offset frame.
            src_key = get_frame(src_layer, offset_frame)
            if src_key:
                if hasattr(src_key, "drawing") and src_key.drawing:
                    # If the keyframe exists and has drawing data, clear its strokes to create a blank keyframe.
                    src_key.drawing.strokes.clear()
            else:
                # If no keyframe exists at the offset frame, create one.
                src_layer.frames.new(offset_frame)

        # Update the Time Offset modifier to point to the new frame number.
        time_mod.offset = new_frame_number
        # Insert a keyframe for the new offset value at the current scene frame.
        time_mod.keyframe_insert(data_path="offset", frame=context.scene.frame_current)
        # Disable the modifier's viewport display so that the duplicated frame appears without interference.
        time_mod.show_viewport = False

        # Set the current scene frame to the new frame number so the user sees the newly duplicated frame.
        context.scene.frame_current = new_frame_number

        if self.create_blank_keyframe:
            # Switch the object to the appropriate edit mode (as defined by the GP version properties).
            bpy.ops.object.mode_set(mode=gp["draw_mode"])
            # Ensure the destination layer has a blank keyframe at the new frame.
            new_frame = src_layer.frames.new(new_frame_number)
            name_attr = gp["layer_name_attr"]
            layer_name = getattr(src_layer, name_attr)
            if debug_mode:
                print(
                    f"DEBUG: Created new frame {new_frame_number} on layer '{layer_name}'"
                )
        else:
            # Switch the object to the appropriate edit mode (as defined by the GP version properties).
            bpy.ops.object.mode_set(mode=gp["edit_mode"])
            # Dynamically retrieve and execute the "select all" operator based on the GP version properties.
            op_path = gp["select_all_op"].split(".")
            op = bpy.ops
            for part in op_path:
                op = getattr(op, part)
            op(action="SELECT")

        # Refresh the UI to ensure all changes are immediately visible.
        refresh()

        # Report a warning to the user reminding them that the Time Offset modifier
        # has been disabled and must be re-enabled after completing their edits.
        self.report(
            {"WARNING"},
            f"Time Offset Modifier disabled for {context.object.name}. Please re-enable it after editing.",
        )

        return {"FINISHED"}

    def invoke(self, context, _event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, _context):
        self.layout.use_property_split = True
        self.layout.prop(self, "target_layer_enum")
        self.layout.prop(self, "create_blank_keyframe")
        if self.target_layer_enum == "NEW_LAYER":
            self.layout.prop(
                self,
                "create_blank_keyframe_on_source",
                text="Create Blank Keyframe on Source Layer",
            )


def get_time_offset_modifier(obj):
    # --- Detect GP version and choose data path --------------------------------
    if bpy.app.version >= (4, 3, 0):  # GP v3 - unified modifier stack
        mods = obj.modifiers
        type_name = "GREASE_PENCIL_TIME"
    else:  # GP v2 - dedicated GP modifiers
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
            BLASTFRAME_OT_duplicate_time_offset_frame.bl_idname,
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


class BLASTFRAME_OT_duplicate_time_offset_frame_preferences(AddonPreferences):
    bl_idname = __name__  # Match your add-on id

    debug_mode: BoolProperty(
        name="Debug Mode",
        description="Enable additional debug output for Frame Jumper",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "debug_mode")
        row = layout.row(align=True)
        row.scale_y = 1.3

        row.operator(
            "wm.url_open",
            text="Blastframe",
            icon_value=get_icon("Blastframe_Logo_White"),
        ).url = "https://blastframe.com"
        row.operator(
            "wm.url_open", text="YouTube", icon_value=get_icon("YouTube")
        ).url = "https://www.youtube.com/@blastframe"


# ------------------------------------------------------------------------
# Registration
# ------------------------------------------------------------------------

classes = (
    BLASTFRAME_OT_duplicate_time_offset_frame,
    BLASTFRAME_OT_duplicate_time_offset_frame_preferences,
)


def register():
    from .icons.custom_icons import register_custom_icons

    register_custom_icons()
    for cls in classes:
        register_class(cls)
    DOPESHEET_HT_header.append(draw_timeoffset_buttons)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
    DOPESHEET_HT_header.remove(draw_timeoffset_buttons)

    from .icons.custom_icons import unregister_custom_icons

    unregister_custom_icons()


if __name__ == "__main__":
    register()
