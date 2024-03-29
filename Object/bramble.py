from pico2d import *
from SourceFiles.stdafx import *


class Bramble:
    # frame speed
    TIME_PER_ACTION = 0.1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 1

    image = None

    player = None

    def __init__(self, x, y, width, height, bg):
        self.width, self.height = width, height
        self.x, self.y = x + width//2, y + width//2
        self.bg = bg
        self.frame = 0
        self.total_frames = 0.0
        self.frame_cnt = 3
        # image
        if self.image == None:
            self.image_load()
        self.img_w = self.image.w//self.frame_cnt
        self.img_h = self.image.h
        # collide
        self.aabb = AABB(0,0,0,0)

    def set_player(self, player):
        if self.player == None:
            self.player = player

    def image_load(self):
        self.image = load_image('Graphics\/bramble.png')

    def update_aabb(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        w = round(self.width * 0.4)
        h = round(self.height * 0.4)
        self.aabb = AABB(sx - w, sy - h, sx + w, sy + h)

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.frame_cnt
        self.update_aabb()

    def draw(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom

        self.image.clip_draw(
            self.frame * self.img_w, 0, self.img_w, self.img_h,
            sx, sy, self.width, self.height)

    def draw_bb(self):
        draw_rectangle(*self.aabb.get_bb())