# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class InterfaceAnimator(object, metaclass = ABCMeta):

    @abstractmethod
    def animate(self, frame_params, op_type, bone_name, **kwargs):
        pass

    @abstractmethod
    def clear(self):
        pass
