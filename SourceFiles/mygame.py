import os
import platform

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = ".././SDL2/x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = ".././SDL2/x64"

from Framework import game_framework

from State import main_state

game_framework.run(main_state)