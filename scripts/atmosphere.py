import bpy

def makeAtmosphere(earth):
    '''
    function which takes in a planet, makes earth-like atmosphere for that planet and parents it to the planet in blender
    '''

    ##### Creating 'Sphere Height' Node Group #####

    sphere_height_node_group = bpy.data.node_groups.new('SphereHeight', 'ShaderNodeTree')

    # Node Group Inputs
    SH_NG_inputs = sphere_height_node_group.nodes.new('NodeGroupInput')
    sphere_height_node_group.inputs.new('NodeSocketFloat', 'Planet Radius')
    sphere_height_node_group.inputs.new('NodeSocketVector', 'Planet Dimensions')

    # Node Group Outputs
    SH_NG_outputs = sphere_height_node_group.nodes.new('NodeGroupOutput')
    sphere_height_node_group.outputs.new('NodeSocketFloat', 'Current Distance')

    ## Adding Nodes in 'Sphere Height'
    SH_object_info = sphere_height_node_group.nodes.new('ShaderNodeObjectInfo')

    SH_geometry = sphere_height_node_group.nodes.new('ShaderNodeNewGeometry')

    SH_Vsubtract = sphere_height_node_group.nodes.new('ShaderNodeVectorMath')
    SH_Vsubtract.operation = 'SUBTRACT'

    SH_Vdivide1 = sphere_height_node_group.nodes.new('ShaderNodeVectorMath')
    SH_Vdivide1.operation = 'DIVIDE'
    SH_Vdivide1.inputs[1].default_value = (2,2,2)

    SH_Vdivide2 = sphere_height_node_group.nodes.new('ShaderNodeVectorMath')
    SH_Vdivide2.operation = 'DIVIDE'

    SH_Vlength = sphere_height_node_group.nodes.new('ShaderNodeVectorMath')
    SH_Vlength.operation = 'LENGTH'

    SH_multiply = sphere_height_node_group.nodes.new('ShaderNodeMath')
    SH_multiply.operation = 'MULTIPLY'

    ## Linking nodes inside 'Sphere Height'
    sphere_height_node_group.links.new(SH_NG_inputs.outputs[0], SH_multiply.inputs[1])
    sphere_height_node_group.links.new(SH_NG_inputs.outputs[1], SH_Vdivide1.inputs[0])
    sphere_height_node_group.links.new(SH_object_info.outputs[0], SH_Vsubtract.inputs[1])
    sphere_height_node_group.links.new(SH_geometry.outputs[0], SH_Vsubtract.inputs[0])
    sphere_height_node_group.links.new(SH_Vsubtract.outputs[0], SH_Vdivide2.inputs[0])
    sphere_height_node_group.links.new(SH_Vdivide1.outputs[0], SH_Vdivide2.inputs[1])
    sphere_height_node_group.links.new(SH_Vdivide2.outputs[0], SH_Vlength.inputs[0])
    sphere_height_node_group.links.new(SH_Vlength.outputs[1], SH_multiply.inputs[0])
    sphere_height_node_group.links.new(SH_multiply.outputs[0], SH_NG_outputs.inputs[0])

    ##### 'Sphere Height' Created #####

    ##### Creating 'Barometric Formula Precise' Node Group #####

    baro_formula_precise_node_group = bpy.data.node_groups.new('BarometricFormulaPrecise', 'ShaderNodeTree')
    # Node Group Inputs
    BFP_NG_inputs = baro_formula_precise_node_group.nodes.new('NodeGroupInput')
    baro_formula_precise_node_group.inputs.new('NodeSocketFloat', 'Current Height')
    baro_formula_precise_node_group.inputs.new('NodeSocketFloat', 'Planet\'s Radius')
    baro_formula_precise_node_group.inputs.new('NodeSocketFloat', 'Atmospheric Density Sea Level (kg/m3)')
    baro_formula_precise_node_group.inputs.new('NodeSocketFloat', 'Molar Mass of Planet\'s Air')
    baro_formula_precise_node_group.inputs.new('NodeSocketFloat', 'Gravitational Acceleration')
    baro_formula_precise_node_group.inputs.new('NodeSocketFloat', 'Universal Gas Constant')
    baro_formula_precise_node_group.inputs[5].default_value = 8.314
    baro_formula_precise_node_group.inputs.new('NodeSocketFloat', 'Standard Temperature (Sea-Level, Celsius')

    # Node Group Outputs
    BFP_NG_outputs = baro_formula_precise_node_group.nodes.new('NodeGroupOutput')
    baro_formula_precise_node_group.outputs.new('NodeSocketFloat', 'Pressure / Density')

    ## Adding nodes in 'Barometric Formula Precise'
    BFP_add = baro_formula_precise_node_group.nodes.new('ShaderNodeMath')
    BFP_add.operation = 'ADD'
    BFP_add.inputs[1].default_value = 272.150

    BFP_multiply1 = baro_formula_precise_node_group.nodes.new('ShaderNodeMath')
    BFP_multiply1.operation = 'MULTIPLY'

    BFP_multiply2 = baro_formula_precise_node_group.nodes.new('ShaderNodeMath')
    BFP_multiply2.operation = 'MULTIPLY'

    BFP_subtract = baro_formula_precise_node_group.nodes.new('ShaderNodeMath')
    BFP_subtract.operation = 'SUBTRACT'

    BFP_divide = baro_formula_precise_node_group.nodes.new('ShaderNodeMath')
    BFP_divide.operation = 'DIVIDE'

    BFP_multiply3 = baro_formula_precise_node_group.nodes.new('ShaderNodeMath')
    BFP_multiply3.operation = 'MULTIPLY'

    BFP_multiply4 = baro_formula_precise_node_group.nodes.new('ShaderNodeMath')
    BFP_multiply4.operation = 'MULTIPLY'
    BFP_multiply4.inputs[1].default_value = -1

    BFP_power = baro_formula_precise_node_group.nodes.new('ShaderNodeMath')
    BFP_power.operation = 'POWER'
    BFP_power.inputs[0].default_value = 2.718

    BFP_multiply5 = baro_formula_precise_node_group.nodes.new('ShaderNodeMath')
    BFP_multiply5.operation = 'MULTIPLY'

    ## Linking nodes inside 'Barometric Formula Precise'
    baro_formula_precise_node_group.links.new(BFP_NG_inputs.outputs[0], BFP_subtract.inputs[0])
    baro_formula_precise_node_group.links.new(BFP_NG_inputs.outputs[1], BFP_subtract.inputs[1])
    baro_formula_precise_node_group.links.new(BFP_NG_inputs.outputs[2], BFP_multiply5.inputs[1])
    baro_formula_precise_node_group.links.new(BFP_NG_inputs.outputs[3], BFP_multiply1.inputs[0])
    baro_formula_precise_node_group.links.new(BFP_NG_inputs.outputs[4], BFP_multiply1.inputs[1])
    baro_formula_precise_node_group.links.new(BFP_NG_inputs.outputs[5], BFP_multiply2.inputs[0])
    baro_formula_precise_node_group.links.new(BFP_NG_inputs.outputs[6], BFP_add.inputs[0])
    baro_formula_precise_node_group.links.new(BFP_add.outputs[0], BFP_multiply2.inputs[1])
    baro_formula_precise_node_group.links.new(BFP_multiply1.outputs[0], BFP_divide.inputs[0])
    baro_formula_precise_node_group.links.new(BFP_multiply2.outputs[0], BFP_divide.inputs[1])
    baro_formula_precise_node_group.links.new(BFP_subtract.outputs[0], BFP_multiply3.inputs[0])
    baro_formula_precise_node_group.links.new(BFP_divide.outputs[0], BFP_multiply3.inputs[1])
    baro_formula_precise_node_group.links.new(BFP_multiply3.outputs[0], BFP_multiply4.inputs[0])
    baro_formula_precise_node_group.links.new(BFP_multiply4.outputs[0], BFP_power.inputs[1])
    baro_formula_precise_node_group.links.new(BFP_power.outputs[0], BFP_multiply5.inputs[0])
    baro_formula_precise_node_group.links.new(BFP_multiply5.outputs[0], BFP_NG_outputs.inputs[0])

    ##### 'Barometric Formula Precise' created #####

    ##### Creating 'Ozone Layer Density' node group #####

    ozone_layer_density_node_group = bpy.data.node_groups.new('OzoneLayerDensity', 'ShaderNodeTree')

    # Node Group Inputs
    OLD_NG_inputs = ozone_layer_density_node_group.nodes.new('NodeGroupInput')
    ozone_layer_density_node_group.inputs.new('NodeSocketFloat', 'Current Height')
    ozone_layer_density_node_group.inputs.new('NodeSocketFloat', 'Density')
    ozone_layer_density_node_group.inputs.new('NodeSocketFloat', 'Planet Radius')
    ozone_layer_density_node_group.inputs.new('NodeSocketFloat', 'Gravitational Acceleration')
    ozone_layer_density_node_group.inputs.new('NodeSocketFloat', 'Ozone Night Glow Intensity')

    # Node Group Outputs
    OLD_NG_outputs = ozone_layer_density_node_group.nodes.new('NodeGroupOutput')
    ozone_layer_density_node_group.outputs.new('NodeSocketFloat', 'Density Ozone')
    ozone_layer_density_node_group.outputs.new('NodeSocketFloat', 'Density Night Light Ozone')

    ## Adding Nodes in 'Ozone Layer Density'
    OLD_divide1 = ozone_layer_density_node_group.nodes.new('ShaderNodeMath')
    OLD_divide1.operation = 'DIVIDE'
    OLD_divide1.inputs[0].default_value = 9.870

    OLD_subtract1 = ozone_layer_density_node_group.nodes.new('ShaderNodeMath')
    OLD_subtract1.operation = 'SUBTRACT'

    OLD_multiply1 = ozone_layer_density_node_group.nodes.new('ShaderNodeMath')
    OLD_multiply1.operation = 'MULTIPLY'

    OLD_mapRange = ozone_layer_density_node_group.nodes.new('ShaderNodeMapRange')
    OLD_mapRange.interpolation_type = 'LINEAR'
    OLD_mapRange.clamp = True
    OLD_mapRange.inputs[1].default_value = 0
    OLD_mapRange.inputs[3].default_value = 0
    OLD_mapRange.inputs[4].default_value = 1

    OLD_colorRamp1 = ozone_layer_density_node_group.nodes.new('ShaderNodeValToRGB')
    OLD_colorRamp1.color_ramp.elements[0].color = (0.015, 0.015, 0.015, 1)
    OLD_colorRamp1.color_ramp.elements[1].color = (0,0,0,1)
    OLD_colorRamp1.color_ramp.elements.new(0.150).color = (0.005, 0.005, 0.005, 1)
    OLD_colorRamp1.color_ramp.elements.new(0.250).color = (0.5, 0.5, 0.5, 1)
    OLD_colorRamp1.color_ramp.elements.new(0.380).color = (1,1,1,1)
    OLD_colorRamp1.color_ramp.elements.new(0.400).color = (0.775, 0.775, 0.775, 1)
    OLD_colorRamp1.color_ramp.elements.new(0.450).color = (0.3, 0.3, 0.3, 1)
    OLD_colorRamp1.color_ramp.elements.new(0.500).color = (0.25, 0.25, 0.25, 1)
    OLD_colorRamp1.color_ramp.elements.new(0.600).color = (0.1, 0.1, 0.1, 1)
    OLD_colorRamp1.color_ramp.elements.new(0.800).color = (0.02, 0.02, 0.02, 1)

    OLD_colorRamp2 = ozone_layer_density_node_group.nodes.new('ShaderNodeValToRGB')
    OLD_colorRamp2.color_ramp.interpolation = 'EASE'
    OLD_colorRamp2.color_ramp.elements[0].color = (0, 0, 0, 1)
    OLD_colorRamp2.color_ramp.elements[1].color = (0, 0, 0, 1)
    OLD_colorRamp2.color_ramp.elements.new(0.923).color = (0.000774, 0.000774, 0.000774, 1)
    OLD_colorRamp2.color_ramp.elements.new(0.964).color = (0.033105, 0.033105, 0.033105, 1)

    OLD_multiply2 = ozone_layer_density_node_group.nodes.new('ShaderNodeMath')
    OLD_multiply2.operation = 'MULTIPLY'
    OLD_multiply2.inputs[1].default_value = 100000

    OLD_multiply3 = ozone_layer_density_node_group.nodes.new('ShaderNodeMath')
    OLD_multiply3.operation = 'MULTIPLY'

    OLD_multiply4 = ozone_layer_density_node_group.nodes.new('ShaderNodeMath')
    OLD_multiply4.operation = 'MULTIPLY'

    ## Linking nodes inside 'Ozone Layer Density'
    ozone_layer_density_node_group.links.new(OLD_NG_inputs.outputs[0], OLD_subtract1.inputs[0])
    ozone_layer_density_node_group.links.new(OLD_NG_inputs.outputs[1], OLD_multiply2.inputs[1])
    ozone_layer_density_node_group.links.new(OLD_NG_inputs.outputs[1], OLD_multiply3.inputs[0])
    ozone_layer_density_node_group.links.new(OLD_NG_inputs.outputs[2], OLD_subtract1.inputs[1])
    ozone_layer_density_node_group.links.new(OLD_NG_inputs.outputs[3], OLD_divide1.inputs[1])
    ozone_layer_density_node_group.links.new(OLD_NG_inputs.outputs[4], OLD_multiply4.inputs[1])
    ozone_layer_density_node_group.links.new(OLD_divide1.outputs[0], OLD_multiply1.inputs[0])
    ozone_layer_density_node_group.links.new(OLD_subtract1.outputs[0], OLD_mapRange.inputs[0])
    ozone_layer_density_node_group.links.new(OLD_multiply1.outputs[0], OLD_mapRange.inputs[2])
    ozone_layer_density_node_group.links.new(OLD_mapRange.outputs[0], OLD_colorRamp1.inputs[0])
    ozone_layer_density_node_group.links.new(OLD_mapRange.outputs[0], OLD_colorRamp2.inputs[0])
    ozone_layer_density_node_group.links.new(OLD_colorRamp1.outputs[0], OLD_multiply2.inputs[0])
    ozone_layer_density_node_group.links.new(OLD_colorRamp2.outputs[0], OLD_multiply3.inputs[1])
    ozone_layer_density_node_group.links.new(OLD_multiply2.outputs[0], OLD_NG_outputs.inputs[0])
    ozone_layer_density_node_group.links.new(OLD_multiply3.outputs[0], OLD_multiply4.inputs[0])
    ozone_layer_density_node_group.links.new(OLD_multiply4.outputs[0], OLD_NG_outputs.inputs[1])

    ##### 'Ozone Layer Density' created #####

    ##### Creating 'Volume Shader' node group #####

    volume_shader_node_group = bpy.data.node_groups.new('VolumeShader', 'ShaderNodeTree')

    # Node Group Inputs
    VS_NG_inputs = volume_shader_node_group.nodes.new('NodeGroupInput')
    volume_shader_node_group.inputs.new('NodeSocketFloat', 'Planet Radius')
    volume_shader_node_group.inputs.new('NodeSocketFloat', 'Current Height')
    volume_shader_node_group.inputs.new('NodeSocketColor', 'Atmo Color')
    volume_shader_node_group.inputs.new('NodeSocketFloat', 'Density Air')
    volume_shader_node_group.inputs.new('NodeSocketFloat', 'Density Stream')
    volume_shader_node_group.inputs.new('NodeSocketFloat', 'Anisotropy Stream')
    volume_shader_node_group.inputs.new('NodeSocketFloat', 'Density Ozone Layer')
    volume_shader_node_group.inputs.new('NodeSocketFloat', 'DensityOzoneNightLight')

    # Node Group outputs
    VS_NG_outputs = volume_shader_node_group.nodes.new('NodeGroupOutput')
    volume_shader_node_group.outputs.new('NodeSocketShader', 'Volume')

    ## Adding nodes in 'Volume Shader'
    VS_multiply1 = volume_shader_node_group.nodes.new('ShaderNodeMath')
    VS_multiply1.operation = 'MULTIPLY'
    VS_multiply1.inputs[1].default_value = 0.998

    VS_multiply2 = volume_shader_node_group.nodes.new('ShaderNodeMath')
    VS_multiply2.operation = 'MULTIPLY'

    VS_invert1 = volume_shader_node_group.nodes.new('ShaderNodeInvert')
    VS_invert1.inputs[0].default_value = 1

    VS_multiply3 = volume_shader_node_group.nodes.new('ShaderNodeMath')
    VS_multiply3.operation = 'MULTIPLY'
    VS_multiply3.inputs[1].default_value = 1.250

    VS_invert2 = volume_shader_node_group.nodes.new('ShaderNodeInvert')
    VS_invert2.inputs[0].default_value = 1

    VS_greater1 = volume_shader_node_group.nodes.new('ShaderNodeMath')
    VS_greater1.operation = 'GREATER_THAN'

    VS_volumeScatter1 = volume_shader_node_group.nodes.new('ShaderNodeVolumeScatter')
    VS_volumeScatter1.inputs[2].default_value = 0

    VS_volumeScatter2 = volume_shader_node_group.nodes.new('ShaderNodeVolumeScatter')
    VS_volumeScatter2.inputs[0].default_value = (1,1,1,1)

    VS_volumeAbsorption1 = volume_shader_node_group.nodes.new('ShaderNodeVolumeAbsorption')

    VS_volumeScatter3 = volume_shader_node_group.nodes.new('ShaderNodeVolumeScatter')
    VS_volumeScatter3.inputs[2].default_value = 0.1

    VS_volumeAbsorption2 = volume_shader_node_group.nodes.new('ShaderNodeVolumeAbsorption')

    VS_emission = volume_shader_node_group.nodes.new('ShaderNodeEmission')
    VS_emission.inputs[0].default_value = (0.411, 1, 0.138, 1)

    VS_volumeScatter4 = volume_shader_node_group.nodes.new('ShaderNodeVolumeScatter')

    VS_addShader1 = volume_shader_node_group.nodes.new('ShaderNodeAddShader')

    VS_addShader2 = volume_shader_node_group.nodes.new('ShaderNodeAddShader')

    VS_addShader3 = volume_shader_node_group.nodes.new('ShaderNodeAddShader')
    
    VS_addShader4 = volume_shader_node_group.nodes.new('ShaderNodeAddShader')

    VS_transparentBsdf = volume_shader_node_group.nodes.new('ShaderNodeBsdfTransparent')
    VS_transparentBsdf.inputs[0].default_value = (1,1,1,1)

    VS_addShader5 = volume_shader_node_group.nodes.new('ShaderNodeAddShader')

    VS_mixShader = volume_shader_node_group.nodes.new('ShaderNodeMixShader')

    ## Linking nodes inside 'Volume Scatter'
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[0], VS_multiply1.inputs[0])
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[1], VS_greater1.inputs[0])
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[2], VS_volumeScatter1.inputs[0])
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[2], VS_invert1.inputs[1])
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[2], VS_volumeScatter3.inputs[1])
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[2], VS_invert2.inputs[1])
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[3], VS_volumeScatter1.inputs[1])
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[3], VS_multiply2.inputs[0])
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[3], VS_multiply3.inputs[0])
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[4], VS_multiply2.inputs[1])
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[5], VS_volumeScatter2.inputs[2])
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[6], VS_volumeScatter3.inputs[1])
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[6], VS_volumeAbsorption2.inputs[1])
    volume_shader_node_group.links.new(VS_NG_inputs.outputs[7], VS_emission.inputs[1])
    volume_shader_node_group.links.new(VS_multiply1.outputs[0], VS_greater1.inputs[1])
    volume_shader_node_group.links.new(VS_multiply2.outputs[0], VS_volumeScatter2.inputs[1])
    volume_shader_node_group.links.new(VS_invert1.outputs[0], VS_volumeAbsorption1.inputs[0])
    volume_shader_node_group.links.new(VS_multiply3.outputs[0], VS_volumeAbsorption1.inputs[1])
    volume_shader_node_group.links.new(VS_invert2.outputs[0], VS_volumeAbsorption2.inputs[0])
    volume_shader_node_group.links.new(VS_greater1.outputs[0], VS_mixShader.inputs[0])
    volume_shader_node_group.links.new(VS_volumeScatter1.outputs[0], VS_addShader1.inputs[0])
    volume_shader_node_group.links.new(VS_volumeScatter2.outputs[0], VS_addShader1.inputs[1])
    volume_shader_node_group.links.new(VS_volumeAbsorption1.outputs[0], VS_addShader3.inputs[1])
    volume_shader_node_group.links.new(VS_volumeScatter3.outputs[0], VS_addShader2.inputs[0])
    volume_shader_node_group.links.new(VS_volumeAbsorption2.outputs[0], VS_addShader2.inputs[1])
    volume_shader_node_group.links.new(VS_emission.outputs[0], VS_addShader4.inputs[1])
    volume_shader_node_group.links.new(VS_addShader1.outputs[0], VS_addShader3.inputs[0])
    volume_shader_node_group.links.new(VS_addShader2.outputs[0], VS_addShader4.inputs[0])
    volume_shader_node_group.links.new(VS_addShader3.outputs[0], VS_addShader5.inputs[0])
    volume_shader_node_group.links.new(VS_addShader4.outputs[0], VS_addShader5.inputs[1])
    volume_shader_node_group.links.new(VS_transparentBsdf.outputs[0], VS_mixShader.inputs[1])
    volume_shader_node_group.links.new(VS_addShader5.outputs[0], VS_mixShader.inputs[2])
    volume_shader_node_group.links.new(VS_mixShader.outputs[0], VS_NG_outputs.inputs[0])

    ##### 'Volume Shader' created #####

    ##### Create 'Spheric Atmospheric Barometric' Node Group #####

    spheric_atmo_baro_node_group = bpy.data.node_groups.new('SphericAtmosphericBarometric', 'ShaderNodeTree')

    # Node Group Inputs
    SAB_NG_inputs = spheric_atmo_baro_node_group.nodes.new('NodeGroupInput')
    spheric_atmo_baro_node_group.inputs.new('NodeSocketVector', 'Planet Dimensions (Blender Unit)')
    spheric_atmo_baro_node_group.inputs[0].default_value = earth.dimensions

    spheric_atmo_baro_node_group.inputs.new('NodeSocketColor', 'Scattering Color')
    spheric_atmo_baro_node_group.inputs[1].default_value = (0.214, 0.638, 1, 1)

    spheric_atmo_baro_node_group.inputs.new('NodeSocketFloat', 'Air Density')
    spheric_atmo_baro_node_group.inputs[2].default_value = 1

    spheric_atmo_baro_node_group.inputs.new('NodeSocketFloat', 'DensityStream (Relative To Air)')
    spheric_atmo_baro_node_group.inputs[3].default_value = 0.05

    spheric_atmo_baro_node_group.inputs.new('NodeSocketFloat', 'OzoneDensity')
    spheric_atmo_baro_node_group.inputs[4].default_value = 0.05

    spheric_atmo_baro_node_group.inputs.new('NodeSocketFloat', 'OzoneNightGlowIntensity')
    spheric_atmo_baro_node_group.inputs[5].default_value = 1

    spheric_atmo_baro_node_group.inputs.new('NodeSocketFloat', 'AnisotropySteam')
    spheric_atmo_baro_node_group.inputs[6].default_value = 0.975

    spheric_atmo_baro_node_group.inputs.new('NodeSocketFloat', 'Planet Radius (m)')
    spheric_atmo_baro_node_group.inputs[7].default_value = 6357000

    spheric_atmo_baro_node_group.inputs.new('NodeSocketFloat', 'Atmospheric Density Sea Level (kg/m3)')
    spheric_atmo_baro_node_group.inputs[8].default_value = 1.250

    spheric_atmo_baro_node_group.inputs.new('NodeSocketFloat', 'Gravitational Acceleration (m/s2)')
    spheric_atmo_baro_node_group.inputs[9].default_value = 9.870

    spheric_atmo_baro_node_group.inputs.new('NodeSocketFloat', 'Molar Mass Of Planet\'s Air (kg/mol)')
    spheric_atmo_baro_node_group.inputs[10].default_value = 0.029

    spheric_atmo_baro_node_group.inputs.new('NodeSocketFloat', 'Temperature (Sea-Level, Celsius)')
    spheric_atmo_baro_node_group.inputs[11].default_value = 15

    # Node Group Outputs
    SAB_NG_outputs = spheric_atmo_baro_node_group.nodes.new('NodeGroupOutput')
    spheric_atmo_baro_node_group.outputs.new('NodeSocketShader', 'Volume')

    ## Adding nodes in 'Spheric Atmospheric Barometric'

    # Adding 'Sphere Height' node group
    sphere_height_groupNode = spheric_atmo_baro_node_group.nodes.new('ShaderNodeGroup')
    sphere_height_groupNode.node_tree = sphere_height_node_group

    # Adding 'Barometric Formula Precise' node group
    baro_formula_precise_groupNode = spheric_atmo_baro_node_group.nodes.new('ShaderNodeGroup')
    baro_formula_precise_groupNode.node_tree = baro_formula_precise_node_group

    # Adding 'Ozone Layer Density' node group
    ozone_layer_density_groupNode = spheric_atmo_baro_node_group.nodes.new('ShaderNodeGroup')
    ozone_layer_density_groupNode.node_tree = ozone_layer_density_node_group

    # Adding 'Volume Shader' node group
    volume_shader_groupNode = spheric_atmo_baro_node_group.nodes.new('ShaderNodeGroup')
    volume_shader_groupNode.node_tree = volume_shader_node_group

    # Adding miscellaneous nodes
    SAB_multiply1 = spheric_atmo_baro_node_group.nodes.new('ShaderNodeMath')
    SAB_multiply1.operation = 'MULTIPLY'

    SAB_power1 = spheric_atmo_baro_node_group.nodes.new('ShaderNodeMath')
    SAB_power1.operation = 'POWER'
    SAB_power1.inputs[1].default_value = 1

    ## Linking nodes in 'Spheric Atmospheric Barometric'
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[7], sphere_height_groupNode.inputs[0])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[0], sphere_height_groupNode.inputs[1])

    spheric_atmo_baro_node_group.links.new(sphere_height_groupNode.outputs[0], baro_formula_precise_groupNode.inputs[0])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[7], baro_formula_precise_groupNode.inputs[1])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[8], baro_formula_precise_groupNode.inputs[2])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[10], baro_formula_precise_groupNode.inputs[3])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[9], baro_formula_precise_groupNode.inputs[4])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[11], baro_formula_precise_groupNode.inputs[6])

    spheric_atmo_baro_node_group.links.new(sphere_height_groupNode.outputs[0], ozone_layer_density_groupNode.inputs[0])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[4], ozone_layer_density_groupNode.inputs[1])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[7], ozone_layer_density_groupNode.inputs[2])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[9], ozone_layer_density_groupNode.inputs[3])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[5], ozone_layer_density_groupNode.inputs[4])

    spheric_atmo_baro_node_group.links.new(baro_formula_precise_groupNode.outputs[0], SAB_multiply1.inputs[0])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[2], SAB_multiply1.inputs[1])
    spheric_atmo_baro_node_group.links.new(SAB_multiply1.outputs[0], SAB_power1.inputs[0])

    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[7], volume_shader_groupNode.inputs[0])
    spheric_atmo_baro_node_group.links.new(sphere_height_groupNode.outputs[0], volume_shader_groupNode.inputs[1])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[1], volume_shader_groupNode.inputs[2])
    spheric_atmo_baro_node_group.links.new(SAB_power1.outputs[0], volume_shader_groupNode.inputs[3])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[3], volume_shader_groupNode.inputs[4])
    spheric_atmo_baro_node_group.links.new(SAB_NG_inputs.outputs[6], volume_shader_groupNode.inputs[5])
    spheric_atmo_baro_node_group.links.new(ozone_layer_density_groupNode.outputs[0], volume_shader_groupNode.inputs[6])
    spheric_atmo_baro_node_group.links.new(ozone_layer_density_groupNode.outputs[1], volume_shader_groupNode.inputs[7])

    spheric_atmo_baro_node_group.links.new(volume_shader_groupNode.outputs[0], SAB_NG_outputs.inputs[0])

    ##### 'Spheric Atmospheric Barometric' created #####

    ##### Creating the actual material #####

    atmo_mat = bpy.data.materials.new(name="Earth_Atmo")
    bpy.ops.mesh.primitive_uv_sphere_add(radius=32*earth.dimensions[0]/30, enter_editmode=False, align='WORLD', location=earth.location)
    earth_atmo = bpy.context.active_object
    earth_atmo.parent = earth
    earth_atmo.data.materials.append(atmo_mat)
    atmo_mat.use_nodes = True
    atmo_nodes = atmo_mat.node_tree.nodes
    atmo_nodes.remove(atmo_nodes['Principled BSDF'])

    material_output = atmo_nodes.get('Material Output')

    ## Adding 'Spheric Atmospheric Barometric' Node Group to Material
    spheric_atmo_baro_groupNode = atmo_nodes.new('ShaderNodeGroup')
    spheric_atmo_baro_groupNode.node_tree = spheric_atmo_baro_node_group

    ## Linking 'Spheric Atmospheric Barometric' Node Group to Material Output
    atmo_links = atmo_mat.node_tree.links
    atmo_links.new(spheric_atmo_baro_groupNode.outputs[0], material_output.inputs[1])
    
    
    return earth_atmo
