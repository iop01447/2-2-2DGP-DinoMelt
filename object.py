from pico2d import *
from stdafx import *
from monster_red import MonsterRed
from monster_blue import Monsterblue
from monster_orange import MonsterOrange
from clay_orb import ClayOrb

class Object:
    def __init__(self, x, y, width, height, type, x_limited, state, bg):
        self.type = type

        if type == 'red':
            self.object = MonsterRed(x, y, width, height, x_limited, bg)
        elif type == 'blue':
            self.object = Monsterblue(x, y, width, height, x_limited, bg)
        elif type == 'orange':
            self.object = MonsterOrange(x, y, width, height, state, bg)
        elif type == 'orb':
            self.object = ClayOrb(x, y, width, height, bg)

    def update(self, frame_time):
        self.object.update(frame_time)

    def draw(self):
        self.object.draw()

    def draw_bb(self):
        self.object.draw_bb()

    def get_bb(self):
        return self.object.aabb.get_bb()

    def set_player(self, player):
        if self.type in ('red', 'blue', 'orange',):
            self.object.set_player(player)