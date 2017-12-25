from Monster.monster_red import MonsterRed
from Monster.monster_orange import MonsterOrange
from Monster.monster_blue import MonsterBlue
from Object.clay_orb import ClayOrb
from Object.bramble import Bramble
from Object.green_light import GreenLight
from Object.blue_light import BlueLight


class Object:
    def __init__(self, x, y, width, height, type, x_limited, state, name, bg):
        self.type = type
        self.object = None

        if type == 'red':
            self.object = MonsterRed(x, y, width, height, x_limited, bg)
        elif type == 'blue':
            self.object = MonsterBlue(x, y, width, height, x_limited, bg)
        elif type == 'orange':
            self.object = MonsterOrange(x, y, width, height, state, bg)
        elif type == 'orb':
            self.object = ClayOrb(x, y, width, height, bg)
        elif type == 'bramble':
            self.object = Bramble(x, y, width, height, bg)
        elif type == 'green_light':
            self.object = GreenLight(x, y, width, height, bg)
        elif type == 'blue_light':
            self.object = BlueLight(x, y, width, height, bg, name)

    def update(self, frame_time):
        if self.type in ('orb', 'red', 'blue', 'orange',):
            if not self.object.exsist: return
        self.object.update(frame_time)

    def draw(self):
        if self.type in ('orb', 'red', 'blue', 'orange',):
            if not self.object.exsist: return
        self.object.draw()

    def draw_bb(self):
        if self.type in ('orb', 'red', 'blue', 'orange',):
            if not self.object.exsist: return
            if self.type != 'orb' and self.object.dying_effect : return
        self.object.draw_bb()

    def get_bb(self):
        return self.object.aabb.get_bb()

    def set_player(self, player):
        if self.type in ('red', 'blue', 'orange', 'orb', ):
            self.object.set_player(player)