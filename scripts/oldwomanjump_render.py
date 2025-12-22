
import bpy
import math
import os
import sys

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for block in bpy.data.meshes: bpy.data.meshes.remove(block)
    for block in bpy.data.materials: bpy.data.materials.remove(block)
    for block in bpy.data.textures: bpy.data.textures.remove(block)
    for block in bpy.data.images: bpy.data.images.remove(block)

def create_terrain(dem_path, hillshade_path):
    print(f"Creating terrain from {dem_path}...")
    
    # Create plane
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
    terrain = bpy.context.active_object
    terrain.name = "OldWomanJump_Terrain"
    
    # High-density subdivision for LiDAR detail
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=150)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Add Displacement
    displace_mod = terrain.modifiers.new(name="LiDAR_Displace", type='DISPLACE')
    
    # Load DEM as Texture
    tex = bpy.data.textures.new("DEM_Tex", type='IMAGE')
    try:
        img_dem = bpy.data.images.load(dem_path)
        tex.image = img_dem
        displace_mod.texture = tex
        displace_mod.strength = 1.8  # Vertical exaggeration for cinematic effect
        displace_mod.texture_coords = 'UV'
    except Exception as e:
        print(f"Failed to load DEM: {e}")

    # Add Material with Hillshade
    mat = bpy.data.materials.new(name="Terrain_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    
    try:
        tex_node = nodes.new('ShaderNodeTexImage')
        img_shade = bpy.data.images.load(hillshade_path)
        tex_node.image = img_shade
        links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
    except Exception as e:
        print(f"Failed to load Hillshade: {e}")
        
    terrain.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    
    return terrain

def setup_lighting_and_cam(target):
    # Lighting
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
    sun = bpy.context.active_object
    sun.data.energy = 4.0
    
    # Orbiting Camera
    bpy.ops.object.camera_add(location=(25, -25, 15))
    cam = bpy.context.active_object
    bpy.context.scene.camera = cam
    
    # Track Constraint
    track = cam.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    return cam

def run_render(output_path):
    print(f"Rendering to {output_path}...")
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = output_path
    
    # Use EEVEE_NEXT for Blender 4.3
    bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
    
    bpy.ops.render.render(write_still=True)
    print("Render complete.")

def main():
    # Paths from the user's local environment
    DEM = r"C:\Users\chris\PeterFidler\oldwomanjump\output\primeau_dem.tif"
    SHADE = r"C:\Users\chris\PeterFidler\oldwomanjump\output\primeau_hillshade.tif"
    OUT = r"c:\Users\chris\antigravity-workspace-template\artifacts\oldwomanjump_demo.png"
    
    # Create dir if not exists
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    
    clear_scene()
    terrain = create_terrain(DEM, SHADE)
    setup_lighting_and_cam(terrain)
    run_render(OUT)

if __name__ == "__main__":
    main()
