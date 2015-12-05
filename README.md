# Spe3d Inc. - Blender Tools for Animation

This python module is not a standard addon for Blender. However, this module is designed for programmers to setup the keyframes for animation quickly and easily using python.

## Basic Usage

Here is a simple sample snippet of this module:

```{python}
from spe3d_bl_tools.animation import Animator

# the scene parameters for setting up a scene with 
#    fame per second: 30
#    frame base :1 
#    frame start: 1
#    frame end: 90   ---> a 3 seconds long animation.
scene_params = {
    "fps": 30,
    "fps_base": 1,
    "frame_start": 1,
    "frame_end": 300
}

# This simple animation is setup as following:
#     frame 1: rotate bone "jaw" in "Armature" object with angle 0.314 (in rad)
#     frame 2: rotate bone "jaw" in "Armature" object with 0.314 rad without 
#              reset previous rotation. (0.628 in total)
#     frame 3: rotate bone "jaw" with 0 rad and reset previous rotation.
#     frame 4: rotate bone "jaw" with 0.15 rad. By default, previous rotation 
#              will be reset to 0.
# And the following goes. 

frame_params = {
    1: {"value": 0.314},
    10: {"value":0.314, "rot_reset": Fasle},
    20: {"value":0, "rot_reset": True},
    30: {"value": 0.15},
    40: {"value": 0},
    50: {"value": 0.6},
    60: {"value": 0},
    70: {"value": 0.314},
    80: {"value": 0},
    90: {"value": 0.15}
}

animator = Animator("Armature", scene_params)
animator.animate(frame_params, "rotate", "jaw", axis = (1, 0, 0))
```

## How to Make It Work in Blender?

1. Find the `site-packages` folder of the python interpretor bundled with your Blender.
    - For me, it is `/Applications/Blender/blender.app/Contents/Resources/2.76/python/lib/python3.4/site-packages`
2. Change working directory to that folder.
3. run `git clone https://github.com/spe3d/spe3d_bl_tools.git`
4. Now it should be available in the python console in Blender.

## To Do List

1. MeshAnimator: animator for mesh object.
2. AudioMaker: helper for adding audio to the animation.

