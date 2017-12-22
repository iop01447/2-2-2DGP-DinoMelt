from pico2d import *
from stdafx import *
from monster_red import MonsterRed

class Monsterblue(MonsterRed):
    image = [0, 0]
    type = 'blue'

    def __init__(self, x, y, width, height, x_limited, bg):
        self.width, self.height = width, height
        self.min_x = x + self.width // 2
        self.max_x = x_limited - self.width // 2
        self.x, self.y = self.min_x, y + height//2
        self.bg = bg
        self.state = self.RIGHT
        self.frame = 0
        self.total_frames = 0.0
        self.frame_cnt = 8
        self.life = 1
        # image
        if self.image == [0, 0]:
            self.image_load()
        self.img_col = 4
        self.img_w = self.image[self.LEFT].w // 4
        self.img_h = self.image[self.LEFT].h // 2
        # collide
        self.aabb = AABB(0, 0, 0, 0)

    def image_load(self):
        self.image[self.LEFT] = load_image('Graphics\/monster\/monster_blue_left.png')
        self.image[self.RIGHT] = load_image('Graphics\/monster\/monster_blue_right.png')

