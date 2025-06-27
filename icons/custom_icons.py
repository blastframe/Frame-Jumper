import os

import bpy
import bpy.utils.previews

path = os.path.join(os.path.dirname(__file__), 'images')
custom_icons = None


def get_icon_value(icon_name: str) -> int:
    icon_items = bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.items()
    icon_dict = {tup[1].identifier : tup[1].value for tup in icon_items}

    return icon_dict[icon_name]

def register_custom_icons():
    global custom_icons
    custom_icons = bpy.utils.previews.new()
    for idx, ic in enumerate(os.listdir(path)):
        if not ic.startswith("."):
            custom_icons.load(ic, os.path.join(path, ic), 'IMAGE')

def unregister_custom_icons():
    global custom_icons
    bpy.utils.previews.remove(custom_icons)
    custom_icons.clear()

def get_icon(string):
    global custom_icons
    if not custom_icons:
        return get_icon_value("QUESTION")
    else:
        return custom_icons[string+".png"].icon_id