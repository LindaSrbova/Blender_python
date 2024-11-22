import bpy
import math
from mathutils import Vector
import random


bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def set_material(obj, color, metallic=0.0, roughness=0.1, emission_strength=0.0):
    # Ensure the color is in RGBA format
    if len(color) == 3:
        color = color + (1,)  # Add the alpha value if it's not present
    
    mat = bpy.data.materials.new(name="Material")
    mat.use_nodes = True
    principled_bsdf = mat.node_tree.nodes["Principled BSDF"]
    
    # Set the base color (RGBA format)
    principled_bsdf.inputs["Base Color"].default_value = color
    
    # Set other material properties
    principled_bsdf.inputs["Metallic"].default_value = metallic
    principled_bsdf.inputs["Roughness"].default_value = roughness
    
    # Create emission if required
    emission_node = mat.node_tree.nodes.get("Emission")
    
    if emission_node is None:
        emission_node = mat.node_tree.nodes.new("ShaderNodeEmission")
        emission_node.inputs["Strength"].default_value = emission_strength
        material_output = mat.node_tree.nodes["Material Output"]
        mat.node_tree.links.new(emission_node.outputs["Emission"], material_output.inputs["Surface"])
    
    else:
        emission_node.inputs["Strength"].default_value = emission_strength

    obj.data.materials.append(mat)

def create_axis_line(start, end, radius=0.1, color=(1, 0, 0)):
    # Calculate the direction vector from the origin to the end point
    direction = Vector(end) - Vector(start)  # The direction vector
    
    # Calculate the length of the vector (distance from origin to end point)
    depth = direction.length  # Depth is the distance from start to end
    
    # Normalize the direction vector (for orientation)
    direction_normalized = direction.normalized()  # Normalize the direction vector
    
    halfway = ( Vector(end)) / 2
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=halfway)
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
    
def create_text_at_position(position, text, rotation,color):
    bpy.ops.object.text_add(location=position)
    text_object = bpy.context.active_object
    
    text_object.data.body = text
    text_object.scale = (1,1,1)
    mat = bpy.data.materials.new(name="AxisMaterial")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color + (1,)  # RGBA
    text_object.data.materials.append(mat)

    text_object.rotation_euler = rotation
    
    return text_object

def create_3d_axes_with_labels():
    create_axis_line(start=(0, 0, 0), end=(10, 0, 0), color=(0, 0, 0))  # Red X-axis
    create_text_at_position(position=(3, -1, 0), text="morphology", rotation=(1,0,0),color=(0, 0, 0))  # Text at the end of X-axis
    
    #create_axis_line(start=(0, 0, 0), end=(0, 10, 0), color=(0, 1, 0))  # Green Y-axis
    create_axis_line(start=(20, 0, 0), end=(20, 20, 0), color= (0,0,0))  # Green Y-axis
    create_text_at_position(position=(11, 5, 0), text="Incubation time", rotation=(1, 0,1),color=(0.235, 0.157, 0.078))  # Text at the end of Y-axis
    
    create_axis_line(start=(0, 0, 0), end=(0, 0, 10), color=(0, 0, 0))  # Blue Z-axis
    create_text_at_position(position=(0, -1, 7), text="stiffness", rotation=(1, 1, 1),color=(159, 0, 0))  # Text at the end of Z-axis

create_3d_axes_with_labels()

def create_cell(location, min_radius=0.05, max_radius=0.2, color=(1.0, 0.647, 0.0)):  # default color orange
    radius = random.uniform(min_radius, max_radius)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    cell = bpy.context.active_object
    
    deform_x = random.uniform(0.8, 1.2)  # Random scale factor between 0.8 and 1.2
    deform_y = random.uniform(0.8, 1.2)  # Random scale factor between 0.8 and 1.2
    deform_z = random.uniform(0.8, 1.2)  # Random scale factor between 0.8 and 1.2
    
    # Apply random deformation
    cell.scale = (deform_x, deform_y, deform_z)
    
    # Set the color of the cell (optional, if using a material)
    set_material(cell, color + (1,))  # Use RGBA
    
    return cell

def create_spheroid_soft(spheroid_center, scaling, min_cell_radius, max_cell_radius, num_cells):
    cells = []
    for _ in range(num_cells):
        x = random.uniform(spheroid_center[0], (spheroid_center[0]+1)*scaling)
        y = random.uniform(spheroid_center[1], (spheroid_center[1]+1)*scaling)
        z = random.uniform(spheroid_center[2], (spheroid_center[2]+1)*scaling)
        location = Vector((x, y, z))
        cell = create_cell(location, min_radius=min_cell_radius, max_radius=max_cell_radius, color=(1.0, 0.647, 0.0))  # Orange cells
        cells.append(cell)

def create_spheroid_stiff(spheroid_center, scaling, min_cell_radius, max_cell_radius, num_cells):
    cells = []
    for _ in range(num_cells):
        x = random.uniform(spheroid_center[0], (spheroid_center[0]+0.5)*scaling)
        y = random.uniform(spheroid_center[1], (spheroid_center[1]+0.5)*scaling)
        z = random.uniform(spheroid_center[2], (spheroid_center[2]+0.5)*scaling)
        location = Vector((x, y, z))
        cell = create_cell(location, min_radius=min_cell_radius, max_radius=max_cell_radius, color=(0.6, 0.6, 0.6))  # Grey cells
        cells.append(cell)
        
