import bpy

# Earth radius assumed 1
# cloud sphere radius 16/30

CLOUDSPEED=1

def makeClouds(animBool, earthRad = 1):
    bpy.ops.mesh.primitive_cube_add(size=2*2*earthRad/(2.54), location=(0, 0, 0))
    cloudSphere=bpy.context.active_object
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.subdivide(number_cuts=10)
    bpy.ops.transform.tosphere(value=1, mirror=True)
    bpy.ops.object.editmode_toggle()
    bpy.data.objects["Cube"].scale=[0.986502,0.986502,0.998748]
    bpy.ops.object.subdivision_set(level=4, relative=False)
    bpy.ops.object.shade_smooth()


    clds = bpy.data.materials.new(name="Clouds")
    cloudSphere.data.materials.append(clds)
    clds.use_nodes = True
    nodes = clds.node_tree.nodes
    links = clds.node_tree.links

    mat_out = nodes.get("Material Output")
    bsdf = nodes.get("Principled BSDF")

    final_mix=nodes.new(type="ShaderNodeMixRGB")
    final_mix.blend_type='ADD'
    final_mix.inputs[0].default_value=1

    links.new(final_mix.outputs[0],bsdf.inputs[0])
    links.new(final_mix.outputs[0],bsdf.inputs.get('Alpha'))
    puffy_mix=nodes.new(type="ShaderNodeMixRGB")
    puffy_mix.inputs[2].default_value=[0,0,0,1]
    windy_mix=nodes.new(type="ShaderNodeMixRGB")
    windy_mix.blend_type='MULTIPLY'
    windy_mix.inputs[0].default_value=1

    links.new(puffy_mix.outputs[0],final_mix.inputs[1])
    links.new(windy_mix.outputs[0],final_mix.inputs[2])

    noise1=nodes.new(type="ShaderNodeTexNoise")
    noise1.inputs[2].default_value=6
    noise1.inputs[3].default_value=16
    noise1.inputs[4].default_value=.65

    ramp1=nodes.new(type="ShaderNodeValToRGB")
    ramp1.color_ramp.elements[0].position=0.354545
    ramp1.color_ramp.elements[1].position=0.509092

    links.new(noise1.outputs[0],ramp1.inputs[0])

    noise2=nodes.new(type="ShaderNodeTexNoise")
    noise2.inputs[2].default_value=5
    noise2.inputs[3].default_value=16
    noise2.inputs[4].default_value=.72
    noise2.inputs[5].default_value=1

    vor=nodes.new(type="ShaderNodeTexVoronoi")

    links.new(noise2.outputs[0],vor.inputs[0])

    links.new(ramp1.outputs[0],puffy_mix.inputs[0])
    links.new(vor.outputs[0],puffy_mix.inputs[1])

    noise3=nodes.new(type="ShaderNodeTexNoise")
    noise3.inputs[2].default_value=6.7
    noise3.inputs[3].default_value=16
    noise3.inputs[4].default_value=.5
    noise3.inputs[5].default_value=.1

    ramp3=nodes.new(type="ShaderNodeValToRGB")
    ramp3.color_ramp.elements[0].position=0.472727
    ramp3.color_ramp.elements[1].position=0.654546

    links.new(noise3.outputs[0],ramp3.inputs[0])

    noise4=nodes.new(type="ShaderNodeTexNoise")
    noise4.inputs[2].default_value=2
    noise4.inputs[3].default_value=16
    noise4.inputs[4].default_value=.667
    noise4.inputs[5].default_value=10.4

    ramp4=nodes.new(type="ShaderNodeValToRGB")
    ramp4.color_ramp.elements[0].position=0.468182
    ramp4.color_ramp.elements[1].position=0.645455

    links.new(noise4.outputs[0],ramp4.inputs[0])

    links.new(ramp3.outputs[0],windy_mix.inputs[1])
    links.new(ramp4.outputs[0],windy_mix.inputs[2])

    map=nodes.new(type="ShaderNodeMapping")

    links.new(map.outputs[0],noise1.inputs[0])
    links.new(map.outputs[0],noise2.inputs[0])
    links.new(map.outputs[0],noise3.inputs[0])
    links.new(map.outputs[0],noise4.inputs[0])

    coor=nodes.new(type="ShaderNodeTexCoord")

    links.new(coor.outputs[3],map.inputs[0])

    mapAnim=nodes.new(type="ShaderNodeMapping")

    links.new(coor.outputs[0],mapAnim.inputs[0])

    noiseAnim=nodes.new(type="ShaderNodeTexNoise")
    noiseAnim.inputs[2].default_value=.22
    noiseAnim.inputs[3].default_value=2
    noiseAnim.inputs[4].default_value=.5
    noiseAnim.inputs[5].default_value=0

    val=nodes.new(type="ShaderNodeValue")
    comb1=nodes.new(type="ShaderNodeCombineXYZ")

    links.new(val.outputs[0],comb1.inputs[0])
    links.new(val.outputs[0],comb1.inputs[1])
    links.new(val.outputs[0],comb1.inputs[2])
    links.new(comb1.outputs[0],mapAnim.inputs[1])
    links.new(comb1.outputs[0],mapAnim.inputs[2])
    links.new(mapAnim.outputs[0],noiseAnim.inputs[0])

    add=nodes.new(type="ShaderNodeMath")
    add.operation='ADD'
    mult=nodes.new(type="ShaderNodeMath")
    mult.operation='MULTIPLY'
    mult.inputs[2].default_value=.1
    comb2=nodes.new(type="ShaderNodeCombineXYZ")

    links.new(mult.outputs[0],add.inputs[0])
    links.new(add.outputs[0],comb2.inputs[0])
    links.new(add.outputs[0],comb2.inputs[1])
    links.new(add.outputs[0],comb2.inputs[2])
    links.new(comb2.outputs[0],map.inputs[1])
    links.new(comb2.outputs[0],map.inputs[2])
    links.new(val.outputs[0],add.inputs[1])
    links.new(noiseAnim.outputs[0],mult.inputs[0])

    if animBool:
        val.outputs[0].default_value=0
        val.outputs[0].keyframe_insert("default_value", frame=0)
        bpy.context.scene.frame_set(bpy.context.scene.frame_end)
        val.outputs[0].default_value=(bpy.context.scene.frame_end)*0.001*CLOUDSPEED
        val.outputs[0].keyframe_insert(data_path="default_value", frame=bpy.context.scene.frame_end)

    return cloudSphere
