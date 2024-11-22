import bpy
import math
from mathutils import Vector
import random

def create_text_at_position(position, text, rotation):
    bpy.ops.object.text_add(location=position)
    text_object = bpy.context.active_object
    
    text_object.data.body = text
    text_object.scale = (1,1,1)
    # Set the rotation (you can adjust if you want the text to face a specific direction)
    text_object.rotation_euler = rotation
    
    return text_object