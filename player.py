import random

from pico2d import *


class Player():
    PIXEL_PER_METER = (130.0 / 0.3)  # 130 pixel 30 cm
    RUN_SPEED_KMPH = 15.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    TIME_PER_ACTION = 0.2
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 1

    image = {}

    LEFT_IDLE, RIGHT_IDLE, LEFT_RUN, RIGHT_RUN\
        = 0, 1, 2, 3


    def __init__(self):
        self.x, self.y = 100, 100
        self.width, self.height = 1255//9, 90
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()

        self.frame = 0
        self.life_time = 0.0
        self.total_frames = 0.0

        self.xdir = 0
        self.state = self.RIGHT_IDLE
        self.jump_active = False

        # 1255 * 90
        Player.image[self.LEFT_IDLE] = load_image('Graphics\idle\idle_left.png')
        Player.image[self.RIGHT_IDLE] = load_image('Graphics\idle\idle_right.png')
        Player.image[self.LEFT_RUN] = Player.image[self.LEFT_IDLE]
        Player.image[self.RIGHT_RUN] = Player.image[self.RIGHT_IDLE]


    def set_background(self, bg):
        self.bg = bg


    def update(self, frame_time):
        self.life_time += frame_time

        distance = Player.RUN_SPEED_PPS * frame_time

        self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 9

        self.x += (self.xdir * distance)
        if self.jump_active: self.y += distance//2
        self.x = clamp(0, self.x, self.bg.w)
        self.y = clamp(0, self.y, self.bg.h)


    def draw(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        Player.image[self.state].clip_draw(
            self.frame * self.width, 0, self.width, self.height, sx, sy)
        debug_print('x=%d, y=%d, sx=%d, sy=%d' % (self.x, self.y, sx, sy))


    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def get_bb(self):
        return self.x - self.width//2, self.y - self.height//2,\
               self.x + self.width//2, self.y + self.height//2


    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT: self.xdir += -1
            elif event.key == SDLK_RIGHT: self.xdir += 1

        if event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT: self.xdir += 1
            elif event.key == SDLK_RIGHT: self.xdir += -1

        if self.xdir == -1:
            self.state = self.LEFT_RUN
        elif self.xdir == 1:
            self.state = self.RIGHT_RUN
        elif self.xdir == 0:
            if self.state == self.RIGHT_RUN:
                self.state = self.RIGHT_IDLE
            elif self.state == self.LEFT_RUN:
                self.state = self.LEFT_IDLE