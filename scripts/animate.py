import bpy



CAMSPEED=1
## Assuming earth radius earthRad
#bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))


def animateCamera(earthRad=1, startLocation=(0,0,0), longitude=0, height=0):
    if startLocation == (0,0,0):
        startLocation = (0, -2*earthRad, 0)
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=([1*earthRad, 1*earthRad, 0.1*earthRad]))
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
    obj=bpy.data.objects
    # bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=startLocation, rotation=(1.5708,0,0))
    # bpy.ops.object.constraint_add(type='TRACK_TO')

    camera_data = bpy.data.cameras.new(name='Camera')
    camera = bpy.data.objects.new('Camera', camera_data)
    bpy.context.collection.objects.link(camera)
    cameraConstraint = camera.constraints.new(type='TRACK_TO')
    cameraConstraint.target = obj["Empty"]
    cameraConstraint.track_axis = 'TRACK_NEGATIVE_Z'
    cameraConstraint.up_axis = 'UP_Y'
    camera.location[2] = height
    bpy.context.scene.camera = camera

    obj["Empty"].location[2] = 0.1*earthRad - height
    obj["Empty"].parent=obj["Empty.001"]
    camera.parent=obj["Empty"]
    camera.location=obj["Camera"].location-obj["Empty"].location
    bpy.context.scene.frame_set(bpy.context.scene.frame_start)
    obj["Empty.001"].rotation_euler = (0, 0, (75+longitude)*0.0174533)
    obj["Empty.001"].keyframe_insert(data_path="rotation_euler", index=2)
    bpy.context.scene.frame_set(bpy.context.scene.frame_end)
    obj["Empty.001"].rotation_euler[2] = (75+longitude)*0.0174533 + (bpy.context.scene.frame_end)*CAMSPEED*3.14/180
    obj["Empty.001"].keyframe_insert(data_path="rotation_euler", index=2)
    for key in obj["Empty.001"].animation_data.action.fcurves.find('rotation_euler',index=2).keyframe_points:
        key.interpolation = 'LINEAR'


def makeStillCamera(camLocation=(0,0,0), earth=None):
    camera_data = bpy.data.cameras.new(name='Camera')
    camera = bpy.data.objects.new('Camera', camera_data)
    camera.location = camLocation
    bpy.context.collection.objects.link(camera)
    # bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=camLocation, rotation=(1.5708,0,0))
    cameraConstraint = camera.constraints.new(type='TRACK_TO')
    if earth is not None:
        cameraConstraint.target = earth
    else:
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
        cameraConstraint.target = bpy.data.objects["Empty"]
    cameraConstraint.track_axis = 'TRACK_NEGATIVE_Z'
    cameraConstraint.up_axis = 'UP_Y'
    bpy.context.scene.camera = camera
    return camera