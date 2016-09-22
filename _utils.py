# -*- coding: utf-8 -*-

from .exceptions import NotFoundError
from functools import partial, wraps
from ._meta import InterfaceParamChecker
import bpy

class ArmatureParamChecker(InterfaceParamChecker):
    """
    Checker for armature animation parameter.
    """

    def check(self, params):

        if not isinstance(params, dict):
            return False

        for ind, param in params.items():
            if not isinstance(param, dict):
                return False

            if not isinstance(ind, int) or not "value" in param.keys():
                return False

        return True


class BLContext(object):

    TOGGLE_FUNC = {
                   "POSE": bpy.ops.object.posemode_toggle,
                   "EDIT_MESH": bpy.ops.object.editmode_toggle,
                   "EDIT_ARMATURE": bpy.ops.object.editmode_toggle,
                   "WEIGHT_PAINT": bpy.ops.paint.weight_paint_toggle,
                   "OBJECT": lambda: None
                   }

    def __init__(self, object_name, mode_name):
        self.__old_mode = bpy.context.mode
        self.__target_mode = mode_name.upper()
        obj = bpy.data.objects.get(object_name, None)

        if obj is None:
            raise NotFoundError("object not found: {}".format(object_name))

        self.__object = obj

    def __enter__(self):

        # Make sure it start with object mode.
        if bpy.context.mode != 'OBJECT':
            self.TOGGLE_FUNC[bpy.context.mode]()

        # Select the target object and make it active.
        bpy.ops.object.select_all(action = "DESELECT") # deselect all objects
        bpy.context.scene.objects.active = self.__object
        self.__object.select = True
        self.__object.hide = False

        # return if the target mode is object mode.(already is)
        if self.__target_mode == "OBJECT":
            return bpy.context

        # Toggle to the correct mode
        if self._valid_config():
            while bpy.context.mode != self.__target_mode:
                self.TOGGLE_FUNC[self.__target_mode]()
        else:
            raise RuntimeError("The target mode is not valid for target object: {}".format(self.__object.name))

        return bpy.context

    def __exit__(self, exc_type, exc_value, exc_tb):

        self.TOGGLE_FUNC[bpy.context.mode]() # Switch to object mode.
        self.TOGGLE_FUNC[self.__old_mode]()

        return False

    def _valid_config(self):

        if self.__target_mode in ["EDIT_MESH", "EDIT_ARMATURE"]:
            return True
        elif self.__target_mode == "POSE" and self.__object.type == "ARMATURE":
            return True
        elif self.__target_mode == "WEIGHT_PAINT" and self.__object.type == "MESH":
            return True
        else:
            return False
