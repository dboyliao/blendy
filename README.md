# Blendy Tools: Make blender handy again!

This python module is **not** a standard addon for Blender. 

However, this module is designed for programmers do some simple stuff using python with ease in `blender`, such as setting up the keyframes for animation quickly or basic context management.

## Basic Usage

Here is a simple sample snippet of this module:

```{python}
# Basic animation
from blendy.animation import ArmatureAnimator

# the scene parameters for setting up a scene with 
#    fame per second: 30
#    frame base :1 
#    frame start: 1
#    frame end: 90   ---> a 3 seconds long animation.
scene_params = {
    "frame_start": 1,
    "frame_end": 90
}

# parameters for animation rendering.

render_params = {
    "fps": 30,
    "fps_base": 1
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
    10: {"value":0.314, "rot_reset": False},
    20: {"value":0, "rot_reset": True},
    30: {"value": 0.15},
    40: {"value": 0},
    50: {"value": 0.6},
    60: {"value": 0},
    70: {"value": 0.314},
    80: {"value": 0},
    90: {"value": 0.15}
}

animator = ArmatureAnimator("Armature", scene_params, render_params)
animator.animate(frame_params, "rotate", "jaw", axis = (1, 0, 0))
```

Add audio to animation is easy:

```{python}
# audio editing
from blendy.animation import AudioManager

audio_manager = AudioManager()
audio_manager.add_audio("path/to/your/auio_file",
                      channel = 1,
                      frame_start = 1,
                      relative_path = True)

# audio_manager.clear()  # clear all audio.
```

Or you can use a handy context manager, `BLContext`, to do whatever you want

```{python}
import bpy
import bmesh
from blendy.utils import BLContext

with BLContext("object_name", "EDIT_MESH") as context:
    # Now the object with name as "object_name" has been selected and toggled into edit mesh mode.
    my_object = context.scene.objects.active
    mesh = bmesh.from_edit_mesh(my_object.data)
    # do whatever you want here...
```

## How to Make It Work in Blender?

1. Find the `site-packages` folder of the python interpretor bundled with your Blender.
    - For me, it is `/Applications/Blender/blender.app/Contents/Resources/2.77/python/lib/python3.5/site-packages`
    - Or you can run `import numpy as np; print(np.__file__)` in the python console in `blender` to see where it is.
2. Change working directory to that folder.
3. run `git clone https://github.com/dboyliao/blendy`
4. Now it should be available in the python console in `blender`.

