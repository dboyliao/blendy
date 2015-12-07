# -*- coding: utf-8 -*-

import os, bpy
import numpy as np
from ._utils import BLContext, ArmatureParamChecker
from ._meta import InterfaceAnimator
from .exceptions import NotFoundError, SpecError
from bpy.types import Object as BlenderObject

_ops = {
    "rotate": bpy.ops.transform.rotate,
    "translate": bpy.ops.transform.translate,
    "scale": bpy.ops.transform.resize
}

_default_scene_params = {
    "frame_start": 1,
    "frame_end": 90
}

_default_render_params = {
    "fps": 30,
    "fps_base": 1
}

class ArmatureAnimator(InterfaceAnimator):

    def __init__(self, armature_name, scene_params = None, render_params = None):
        
        # Setup the scene and the render parameters.
        self.setup(scene_params, render_params)

        armature = bpy.data.objects.get(armature_name, None)
        if armature is None:
            raise NotFoundError("Armature is not found: {}".format(armature_name))
        
        self.__armature = armature

    def setup(self, scene_params, render_params):

        scene = bpy.context.scene

        # Setup default scene params if there is none.
        if scene_params is None:
            scene_params = _default_scene_params

        # Setup default render params if there is none.
        if render_params is None:
            render_params = _default_render_params

        for attr_name, value in scene_params.items():
            setattr(scene, attr_name, value)

        for attr_name, value in render_params.items():
            setattr(scene.render, attr_name, value)


    def animate(self, frame_params, op_type, bone_name = None, **op_kwargs):
        
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

                    operation(value = params["value"], **op_kwargs)
                    bpy.ops.anim.keyframe_insert_menu(type = params.get("anim_type", "LocRotScale"))

                bpy.ops.pose.select_all(action = "DESELECT")
            else:
                raise SpecError("the spec of frame_params is not correct.")

    @property
    def armature(self):
        return self.__armature

    @armature.setter
    def armature(self, new_armature):
        if not isinstance(new_armature, BlenderObject):
            raise TypeError("This attribute can be set only as object with type {}.".format(BlenderObject))

        if new_armature.type != "ARMATURE":
            raise TypeError("Can not set attribute to non armatrue object.")

        self.__armature = new_armature
        
    def clear(self):
        """
        Clear current armature's animation.
        """

        self.armature.animation_data_clear()

class AudioManager(object):

    def add_audio(self, fpath, **kwargs):
        """
        Add audio.

        `params`:
            `fpath` <string>: path to the audio file to be added.
            `kwargs`: keyword arguement for `bpy.ops.sequencer.sound_strip_add` 
                      except `filepath` and files. 
        """

        old_type = bpy.context.area.type
        bpy.context.area.type = "SEQUENCE_EDITOR"

        bpy.ops.sequencer.sound_strip_add(filepath = fpath, 
                                          files = [{"name": os.path.basename(fpath)}],
                                          **kwargs)
        bpy.context.area.type = old_type

    def clear(self, audio_names = None):
        """
        Clear audio.

        `params`:
            `audio_names` <list>: list of names of audio to be removed. If it
                                  is None, all audio will be removed.
        """

        if audio_names is None:

            if len(bpy.context.sequences) > 0:
                bpy.ops.sequencer.select_all(action = "SELECT")
                bpy.ops.sequencer.delete()
        else:
            for audio_name in audio_names:
                sound_obj = bpy.context.scene.sequence_editor.sequences_all.get(audio_name, None)
                if sound_obj is not None:
                    bpy.context.scene.sequence_editor.sequences.remove(sound_obj)

