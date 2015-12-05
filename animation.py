# -*- coding: utf-8 -*-

import os, bpy
import numpy as np
from ._utils import BLContext, ArmatureParamChecker
from ._meta import InterfaceAnimator
from .exceptions import NotFoundError, SpecError

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
        
        self.__armature = armature

    def animate(self, frame_params, op_type, bone_name = None, **kwargs):
        
        with BLContext(self.armature.name, "pose") as context:
            scene = context.scene
            operation = _ops[op_type]
            param_checker = ArmatureParamChecker()

            # Deselect all objects.
            bpy.ops.pose.select_all(action = "DESELECT")

            armature_data = self.armature.data
            bones = armature_data.bones

            if bone_name is None:
                bpy.ops.pose.select_all(action = "SELECT")
            else:
                bone = bones.get(bone_name, None)
                if bone is None:
                    raise NotFoundError("Bone is not found: {}".format(bone_name))
                bone.select = True
            
            # Checking the format of frame_params
            if param_checker.check(frame_params):

                for frame_ind, params in frame_params.items():
                    scene.frame_set(frame = frame_ind)

                    if params.get("rot_reset", True):
                        bpy.ops.pose.rot_clear()
                    if params.get("loc_reset", True):
                        bpy.ops.pose.loc_clear()
                    if params.get("scale_reset", True):
                        bpy.ops.pose.scale_clear()

                    operation(value = params["value"], **kwargs)
                    bpy.ops.anim.keyframe_insert_menu(type = params.get("anim_type", "LocRotScale"))

                bpy.ops.pose.select_all(action = "DESELECT")
            else:
                raise SpecError("the spec of frame_params is not correct.")

    @property
    def armature(self):
        return self.__armature

    @armature.setter
    def armature(self, new_armature):
        try:
            if new_armature.type != "ARMATURE":
                raise TypeError("Can not set attribute to non armatrue object.")
                self.__armature = new_armature
        except AttributeError as e:
            print(e)

    def clear(self):
        """
        Clear current animation.
        """

        # Switch back to object mode and deselect all objects.
        BLContext.TOGGLE_FUNC[bpy.context.mode]()
        bpy.ops.objects.select_all(action = "DESELECT")

        # select current armature.
        self.armature.select = True 
        # clear animation
        bpy.context.active_object.animation_data_clear()

def MeshAnimator(InterfaceAnimator):

    def animate(self, frame_params, op_type, bone_name, **kwargs):
        pass
    
    def clear(self):
        pass

class AudioMaker(object):

    def add_audio(self, fname):
        pass

    def clear_audio(self):

        if len(bpy.context.sequences) > 0:
            bpy.ops.sequencer.select_all(action = "SELECT")
            bpy.ops.sequencer.delete()