def create_xy_plane(width, height, location):
    bpy.ops.mesh.primitive_plane_add(size=1, location=location)
    plane = bpy.context.active_object
    plane.scale = (width / 2, height / 2, 1)
    
def create_zy_plane(width, height, location):
    # Add a plane to the scene with default size
    bpy.ops.mesh.primitive_plane_add(size=1, location=location)
    plane = bpy.context.active_object
    
    # Scale the plane to the desired width and height
    plane.scale = (width / 2, height / 2, 1)  # Divide by 2 since default size is 1
    
    # Rotate the plane 90 degrees around the X-axis to align with the ZX plane
    plane.rotation_euler = (0, math.radians(90), 0)
    set_material(plane, (0.6, 8, 0.6), metallic=0.1, roughness=0.2, emission_strength=5.0)

def create_zx_plane(size, location):
    # Add a plane to the scene at the specified location
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)
    plane = bpy.context.active_object
    # Rotate the plane 90 degrees around the X axis to align it with the ZY plane
    plane.rotation_euler = (math.radians(90), math.radians(90), 0)
    set_material(plane, (0.6, 0.6, 0.6), metallic=0.1, roughness=0.2, emission_strength=5.0)

create_xy_plane(20,40, (5, 10, 0))
create_zy_plane(20,40, (0, 10, 5))
create_zx_plane(10, (5, 20, 5))
create_text_at_position(position=(0.5, 2, 3), text="soft", rotation=(1, 0, 1),color=(159, 0, 0))  # Text at the end of Y-axis
create_text_at_position(position=(0.5, 3, 7), text="stiff", rotation=(1, 0, 1),color=(159, 0, 0))  # Text at the end of Y-axis

        
# Parameters for the spheroid
spheroid_center = (3,0,5)
spheroid_radius = 2  # Radius of the spheroid (larger)
min_cell_radius = 0.2    # Minimum radius of each cell
max_cell_radius = 0.4     # Maximum radius of each cell
num_cells = 50         # Number of cells in the spheroid

create_spheroid_soft((3.5, 3, 2), 0.9, 0.2, 0.3, 15)
create_spheroid_soft((4.0, 9, 2), 1.01, 0.2, 0.3, 35)
create_spheroid_soft((4.5, 15, 2), 1.02, 0.2, 0.3, 50)

create_spheroid_stiff((7.0, 3, 6), 1, 0.2, 0.3, 7)
create_spheroid_stiff((7.2, 9, 6), 1, 0.2, 0.3, 25)
create_spheroid_stiff((7.5 ,15, 6), 1, 0.2, 0.3, 30)

create_text_at_position(position=(8, 3, 0.2), text="Day 1", rotation=(1, 0, 1),color= (0.396, 0.263, 0.129))  # Text at the end of Y-axis
create_text_at_position(position=(8.5, 9,0.2), text="Day 3", rotation=(1, 0, 1),color= (0.396, 0.263, 0.129))  # Text at the end of Y-axis
create_text_at_position(position=(9, 15, 0.2), text="Day 6", rotation=(1, 0, 1),color= (0.396, 0.263, 0.129))  # Text at the end of Y-axis


def create_lights():
    # Remove any existing lights first
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()

    # Add a point light
    bpy.ops.object.light_add(type='POINT', location=(10, -10, 10))  # Point light at an angle
    point_light = bpy.context.active_object
    point_light.data.energy = 500  # Increase the intensity for stronger light

    # Add a key light (Sun) for softer shadows
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))  # Sun light above the scene
    sun_light = bpy.context.active_object
    sun_light.data.energy = 3  # Moderate sun intensity

    # Add some ambient lighting (optional)
    bpy.ops.object.light_add(type='AREA', location=(10, 10, 10))  # Area light to fill the scene
    area_light = bpy.context.active_object
    area_light.data.energy = 200  # Adjust intensity for a softer light fill

create_lights()

def create_camera():
    # Check if a camera already exists, if not, create a new one
    if not bpy.data.objects.get('Camera'):
        bpy.ops.object.camera_add(location=(15, -15, 15))
        camera = bpy.context.active_object
        camera.rotation_euler = (math.radians(60), 0, math.radians(45))
        
        # Set the camera to always point at the center of the scene (or target object)
        target = bpy.data.objects.new("Target", bpy.data.meshes.new('TargetMesh'))  # Dummy target object
        target.location = (0, 0, 0)  # You can place it wherever you want to focus the camera on
        
        bpy.context.collection.objects.link(target)  # Link the target object to the scene
        
        # Add a Track To constraint to the camera to always face the target
        constraint = camera.constraints.new('TRACK_TO')
        constraint.target = target
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'
        bpy.context.scene.camera = camera  # Set the newly created camera as the active camera

create_camera()

# Set the render resolution (optional)
scene = bpy.context.scene
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.image_settings.file_format = 'PNG'

