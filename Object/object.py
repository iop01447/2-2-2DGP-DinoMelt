from Monster.monster_red import MonsterRed
from Monster.monster_orange import MonsterOrange
from Monster.monster_blue import MonsterBlue
from Object.clay_orb import ClayOrb


class Object:
    def __init__(self, x, y, width, height, type, x_limited, state, bg):
        self.type = type

        if type == 'red':
            self.object = MonsterRed(x, y, width, height, x_limited, bg)
        elif type == 'blue':
            self.object = MonsterBlue(x, y, width, height, x_limited, bg)
        elif type == 'orange':
            self.object = MonsterOrange(x, y, width, height, state, bg)
        elif type == 'orb':
            self.object = ClayOrb(x, y, width, height, bg)

    def update(self, frame_time):
        if not self.object.exsist: return
        self.object.update(frame_time)

    def draw(self):
        if not self.object.exsist: return
        self.object.draw()

    def draw_bb(self):
        if not self.object.exsist: return
        self.object.draw_bb()

    def get_bb(self):
        return self.object.aabb.get_bb()

    def set_player(self, player):
        if self.type in ('red', 'blue', 'orange',):
            self.object.set_player(player)