import bpy
import os

## Earth of radius 1

def makeTerrainOcean():


    #creating UV Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))

    #referencing object as earth
    earth=bpy.context.active_object

    # bpy.ops.transform.resize(value=(10, 10, 10), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


    #Creating modifier
    earth.modifiers.new("My Modifier",'SUBSURF')
    bpy.ops.object.shade_smooth()


    #adding base material
    earth_mat = bpy.data.materials.new(name = "Earth_base")
    earth.data.materials.append(earth_mat)

    #accessing nodes in material tab
    earth_mat.use_nodes = True
    earth_nodes = earth_mat.node_tree.nodes

    #removing node
    principled_bsdf = earth_nodes['Principled BSDF']
    earth_nodes.remove(principled_bsdf)

    #accessing material output node
    material_output = earth_nodes.get("Material Output")

    #adding new nodes

    #texture coordinate
    tex_coord = earth_nodes.new(type = 'ShaderNodeTexCoord')

    #ocean mask
    ocean_mask_tex = earth_nodes.new(type = 'ShaderNodeTexImage')

    #invert
    invert_1 = earth_nodes.new(type = 'ShaderNodeInvert')
    invert_2 = earth_nodes.new(type = 'ShaderNodeInvert')

    #image texture for base earth texture
    base_tex = earth_nodes.new(type = 'ShaderNodeTexImage')

    #Glossy node
    glossy = earth_nodes.new(type = 'ShaderNodeBsdfGlossy')

    #mix shader
    mix_shader_1 = earth_nodes.new(type = 'ShaderNodeMixShader')
    mix_shader_2 = earth_nodes.new(type = 'ShaderNodeMixShader')
    mix_shader_3 = earth_nodes.new(type = 'ShaderNodeMixShader')


    #Fresnel node
    fresnel = earth_nodes.new(type = 'ShaderNodeFresnel')

    #camera data node
    cam_data = earth_nodes.new(type="ShaderNodeCameraData")

    #math -> subtract node
    subtract = earth_nodes.new(type = 'ShaderNodeMath')
    subtract.operation = 'SUBTRACT'

    #math -> multiply node
    multiply = earth_nodes.new(type = 'ShaderNodeMath')
    multiply.operation = 'MULTIPLY'

    #combine hsv node
    combine_hsv = earth_nodes.new(type= 'ShaderNodeCombineHSV')

    #refraction bsdf
    refraction = earth_nodes.new(type= 'ShaderNodeBsdfRefraction')

    #diffuse BSDF
    diff = earth_nodes.new(type = 'ShaderNodeBsdfDiffuse')

    #noise texture node
    noise_tex = earth_nodes.new(type= 'ShaderNodeTexNoise')

    #voronoi texture node
    voronoi_tex = earth_nodes.new(type= 'ShaderNodeTexVoronoi')

    #mix rgb
    mix_rgb = earth_nodes.new(type = 'ShaderNodeMixRGB')

    #bump
    bump_tex = earth_nodes.new(type = 'ShaderNodeTexImage')
    bump = earth_nodes.new(type = 'ShaderNodeBump')


    #adding image to image texture nodes

    #Albedo image
    earth_img = bpy.data.images.load(os.path.join(".", os.path.normpath(r"../textures/albedo.jpg")))
    base_tex.image = earth_img
    #bump texture
    bump_img = bpy.data.images.load(os.path.join(".", os.path.normpath(r"../textures/bump.jpg")))
    bump_tex.image = bump_img
    #ocean mask image
    ocean_mask_img = bpy.data.images.load(os.path.join(".", os.path.normpath(r"../textures/ocean_mask.png")))
    ocean_mask_tex.image = ocean_mask_img

    #changing value of img texture nodes
    base_tex.projection = 'SPHERE'
    base_tex.extension = 'EXTEND'
    base_tex.interpolation = 'Cubic'
    ocean_mask_tex.projection = 'SPHERE'
    ocean_mask_tex.extension = 'EXTEND'
    ocean_mask_tex.interpolation = 'Cubic'
    bump_tex.projection = 'SPHERE'
    bump_tex.extension = 'EXTEND'
    bump_tex.interpolation = 'Linear'
    bump.inputs[0].default_value = 3
    bump.inputs[1].default_value = 2
    #changing color space to non color
    bpy.data.images["ocean_mask.png"].colorspace_settings.name = 'Non-Color'
    bpy.data.images["albedo.jpg"].colorspace_settings.name = 'Non-Color'
    bpy.data.images["bump.jpg"].colorspace_settings.name = 'Non-Color'

    #changing values of glossy node parameters
    glossy.inputs[1].default_value = 0.48
    #changing values of fresnel node parameters
    fresnel.inputs[0].default_value = 1.33
    #invert node fac value
    invert_1.inputs[0].default_value = 1
    invert_2.inputs[0].default_value = 1
    #changing value of math nodes
    subtract.inputs[1].default_value = 0.3
    multiply.inputs[0].default_value = 0.25
    #combine hsv values
    combine_hsv.inputs[0].default_value = 0.6
    combine_hsv.inputs[1].default_value = 0.6
    #refraction bsdf IOR value
    refraction.inputs[2].default_value = 1.33
    #mix shader fac
    mix_shader_1.inputs[0].default_value = 0.2
    mix_shader_2.inputs[0].default_value = 0.75
    mix_shader_2.inputs[0].default_value = 0.625
    #noise and voronoi tex values
    noise_tex.inputs[2].default_value = 50
    noise_tex.inputs[3].default_value = 100
    noise_tex.inputs[4].default_value = 1

    voronoi_tex.inputs[1].default_value = 0.5
    voronoi_tex.inputs[2].default_value = 0.5

    #mix rgb value
    mix_rgb.inputs[0].default_value = 0.999

    #linking nodes
    earth_links = earth_mat.node_tree.links
    #tex coord to base tex
    link1 = earth_links.new(tex_coord.outputs[0], base_tex.inputs[0])
    #tex coord to ocean mask
    link2 = earth_links.new(tex_coord.outputs[0], ocean_mask_tex.inputs[0])
    #ocean mask to invert
    link3 = earth_links.new(ocean_mask_tex.outputs[0], invert_1.inputs[1])
    #base_tex to diffuse bsdf
    link4 = earth_links.new(base_tex.outputs[0], diff.inputs[0])
    #cam data and math nodes setup
    link5 = earth_links.new(cam_data.outputs[2], subtract.inputs[0])
    link6 = earth_links.new(subtract.outputs[0], multiply.inputs[1])
    link7 = earth_links.new(multiply.outputs[0], combine_hsv.inputs[2])
    #combine hsv to glossy bsdf
    link8 = earth_links.new(combine_hsv.outputs[0], glossy.inputs[0])
    link9 = earth_links.new(combine_hsv.outputs[0], glossy.inputs[1])
    #fresnel to refraction bsdf
    link10 = earth_links.new(fresnel.outputs[0], refraction.inputs[2])
    #glossy and refarction to mix shader
    link11 = earth_links.new(glossy.outputs[0], mix_shader_1.inputs[1])
    link12 = earth_links.new(refraction.outputs[0], mix_shader_2.inputs[1])
    #fresnel and mixshader_1 to mixshader_2
    link13 = earth_links.new(fresnel.outputs[0], mix_shader_2.inputs[0])
    link14 = earth_links.new(mix_shader_1.outputs[0], mix_shader_2.inputs[2])
    #diffuse to mix shader 2
    link15 = earth_links.new(diff.outputs[0], mix_shader_2.inputs[1])
    #links to mix shader 3
    link16 = earth_links.new(invert_1.outputs[0], mix_shader_3.inputs[0])
    link17 = earth_links.new(diff.outputs[0], mix_shader_3.inputs[1])
    link18 = earth_links.new(mix_shader_2.outputs[0], mix_shader_3.inputs[2])
    #mix shader 3 to material output
    link19 = earth_links.new(mix_shader_3.outputs[0], material_output.inputs[0])
    #links to bump
    link20 = earth_links.new(tex_coord.outputs[0], bump_tex.inputs[0])
    link21 = earth_links.new(bump_tex.outputs[0], bump.inputs[2])
    link22 = earth_links.new(bump.outputs[0], diff.inputs[2])
    #optional:
    #noise to mix rgb
    #link23 = earth_links.new(noise_tex.outputs[1], mix_rgb.inputs[1])
    #voronoi tex to invert
    #link24 = earth_links.new(voronoi_tex.outputs[1], invert_2.inputs[1])
    #invert to mix rgb
    #link25 = earth_links.new(invert_2.outputs[0], mix_rgb.inputs[2])
    #mix rgb to material output
    #link26 = earth_links.new(mix_rgb.outputs[0], material_output.inputs[2])
    return earth
