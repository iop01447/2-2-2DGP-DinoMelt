from pico2d import *
from stdafx import *

class Object:
    image = {'orb':None, 'monster':{'blue':{'left':None, 'right':None},
                                       'red':{'left':None, 'right':None},
                                       'orange':{'idle':{'left':None, 'right':None},
                                                 'attack':{'left':None, 'right':None}}}}

    def __init__(self, x, y, width, height, type, x_limited):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.type = type
        self.x_limited = x_limited
        self.window_left = 0
        self.window_bottom = 0
        self.frame = 0

        Object.image['orb'] = load_image('Graphics\/clay_orb.png')
        Object.image['monster']['blue']['left'] = load_image('Graphics\/monster\/monster_blue_left.png')
        Object.image['monster']['blue']['right'] = load_image('Graphics\/monster\/monster_blue_right.png')
        Object.image['monster']['red']['left'] = load_image('Graphics\/monster\/monster_red_left.png')
        Object.image['monster']['red']['right'] = load_image('Graphics\/monster\/monster_red_right.png')
        Object.image['monster']['orange']['idle']['left'] = load_image('Graphics\/monster\/monster_orange_idle_left.png')
        Object.image['monster']['orange']['idle']['right'] = load_image('Graphics\/monster\/monster_orange_idle_right.png')
        Object.image['monster']['orange']['attack']['left'] = load_image('Graphics\/monster\/monster_orange_attack_left.png')
        Object.image['monster']['orange']['attack']['left'] = load_image('Graphics\/monster\/monster_orange_attack_right.png')
        pass

    def update(self, frame_time):
        pass

    def draw(self, window_left, window_bottom):
        self.window_left = window_left
        self.window_bottom = window_bottom

        sx = self.x - window_left
        sy = self.y - window_bottom

        if self.type in ('blue', ):
            self.image['monster'][self.type]['left'].clip_draw(self.frame * self.width*2, 0, 292, 188, sx, sy, self.width, self.height)

        pass

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx = self.x - self.window_left
        sy = self.y - self.window_bottom
        return sx, sy, sx + self.width, sy + self.height
      # return self.x, self.y, self.x + self.width, self.y + self.height