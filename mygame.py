import os
import platform

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = "SDL2/x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = "SDL2/x64"

from Framework import game_framework


from pico2d import *
from State import start_state
from State import main_state
from State import boss_state

#open_canvas(1280, 720)
game_framework.run(main_state)
#clear_canvas()