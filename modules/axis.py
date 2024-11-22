import bpy
import math
from mathutils import Vector
import random

def create_axis_line(start, end, radius=0.1, color=(1, 0, 0)):
    # Calculate the direction vector from the origin to the end point
    direction = Vector(end) - Vector(start)  # The direction vector
    
    # Calculate the length of the vector (distance from origin to end point)
    depth = direction.length  # Depth is the distance from start to end
    
    # Normalize the direction vector (for orientation)
    direction_normalized = direction.normalized()  # Normalize the direction vector
    
    halfway = ( Vector(end)) / 2
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=halfway)
    
    # The active object is now the cylinder
    axis = bpy.context.active_object
    
    # Calculate the rotation needed to align the cylinder along the direction vector
    up = Vector((0, 0, 1))  # The "up" direction (Z-axis in world coordinates)
    axis_of_rotation = direction_normalized.cross(up)
    
    # Apply the rotation to the cylinder
    axis.rotation_euler = axis_of_rotation.to_track_quat('X', 'Y').to_euler()
    
    # Set the color of the cylinder (optional, if using a material)
    mat = bpy.data.materials.new(name="AxisMaterial")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color + (1,)  # RGBA
    axis.data.materials.append(mat)