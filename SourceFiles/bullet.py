from pico2d import *

from SourceFiles.stdafx import *


class PlayerBullet:
    image = None

    PIXEL_PER_METER = (130.0 / 1.5)  # 130 pixel 1.5 m
    RUN_SPEED_KMPH = 20.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self):
        self.x, self.y = 0, 0
        self.width, self.height = 64,50
        self.aabb = AABB(0, 0, 0, 0)
        self.bg = None
        self.direction = 0
        if self.image == None:
            self.image = load_image('..\/Graphics\/Player\/bullet.png')

    def initialize(self, x, y, direction, bg):
        self.x, self.y = x, y
        self.direction = direction
        self.bg = bg

    def update_aabb(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        w = self.width//5
        h = self.height//5
        self.aabb = AABB(sx - w, sy - h, sx + w, sy + h)

    def update(self, frame_time):
        distance = self.RUN_SPEED_PPS * frame_time
        self.x += self.direction * distance
      #  self.y -= distance//3

        if not self.bg == None:
            self.update_aabb()

    def draw(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        self.image.draw(sx, sy)

    def draw_bb(self):
        draw_rectangle(*self.aabb.get_bb())


class MonsterBullet:
    image = None

    PIXEL_PER_METER = (130.0 / 1.5)  # 130 pixel 1.5 m
    RUN_SPEED_KMPH = 10.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self):
        self.x, self.y = 0, 0
        self.width, self.height = 64,50
        self.aabb = AABB(0, 0, 0, 0)
        self.bg = None
        self.direction = 0
        if self.image == None:
            self.image = load_image('..\/Graphics\/Monster\/monster_bullet.png')

    def initialize(self, x, y, direction, bg):
        self.x, self.y = x, y
        self.direction = direction
        self.bg = bg

    def update_aabb(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        w = self.width//5
        h = self.height//5
        self.aabb = AABB(sx - w, sy - h, sx + w, sy + h)

    def update(self, frame_time):
        distance = self.RUN_SPEED_PPS * frame_time
        self.x += self.direction * distance
      #  self.y -= distance//3

        if not self.bg == None:
            self.update_aabb()

    def draw(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        self.image.draw(sx, sy)

    def draw_bb(self):
        draw_rectangle(*self.aabb.get_bb())


class BossState_PlayerBullet:
    image = None

    PIXEL_PER_METER = (130.0 / 1.5)  # 130 pixel 1.5 m
    RUN_SPEED_KMPH = 20.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self):
        self.x, self.y = 0, 0
        self.width, self.height = 64,50
        self.aabb = AABB(0, 0, 0, 0)
        self.bg = None
        self.direction = 0
        if self.image == None:
            self.image = load_image('..\/Graphics\/Player\/bullet.png')

    def initialize(self, x, y, direction):
        self.x, self.y = x, y
        self.direction = direction

    def update_aabb(self):
        sx = self.x
        sy = self.y
        w = self.width//5
        h = self.height//5
        self.aabb = AABB(sx - w, sy - h, sx + w, sy + h)

    def update(self, frame_time):
        distance = self.RUN_SPEED_PPS * frame_time
        self.x += self.direction * distance
        self.update_aabb()

    def draw(self):
        sx = self.x
        sy = self.y
        self.image.draw(sx, sy)

    def draw_bb(self):
        draw_rectangle(*self.aabb.get_bb())

