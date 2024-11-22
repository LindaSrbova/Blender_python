import bpy
import math
from mathutils import Vector
import random

def create_zy_plane(size, location):
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)

    

def create_zy_plane(size, location):
    # Add a plane to the scene at the specified location
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)
    
    # Get the active object (the newly created plane)
    plane = bpy.context.active_object
    
    # Rotate the plane 90 degrees around the X axis to align it with the ZY plane
    plane.rotation_euler = (math.radians(90), 0, 0)
