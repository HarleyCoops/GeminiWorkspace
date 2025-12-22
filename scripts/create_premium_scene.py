
import bpy
import math
import os

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    # Deep clean data blocks
    for block in [bpy.data.meshes, bpy.data.materials, bpy.data.textures, bpy.data.images, bpy.data.lights, bpy.data.cameras]:
        for item in block:
            block.remove(item, do_unlink=True)

def setup_environment():
    # Set Cycles render engine for high quality setup
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    
    # World lighting (Sky Texture)
    bpy.context.scene.world.use_nodes = True
    nodes = bpy.context.scene.world.node_tree.nodes
    links = bpy.context.scene.world.node_tree.links
    nodes.clear()
    
    node_out = nodes.new('ShaderNodeOutputWorld')
    node_bg = nodes.new('ShaderNodeBackground')
    node_sky = nodes.new('ShaderNodeTexSky')
    node_sky.sky_type = 'NISHITA'
    node_sky.sun_elevation = math.radians(25)
    
    links.new(node_sky.outputs['Color'], node_bg.inputs['Color'])
    links.new(node_bg.outputs['Background'], node_out.inputs['Surface'])

def create_high_res_terrain(dem_path, shade_path):
    print(f"Building high-res terrain from {dem_path}")
    
    # Create high-density plane
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
    terrain = bpy.context.active_object
    terrain.name = "OldWomanJump_HiRes"
    
    # Subdivision for LiDAR fidelity
    # Level 1: Edit mode subdivision
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=100)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Level 2: Subsurf modifier for even more detail (viewports and render)
    subsurf = terrain.modifiers.new(name="SubDiv", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 2
    subsurf.render_levels = 3
    
    # Displacement
    displace = terrain.modifiers.new(name="LiDAR_Displace", type='DISPLACE')
    tex = bpy.data.textures.new("DEM_Height", type='IMAGE')
    img_dem = bpy.data.images.load(dem_path)
    tex.image = img_dem
    # LiDAR textures usually need RAW or Linear color space for height
    img_dem.colorspace_settings.name = 'Non-Color'
    
    displace.texture = tex
    displace.strength = 1.2
    displace.texture_coords = 'UV'
    
    # Material
    mat = bpy.data.materials.new(name="Terrain_Premium")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    node_out = nodes.new('ShaderNodeOutputMaterial')
    node_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    node_tex = nodes.new('ShaderNodeTexImage')
    node_bump = nodes.new('ShaderNodeBump')
    
    try:
        img_shade = bpy.data.images.load(shade_path)
        node_tex.image = img_shade
        
        # Base Color
        links.new(node_tex.outputs['Color'], node_bsdf.inputs['Base Color'])
        
        # Bump (adds micro-detail)
        node_bump.inputs['Strength'].default_value = 0.5
        links.new(node_tex.outputs['Color'], node_bump.inputs['Height'])
        links.new(node_bump.outputs['Normal'], node_bsdf.inputs['Normal'])
        
    except Exception as e:
        print(f"Texture error: {e}")
        
    links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])
    terrain.data.materials.append(mat)
    
    bpy.ops.object.shade_smooth()
    return terrain

def setup_scene_view_and_save(terrain, save_path):
    # Camera
    bpy.ops.object.camera_add(location=(20, -25, 12))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(65), 0, math.radians(40))
    bpy.context.scene.camera = cam
    
    # UI Setup: Set viewport for the user
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL' # Material Preview mode
                    space.region_3d.view_perspective = 'PERSP'
                    
    # Save the file
    print(f"Saving premium scene to {save_path}")
    bpy.ops.wm.save_as_mainfile(filepath=save_path)

def main():
    DEM = r"C:\Users\chris\PeterFidler\oldwomanjump\output\primeau_dem.tif"
    SHADE = r"C:\Users\chris\PeterFidler\oldwomanjump\output\primeau_hillshade.tif"
    BLEND_PATH = r"C:\Users\chris\PeterFidler\oldwomanjump\OldWomansJump_HiRes.blend"
    
    clear_scene()
    setup_environment()
    terrain = create_high_res_terrain(DEM, SHADE)
    setup_scene_view_and_save(terrain, BLEND_PATH)

if __name__ == "__main__":
    main()
