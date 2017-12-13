import random

from pico2d import *
from stdafx import *
import math

class Player:
    # run speed
    PIXEL_PER_METER = (130.0 / 1.5)  # 130 pixel 1.5 m
    RUN_SPEED_KMPH = 15.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    # frame speed
    TIME_PER_ACTION = 0.1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 1

    # image
    image = {}
    life_image = []

    # enum
    LEFT, RIGHT = -1, 1
    JUMPING_UP, JUMPING_DOWN, JUMPED = 0, 1, 2
    gravity = 9.8

    def __init__(self):
        # init
        self.x, self.y = 100, 3250
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.life = 3

        # frame
        self.frame = 0
        self.total_frames = 0.0

        # state
        self.state = 'idle' # idle, walk
        self.direction = self.RIGHT
        self.button = {'left': False, 'right': False}
        self.attack_active = False

        # image
        with open("data.json") as f:
            self.data = json.load(f)
        self.data = self.data['player']

        if not Player.image:
            Player.image['idle'] = {self.LEFT: load_image(self.data['idle']['image']['left']),
                                    self.RIGHT: load_image(self.data['idle']['image']['right'])}
            Player.image['walk'] = {self.LEFT: load_image(self.data['walk']['image']['left']),
                                    self.RIGHT: load_image(self.data['walk']['image']['right'])}
            Player.image['jump'] = {self.LEFT: load_image(self.data['jump']['image']['left']),
                                    self.RIGHT: load_image(self.data['jump']['image']['right'])}
            Player.image['jumping'] = {self.LEFT: load_image(self.data['jumping']['image']['left']),
                                    self.RIGHT: load_image(self.data['jumping']['image']['right'])}
            Player.image['jumped'] = {self.LEFT: load_image(self.data['jumped']['image']['left']),
                                    self.RIGHT: load_image(self.data['jumped']['image']['right'])}

        if not Player.life_image:
            Player.life_image.append(load_image('Graphics\/life_level1.png'))
            Player.life_image.append(load_image('Graphics\/life_level2.png'))
            Player.life_image.append(load_image('Graphics\/life_level3.png'))

        # jump
        self.jump_active = False
        self.jump_direction = self.JUMPING_UP
        self.jump_state = 'jump' # jump, jumping, jumped (image)

        # collide
        self.aabb = AABB(self.x - 25, self.y - 30, self.x + 25, self.y + 10)

    def set_background(self, bg):
        self.bg = bg

    def background_collide_check(self):
        self.update_aabb()
        return self.bg.tile_map.collide_check(self.bg.window_left, self.bg.window_bottom,
                                            self.canvas_width, self.canvas_height, self)

    def jump_initialize(self):
        self.jump_direction = self.JUMPING_UP
        self.jump_state = 'jump'
        self.total_frames = 0
        self.y_base = self.y
        # jump with gravity
        self.a0 = -500
        self.v0 = 400
        self.y0 = self.y
        self.jump_time = 0.0

    def jump(self, frame_time):
        # jump with gravity
        self.jump_time = frame_time
        self.a1 = self.a0 - self.gravity
        self.a0 = self.a1
        self.v1 = self.v0 + self.a1 * self.jump_time
        height = (self.v0 + self.v1) / 2 * self.jump_time
        self.v0 = self.v1
        self.y0 = self.y

        if self.jump_direction == self.JUMPING_UP:
            self.y = self.y0 + height
            if int(self.total_frames) >= self.frame_cnt:
                self.jump_state = 'jumping'
            if self.y >= self.y_base + self.height * 1.2:
                self.jump_direction = self.JUMPING_DOWN
            if self.background_collide_check():
                self.y -= height
                self.jump_state = 'jumping'
                self.jump_direction = self.JUMPING_DOWN

        elif self.jump_direction == self.JUMPING_DOWN:
            self.y = self.y0 + height
            if self.background_collide_check():
                self.y -= height
                self.jump_direction = self.JUMPED
                self.jump_state = 'jumped'
                self.total_frames = 0

        elif self.jump_direction == self.JUMPED:
            pass

    def update_image_date(self):
        state = self.state
        if self.jump_active:
            state = self.jump_state

        self.frame_cnt = self.data[state]['image']['frame_cnt']
        self.width = self.data[state]['image']['width'] // self.frame_cnt
        self.height = self.data[state]['image']['height']

    def update_aabb(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        self.aabb = AABB(sx - 25, sy- 30, sx + 25, sy + 10)

    def update(self, frame_time):
        self.update_image_date() # 애니메이션 데이터

        distance = Player.RUN_SPEED_PPS * frame_time

        self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.frame_cnt

        # 점프
        if self.jump_active:
            if self.jump_state == 'jumped' and int(self.total_frames) > self.frame_cnt:
                self.jump_active = False
            self.jump(frame_time)

        # 이동
        if not self.state == 'idle':
            self.x += self.direction * distance
            if self.background_collide_check():
                self.x -= self.direction * distance

        # 중력
        if not self.jump_active:
            self.y -= distance
            if self.background_collide_check():
                self.y += distance

        self.x = clamp(0, self.x, self.bg.w)
        self.y = clamp(0, self.y, self.bg.h)

    def draw(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        state = self.state

        if self.jump_active:
            state = self.jump_state

        Player.image[state][self.direction].clip_draw(
            self.frame * self.width, 0, self.width, self.height, sx, sy)
        #debug_print('x=%d, y=%d, sx=%d, sy=%d' % (self.x, self.y, sx, sy))

    def draw_life(self):
        # 362 x 131
        Player.life_image[self.life - 1].draw(self.canvas_width/2, self.canvas_height - 50, 145, 52)

    def draw_bb(self):
        draw_rectangle(*self.aabb.get_bb())

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT: self.button['left'] = True
            elif event.key == SDLK_RIGHT: self.button['right'] = True
            elif event.key == SDLK_a:
                if not self.jump_active:
                    self.jump_active = True
                    self.jump_initialize()
            elif event.key == SDLK_s: pass

        if event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT: self.button['left'] = False
            elif event.key == SDLK_RIGHT: self.button['right'] = False

        if (self.button['left'] and self.button['right']) or (not self.button['left'] and not self.button['right']):
           self.state = 'idle'
        elif self.button['left']:
            self.state = 'walk'
            self.direction = self.LEFT
        elif self.button['right']:
            self.state = 'walk'
            self.direction = self.RIGHT