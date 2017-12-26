from pico2d import *

from Monster.monster_red import MonsterRed
from SourceFiles.stdafx import *


class MonsterBlue(MonsterRed):
    image = [0, 0]
    type = 'blue'

    dead_effect_img = None

    def __init__(self, x, y, width, height, x_limited, bg):
        self.exsist = True
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
        if self.dead_effect_img == None:
            self.dead_effect_img = load_image('Graphics\/monster\/dead_effect.png')
        # collide
        self.aabb = AABB(0, 0, 0, 0)
        self.big_aabb = AABB(0, 0, 0, 0)
        # dead
        self.attacked_effect = False
        self.being_attacked_time = 0
        self.dying_effect = False
        self.dying_time = 0
        self.original_height = self.height

    def image_load(self):
        self.image[self.LEFT] = load_image('Graphics\/Monster\/monster_blue_left.png')
        self.image[self.RIGHT] = load_image('Graphics\/Monster\/monster_blue_right.png')

    def update_aabb(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        w = round(self.width * 0.3)
        h = round(self.height * 0.3)
        self.aabb = AABB(sx - w, sy - h, sx + w, sy + h)

    def update(self, frame_time):
        if self.attacked_effect:
            self.being_attacked(frame_time)
        if self.dying_effect:
            self.dying(frame_time)
            return

        distance = self.WALK_SPEED_PPS * frame_time

        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.frame_cnt

        if self.state == self.LEFT:
            self.x -= distance
        else:
            self.x += distance

        if self.x > self.max_x or self.x < self.min_x:
            if self.state == self.LEFT:
                self.state = self.RIGHT
            else:
                self.state = self.LEFT
            self.x = clamp(self.min_x, self.x, self.max_x)

        self.update_aabb()

    def draw_bb(self):
        draw_rectangle(*self.aabb.get_bb())

