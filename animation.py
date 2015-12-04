# -*- coding: utf-8 -*-

import os, bpy
import numpy as np
from ._utils import frame_params_checker, BLContext
from ._meta import InterfaceAnimator
from .exceptions import NotFoundError

_ops = {
    "rotate": bpy.ops.transform.rotate,
    "translate": bpy.ops.transform.translate,
    "scale": bpy.ops.transform.resize
}

class ArmatureAnimator(InterfaceAnimator):

    def __init__(self, armature_name, scene_params = None):
        scene = bpy.context.scene

        if scene_params is None:
            scene_params = {}
            scene_params["fps"] = 30
            scene_params["fps_base"] = 1
            scene_params["frame_start"] = 1
            scene_params["frame_end"] = 90

        scene.render.fps = scene_params["fps"]
        scene.render.fps_base = scene_params["fps_base"]
        scene.frame_start = scene_params["frame_start"]
        scene.frame_end = scene_params["frame_end"]

        armature = bpy.data.objects.get(armature_name, None)
        if armature is None:
            raise NotFoundError("Armature is not found: {}".format(armature_name))
        
        self.armature = armature

    def animate(self, frame_params, op_type, bone_name = None, **kwargs):
        
        with BLContext(self.armature.name, "POSE") as context:
            armature_data = self.armature.data

    @property
    def armature(self):
        return self.__armature

    @armature.setter
    def armature(self, new_armature):
        if new_armature.type != "ARMATURE":
            raise TypeError("Can not set attribute to non armatrue object.")
        
        self.__armature = new_armature

    def clear(self):
        """
        Clear current animation.
        """
        
        BLContext.TOGGLE_FUNC[bpy.context.mode]()

        bpy.ops.object.select_by_type(type = "ARMATURE")
        bpy.context.active_object.animation_data_clear()

def MeshAnimator(InterfaceAnimator):

    def animate(self, frame_params, op_type, bone_name, **kwargs):
        pass
    
    def clear(self):
        pass

def animate(armature_name, frame_params, op_type, bone_name = None, scene_params = None, **kwargs):
    """
    Automatic animation

    `params`:
        `armature_name` <string>: the name of the armature to be animated.
        `frame_params` <dict>: the dict of frame parameters with frame index as its key and 
                               animation parameters as its value. The animation parameter is a
                               dictionary with keys `rot_reset`, `loc_reset`, `scale_reset` and `value`. 
                               If the value of `<op_type>_reset` is True, then the pose of `<type>` will 
                               be reset before the frame being set. The value will be used in the animation 
                               (ex: the value of transition.. etc)
        `bone_name` <string>: the name of the target bone in the armature to be animated.
                              If it is None, all the bones will be animated.
        `scene_params` <dict>: the parameter used to setup the scene such as fps and fps_base. (by default they are 30 and 1 respectively)
        `op_type` <string>: the type of operation to be applied. It can be "rotation", "scale" or "transition".
        `kwargs`: keyword arguments to be passed to the generic python api `bpy`.
    """
    
    context = bpy.context
    scene = context.scene
    operation = _ops[op_type]

    if scene_params is None:
        scene_params = {}
        scene_params["fps"] = 30
        scene_params["fps_base"] = 1

    frame_params_checker(frame_params)

    ## Switch to pose mode.
    while not context.mode == "POSE":
        bpy.ops.object.posemode.toggle()

    bpy.ops.pose.select_all(action = "DESELECT")

    ## Select armatrue and bone.
    target_armature = bpy.data.armatures[armature_name]
    bones = target_armature.bones

    if bone_name is not None:
        bones[bone_name].select = True
    else:
        bpy.ops.pose.select_all(action = "SELECT")

    ## Setup the scene
    scene.render.fps = scene_params.get("fps", 30)
    scene.render.fps_base = scene_params.get("fps_base", 1)

    for frame_ind, params in frame_params.items():
        scene.frame_set(frame = frame_ind)
        
        if params.get("rot_reset", True):
            bpy.ops.pose.rot_clear()
        if params.get("loc_reset", True):
            bpy.ops.pose.loc_clear()
        if params.get("scale_reset", True):
            bpy.ops.pose.scale_clear()

        operation(value = params["value"], **kwargs)
        bpy.ops.anim.keyframe_insert_menu(type = "LocRotScale")

    bpy.ops.pose.select_all(action = "DESELECT")

class AudioMaker(object):

    def add_audio(self, fname):
        pass

    def clear_audio(self):

        if len(bpy.context.sequences) > 0:
            bpy.ops.sequencer.select_all(action = "SELECT")
            bpy.ops.sequencer.delete()


