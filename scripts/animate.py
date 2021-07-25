import bpy



CAMSPEED=1
## Assuming earth radius earthRad
#bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))


def animateCamera(earthRad=1):
    DISTANCE=2*earthRad
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=([1, 1, 0.1]*earthRad))
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
    obj=bpy.data.objects
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0,0,0), rotation=(1.5708,0,0))
    bpy.context.object.location[1] = -DISTANCE
    bpy.ops.object.constraint_add(type='TRACK_TO')
    bpy.context.object.constraints["Track To"].target = obj["Empty"]
    bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
    obj["Empty"].parent=obj["Empty.001"]
    obj["Camera"].parent=obj["Empty"]
    obj["Camera"].location=obj["Camera"].location-obj["Empty"].location
    obj["Empty.001"].keyframe_insert(data_path="rotation_euler", frame=0,index=2)
    bpy.context.scene.frame_set(bpy.context.scene.frame_end)
    obj["Empty.001"].rotation_euler[2]=(bpy.context.scene.frame_end)*CAMSPEED*3.14/180
    obj["Empty.001"].keyframe_insert(data_path="rotation_euler", frame=bpy.context.scene.frame_end,index=2)
    for key in obj["Empty.001"].animation_data.action.fcurves.find('rotation_euler',index=2).keyframe_points:
        key.interpolation = 'LINEAR'


def getDistance():
    return DISTANCE


def makeStillCamera(camLocation=(0,0,0), earth=None):
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0,0,0), rotation=(1.5708,0,0))
    bpy.ops.object.constraint_add(type='TRACK_TO')
    if earth is not None:
        bpy.context.object.constraints["Track To"].target = earth
    else:
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
        bpy.context.object.constraints["Track To"].target = obj["Empty"]
    bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
    bpy.context.object.constraints["Track To"].up_axis = 'UP_Z'
    return bpy.data.objects["Camera"]