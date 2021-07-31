## TODO
# 1. fix command line run errors.
# 5. render image from cmd line
# Render an image/animation instead of just saving the blend file

RAD_EARTH = 6_371 # km
DIST_ES = 149_600_000 # km
SCALE_FAC = 1000 # scaled m per blender m
SCALED_DIST_ES = DIST_ES/(RAD_EARTH*SCALE_FAC)

## Init script
import os
import numpy as np
from datetime import timedelta, datetime
import sys
import argparse
from astropy.time import Time

try:
	import bpy
except ModuleNotFoundError:
	sys.exit("Please run this script using Blender python.\nExample Usage:\nblender --background --python " + __file__ + " -- [options]")

'''
	------------------------------------------------------------------------------------------------------------
	This part is to store the directory information in a variable.
	The first part of this is to check if blender is returning a directory on it's own.
	The second part is to use the path of this script.
'''
dir = os.path.dirname(bpy.data.filepath)
if not dir or dir != "":
	dir = os.path.dirname(__file__)
if dir not in sys.path:
	sys.path.append(dir)
print(os.path.dirname(__file__))

# Import only after adding current directory to sys.path (done in above script)
from scripts import *


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


if __name__ == "__main__":

	argv = sys.argv

	if "--" not in argv:
		argv = []
	else:
		argv = argv[argv.index("--") + 1:]

	usage_text = (
		"Run Blender to get an astrophysically accurate Earth:"
		"  blender --background --python " + __file__ + " -- [options]"
	)

	parser = argparse.ArgumentParser(description=usage_text)
	parser.add_argument("--time", "-t", nargs=1, type=makeTimeArr, default=[[str(datetime.now().hour), str(datetime.now().minute)]], help="Time to be inputted in the format 'HH:MM'", dest="time")
	parser.add_argument("--date", "-d", nargs=1, type=makeDateArr, default=[[str(datetime.now().year), str(datetime.now().month), str(datetime.now().day)]], help="Date to be inputted in the format YYYY-MM-DD", dest="date")
	parser.add_argument("--save", "-s", action='store_true', default=False, help="Use this flag if you want the .blend (Blender) file saved or not.", dest="save")
	parser.add_argument("--animate", "-a", action='store_true', default=False, help="Use this flag if you want default simple animation.", dest="animate")
	parser.add_argument("--latitude", "-lat", type=float, default=19.0760, help="Enter the latitude of starting scene in degrees (North is positive. It should be a decimal value)", dest="latitude")
	parser.add_argument("--longitude", "-lon", type=float, default=72.8777, help="Enter the longitude of starting scene in degrees (East is positive. It should be a decimal value)", dest="longitude")
	parser.add_argument("--render-img", "-ri", action='store_true', default=False, help="Use this flag if you want to render the image.", dest="renderImg")
	parser.add_argument("--render-anim", "-ra", action='store_true', default=False, help="Use this flag if you want to render the default animation in the background.\nNote: --render-anim works only if --animate (-a) is passed.", dest="renderAnim")
	args = parser.parse_args(argv)
	time = timedelta(hours=int(args.time[0][0]), minutes=int(args.time[0][1]))
	date = datetime(year=int(args.date[0][0]), month=int(args.date[0][1]), day=int(args.date[0][2]))
	finalTime = Time(date + time)

	print(finalTime)

	clean_slate()
	earth = earth.makeTerrainOcean(imgDir=dir)
	earth_atmo = atmosphere.makeAtmosphere(earth)
	sun = lighting.makeSun(toTrack=earth, datetime=finalTime)
	clouds = clouds.makeClouds(args.animate)
	bpy.context.scene.render.engine = 'CYCLES'
	bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
	for layer in bpy.context.scene.view_layers:
		layer.cycles.use_denoising = True
	if args.animate:
		animate.animateCamera(longitude=args.longitude, height=(earth.dimensions[0]*3/2*np.sin(np.deg2rad(args.latitude))))
	else:
		animate.makeStillCamera(camLocation=helper.get_cartesian(latitude=args.latitude, longitude=args.longitude, height=earth.dimensions[0], scale=RAD_EARTH*SCALE_FAC), earth=earth)
	if args.save:
		bpy.ops.wm.save_as_mainfile(filepath="./realistic_earth.blend")

	if args.renderImg:
		bpy.context.scene.frame_set(1)
		bpy.context.scene.render.image_settings.file_format='JPEG'
		bpy.context.scene.render.filepath = bpy.path.relpath(os.path.join(dir, "Realistic_Earth_Img"))
		bpy.ops.render.render(use_viewport=True, write_still=True)

	if args.renderAnim and args.animate:
		try:
			os.mkdir("frames")
		except FileExistsError:
			print("Folder 'frames' already exists")
		bpy.context.scene.render.image_settings.file_format = "PNG"
		bpy.context.scene.render.filepath = bpy.path.relpath(os.path.join(dir, "frames", "Realistic_Earth_Anim"))
		bpy.ops.render.render(animation=True, write_still=1)


