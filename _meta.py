# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class InterfaceAnimator(object, metaclass = ABCMeta):

    @abstractmethod
    def animate(self, frame_params, op_type, bone_name, **kwargs):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def setup(self, scene_params, render_params):
        pass

class InterfaceParamChecker(object, metaclass = ABCMeta):

    @abstractmethod
    def check(self, params):
        pass
