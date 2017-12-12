import random

from pico2d import *
from stdafx import *


class Player:
    PIXEL_PER_METER = (130.0 / 1.5)  # 130 pixel 1.5 m
    RUN_SPEED_KMPH = 15.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    print("RUN_SPEED_PPS: %f" % RUN_SPEED_PPS)
    TIME_PER_ACTION = 0.1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 1

    image = {}
    life_image = []

    LEFT, RIGHT = -1, 1
    JUMPING_UP, JUMPING_DOWN, JUMPED = 0, 1, 2

    def __init__(self):
        self.x, self.y = 100, 3300
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()

        self.frame = 0
        self.life_time = 0.0
        self.total_frames = 0.0

        self.state = 'idle' # idle, walk
        self.direction = self.RIGHT

        self.button = {'left': False, 'right': False}
        self.attack_active = False

        self.life = 3

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
        self.double_jump = False
        self.jump_direction = self.JUMPING_UP
        self.jump_state = 'jump' # jump, jumping, jumped

        # collide
        self.collide_object = []
        self.x_change = '0'
        self.y_change = '0'

    def set_background(self, bg):
        self.bg = bg

    def background_collide_check(self):
        for tile in self.bg.tiles:
            if collide(self, tile) and tile.value != 0:
                min_x, min_y, max_x, max_y = tile.get_bb()
                # if self.x_change == '+': self.x = min_x + self.bg.window_left - 30
                # elif self.x_change == '-': self.x = max_x + self.bg.window_left + 30
                # if self.y_change == '+': self.y = min_y + self.bg.window_bottom - 30
                # elif self.y_change == '-': self.y = max_y + self.bg.window_bottom + 30
                return True
        return False

    def jump_initialize(self):
        self.jump_direction = self.JUMPING_UP
        self.jump_state = 'jump'
        self.total_frames = 0
        if not self.double_jump:
            self.y_base = self.y

    def jump(self, distance):
        y = self.y
        if self.jump_direction == self.JUMPING_UP:
            self.y += distance*0.7
            if int(self.total_frames) >= self.frame_cnt:
                self.jump_state = 'jumping'
            if (not self.double_jump and self.y >= self.y_base + self.height)\
                    or (self.double_jump and self.y >= self.y_base + self.height * 1.5):
                self.jump_direction = self.JUMPING_DOWN

        elif self.jump_direction == self.JUMPING_DOWN:
            self.y -= distance
            if self.y <= self.y_base:
                self.jump_direction = self.JUMPED
                self.jump_state = 'jumped'
                self.total_frames = 0

        elif self.jump_direction == self.JUMPED:
            pass

        if self.background_collide_check():
           self.y = y
           self.jump_direction = self.JUMPED
           self.jump_state = 'jumped'
           self.total_frames = 0

    def update_image_date(self):
        state = self.state
        if self.jump_active:
            state = self.jump_state

        self.frame_cnt = self.data[state]['image']['frame_cnt']
        self.width = self.data[state]['image']['width'] // self.frame_cnt
        self.height = self.data[state]['image']['height']

    def update(self, frame_time):
        x, y = self.x, self.y

        self.update_image_date() # 애니메이션 데이터

        self.life_time += frame_time

        distance = Player.RUN_SPEED_PPS * frame_time

        self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.frame_cnt

        # 점프
        if self.jump_active:
            if not self.state == 'idle':
                self.x += (self.direction * distance*0.7)
                if self.background_collide_check():
                    self.x -= (self.direction * distance*0.7)
            if self.jump_state == 'jumped' and int(self.total_frames) > self.frame_cnt:
                self.jump_active = False
                self.double_jump = False
            self.jump(distance)
        # 그냥 이동
        elif not self.state == 'idle':
            self.x += (self.direction * distance)
            if self.background_collide_check():
                self.x -= (self.direction * distance)

        # 중력
        if not self.jump_active:
            self.y -= distance
            if self.background_collide_check():
                self.y += distance

        # collide check
        # if x == self.x:
        #     self.x_change = '0'
        # elif x < self.x:
        #     self.x_change = '+'
        # else:
        #     self.x_change = '-'
        # if y == self.y:
        #     self.y_change = '0'
        # elif y < self.y:
        #     self.y_change = '+'
        # else:
        #     self.y_change = '-'

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
        debug_print('x=%d, y=%d, sx=%d, sy=%d' % (self.x, self.y, sx, sy))
        #print('state = %s, frame = %d, frame_cnt = %d, width = %d, height = %d, data_widht = %d'
        #      % (state, self.frame, self.frame_cnt, self.width, self.height, self.data[state]['image']['width']))

    def life_draw(self):
        # 362 131
        Player.life_image[self.life - 1].draw(self.canvas_width/2, self.canvas_height - 50, 145, 52)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        return sx - 25, sy - 30, sx + 25, sy + 30

    def handle_event(self, event):

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT: self.button['left'] = True
            elif event.key == SDLK_RIGHT: self.button['right'] = True
            elif event.key == SDLK_a:
                if not self.jump_active:
                    self.jump_active = True
                    self.jump_initialize()
                elif not self.double_jump:
                    self.double_jump = True
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