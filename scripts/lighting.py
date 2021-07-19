## TODO
# Clean the code a bit

import bpy
from astropy import units as u
from astropy.coordinates import solar_system_ephemeris
from astropy.coordinates import get_body_barycentric

RAD_EARTH = 6_371 # km
DIST_ES = 149_600_000 # km
SCALE_FAC = 1000 # scaled m per blender m
SCALED_DIST_ES = DIST_ES/(RAD_EARTH*SCALE_FAC)

def _getSunCoors(time):
    solar_system_ephemeris.set('builtin')
    earthCoorRaw = get_body_barycentric('earth', time)
    sunCoorRaw = get_body_barycentric('sun', time)
    sunRelCoor = (sunCoorRaw - earthCoorRaw).get_xyz().to(u.m).value/(SCALED_DIST_ES)
    return sunRelCoor


def makeSun(toTrack, datetime, radius=BLEND_RAD_SUN, power=10):
    sunLight = bpy.data.lights.new(name='SunLight', type='SUN')
    sun = bpy.data.objects.new(name='Sun', object_data=sunLight)
    bpy.context.scene.objects.link(sun)
    sunLight.type = 'SUN'
    sunLight.energy = power
    sunConstraint = sun.constraints.new(type='DAMPED_TRACK')
    sunConstraint.target = toTrack
    sunConstraint.track_axis = 'TRACK_NEGATIVE_Z'
    sun.location = _getSunCoors(datetime)
    return sun

#############################################################################################
## Below code is purely for testing purposes. Can be safely ignored. ########################
#############################################################################################

