#Function to create a single cell (small sphere) with random size and deformation
import bpy
import math
from mathutils import Vector
import random

def create_cell(location, min_radius=0.05, max_radius=0.2, color=(0, 1, 0)):
    radius = random.uniform(min_radius, max_radius)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    cell = bpy.context.active_object
    deform_x = random.uniform(0.8, 1.2)  # Random scale factor between 0.8 and 1.2
    deform_y = random.uniform(0.8, 1.2)  # Random scale factor between 0.8 and 1.2
    deform_z = random.uniform(0.8, 1.2)  # Random scale factor between 0.8 and 1.2
    
    # Apply the random deformation
    cell.scale = (deform_x, deform_y, deform_z)

    # Set the color of the cell (optional, if using a material)
    mat = bpy.data.materials.new(name="CellMaterial")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color + (1,)  # RGBA
    cell.data.materials.append(mat)
    
    return cell
def create_spheroid_soft(spheroid_center, scaling, min_cell_radius, max_cell_radius, num_cells):
    
    cells = []  # List to store the cells

    for _ in range(num_cells):
        # Random position within a spherical volume
        x = random.uniform(spheroid_center[0], (spheroid_center[0]+1)*scaling)
        y = random.uniform(spheroid_center[1], (spheroid_center[1]+1)*scaling)
        z = random.uniform(spheroid_center[2], (spheroid_center[2]+1)*scaling)
        location = Vector((x, y, z))
        
        cell = create_cell(location, min_radius=min_cell_radius, max_radius = max_cell_radius)
        cells.append(cell)

def create_spheroid_stiff(spheroid_center, scaling, min_cell_radius, max_cell_radius, num_cells):
    
    cells = []  # List to store the cells

    for _ in range(num_cells):
        # Random position within a spherical volume
        x = random.uniform(spheroid_center[0], (spheroid_center[0]+0.5)*scaling)
        y = random.uniform(spheroid_center[1], (spheroid_center[1]+0.5)*scaling)
        z = random.uniform(spheroid_center[2], (spheroid_center[2]+0.5)*scaling)
        location = Vector((x, y, z))
        
        cell = create_cell(location, min_radius=min_cell_radius, max_radius = max_cell_radius)
        cells.append(cell)