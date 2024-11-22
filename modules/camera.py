import bpy
import math
from mathutils import Vector
import random

def create_camera():
    # Check if a camera already exists, if not, create a new one
    if not bpy.data.objects.get('Camera'):
        bpy.ops.object.camera_add(location=(15, -15, 15))
        camera = bpy.context.active_object
        camera.rotation_euler = (math.radians(60), 0, math.radians(45))
        bpy.context.scene.camera = camera  # Set the newly created camera as the active camera