if __name__ == "__main__":

    import sys
    import argparse
    from astropy.time import Time
    import os
    from datetime import timedelta, datetime

    def clean_slate():
        '''
        Simple function to clean up the scene,
        it deletes all objects and material from the scene
        '''
        for o in bpy.context.scene.objects:
            if o.type in ['MESH', 'EMPTY']:
                o.select_set(True)
            else:
                o.select_set(False)
        #
        bpy.ops.object.delete()
        bpy.data.lights.remove(bpy.data.lights[0])
        bpy.data.cameras.remove(bpy.data.cameras[0])
        #
        for m in bpy.data.materials:
            bpy.data.materials.remove(m)


    def makeTimeArr(timeStr):
        return timeStr.split(':')

    def makeDateArr(dateStr):
        return dateStr.split('-')

    def makeEarth():
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))

        #referencing sphere as earth
        earth = bpy.context.active_object

        #adding subsurf modifier
        earth.modifiers.new("earth_mod", 'SUBSURF')
        earth.modifiers["earth_mod"].render_levels = 2

        #shade smooth sphere
        mesh_earth = earth.data
        for face in mesh_earth.polygons:
            face.use_smooth = True


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
        #diffuse BSDF
        diff = earth_nodes.new(type = 'ShaderNodeBsdfDiffuse')
        #Image Texture node for base earth texture
        base_tex = earth_nodes.new(type = 'ShaderNodeTexImage')
        #Image Texture node for ocean mask
        ocean_mask_tex = earth_nodes.new(type = 'ShaderNodeTexImage')
        #Texture coordinate
        tex_coord = earth_nodes.new(type = 'ShaderNodeTexCoord')
        #mix shader
        mix_shader_1 = earth_nodes.new(type = 'ShaderNodeMixShader')
        mix_shader_2 = earth_nodes.new(type = 'ShaderNodeMixShader')
        #Invert node
        invert = earth_nodes.new(type = 'ShaderNodeInvert')


        #adding image to image texture nodes
        #Albedo image
        earth_img = bpy.data.images.load(os.path.join(".", os.path.normpath(r"./Textures/Albedo.jpg")))
        base_tex.image = earth_img
        #changing value of img texture nodes
        base_tex.projection = 'SPHERE'
        base_tex.extension = 'EXTEND'
        base_tex.interpolation = 'Cubic'
        ocean_mask_tex.projection = 'SPHERE'
        ocean_mask_tex.extension = 'EXTEND'
        ocean_mask_tex.interpolation = 'Cubic'

        #ocean mask image
        ocean_mask_img = bpy.data.images.load(os.path.join(".", os.path.normpath(r"./Textures/Ocean_Mask.png")))
        ocean_mask_tex.image = ocean_mask_img

        #invert node fac value
        invert.inputs[0].default_value = 1


        #linking nodes
        earth_links = earth_mat.node_tree.links
        #tex coord to base tex
        link1 = earth_links.new(tex_coord.outputs[0], base_tex.inputs[0])
        #tex coordinate to ocean mask tex
        link2 = earth_links.new(tex_coord.outputs[0], ocean_mask_tex.inputs[0])
        #ocean_mask to invert
        link4 = earth_links.new(ocean_mask_tex.outputs[1], invert.inputs[1])
        #base_tex to diffuse bsdf
        link5 = earth_links.new(base_tex.outputs[0], diff.inputs[0])
        #diffuse to mix shader
        link11 = earth_links.new(diff.outputs[0], mix_shader_1.inputs[1])
        #mix shader 2 to mix shader 1
        link12 = earth_links.new(mix_shader_1.outputs[0], mix_shader_2.inputs[1])
        #invert to mix shader
        link13 = earth_links.new(invert.outputs[0], mix_shader_1.inputs[2])

        #nightlights
        #adding nodes
        #image texture node
        nightlights_tex = earth_nodes.new(type = 'ShaderNodeTexImage')
        #coloramp
        night_colorramp = earth_nodes.new(type = 'ShaderNodeValToRGB')
        #math
        night_multiply = earth_nodes.new(type = 'ShaderNodeMath')
        #emission
        night_emission = earth_nodes.new(type = 'ShaderNodeEmission')


        #changing parameters
        #tex image
        nightlights_img = bpy.data.images.load(os.path.join(".", os.path.normpath(r"./Textures/night_lights_modified.png")))
        nightlights_tex.image = nightlights_img
        nightlights_tex.projection = 'SPHERE'
        nightlights_tex.extension = 'EXTEND'
        nightlights_tex.interpolation = 'Cubic'

        #coloramp
        night_colorramp.color_ramp.elements[1].position = 0.616
        night_colorramp.color_ramp.elements[0].position = 0.116

        #math
        night_multiply.operation = 'MULTIPLY'
        night_multiply.inputs[1].default_value = 0.65

        #emission node
        night_emission.inputs[0].default_value[0] = 0.961
        night_emission.inputs[0].default_value[1] = 1.000
        night_emission.inputs[0].default_value[2] = 0.623
        night_emission.inputs[0].default_value[3] = 1.000


        #links
        #img tex to color ramp
        link39 = earth_links.new(nightlights_tex.outputs[0], night_colorramp.inputs[0])
        #color ramp to multiply
        link40 = earth_links.new(night_colorramp.outputs[0], night_multiply.inputs[0])
        #multiply to emission
        link41 = earth_links.new(night_multiply.outputs[0], night_emission.inputs[1])
        #emission to mix shader
        link43 = earth_links.new(night_emission.outputs[0], mix_shader_2.inputs[2])
        #mix shader to material output
        link44 = earth_links.new(mix_shader_2.outputs[0], material_output.inputs[0])
        #tex coord to img tex
        link45 = earth_links.new(tex_coord.outputs[0], nightlights_tex.inputs[0])

        earth.name = "Earth"
        return earth


    if __name__ == "__main__":

        argv = sys.argv
        print(argv)

        if "--" not in argv:
            argv = []
        else:
            argv = argv[argv.index("--") + 1:]

        usage_text = (
            "Run Blender to get accurate lighting with a minimally shaded Earth:"
            "  blender --background --python " + __file__ + " -- [options]"
            )
        print(argv)

        parser = argparse.ArgumentParser(description=usage_text)
        parser.add_argument("--time", "-t", nargs=1, type=makeTimeArr, default=[['00','00']], help="Time to be inputted in the format 'HH:MM'", dest="time")
        parser.add_argument("--date", "-d", nargs=1, type=makeDateArr, default=[['2021','07','26']], help="Date to be inputted in the format YYYY:MM:DD", dest="date")
        args = parser.parse_args(argv)
        time = timedelta(hours=int(args.time[0][0]), minutes=int(args.time[0][1]))
        date = datetime(year=int(args.date[0][0]), month=int(args.date[0][1]), day=int(args.date[0][2]))
        finalTime = Time(date + time)
        print(finalTime)

        clean_slate()

        earth = makeEarth()
        sun = makeSun(earth, radius=(BLEND_RAD_EARTH + 0.5), power=SCALED_POW)
        sun.location = getSunCoors(finalTime)

        bpy.ops.wm.save_as_mainfile(filepath="./trial3.blend")
        # cam = makeCamera()