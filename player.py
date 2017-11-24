import random

from pico2d import *


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

    LEFT, RIGHT = -1, 1
    JUMPING_UP, JUMPING_DOWN, JUMPED = 0, 1, 2

    def __init__(self):
        self.x, self.y = 100, 3000
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()

        self.frame = 0
        self.life_time = 0.0
        self.total_frames = 0.0

        self.state = 'idle' # idle, walk
        self.direction = self.RIGHT

        self.button = {'left': False, 'right': False}
        self.jump_active = False
        self.attack_active = False

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

        # jump
        self.double_jump = False
        self.jump_direction = self.JUMPING_UP
        self.jump_state = 'jump' # jump, jumping, jumped


    def set_background(self, bg):
        self.bg = bg


    def initialize_jump(self):
        self.jump_direction = self.JUMPING_UP
        self.jump_state = 'jump'
        self.total_frames = 0
        if not self.double_jump:
            self.y_base = self.y


    def jump(self, distance):
        if self.jump_direction == self.JUMPING_UP:
            self.y += distance*0.7
            if int(self.total_frames) >= self.frame_cnt:
                self.jump_state = 'jumping'
            if (not self.double_jump and self.y >= self.y_base + self.height)\
                    or (self.double_jump and self.y >= self.y_base + self.height * 2):
                self.jump_direction = self.JUMPING_DOWN

        elif self.jump_direction == self.JUMPING_DOWN:
            self.y -= distance*0.7
            if self.y <= self.y_base:
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


    def update(self, frame_time):
        self.update_image_date()

        self.life_time += frame_time

        distance = Player.RUN_SPEED_PPS * frame_time

        self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.frame_cnt

        if self.jump_active:
            if not self.state == 'idle':
                self.x += (self.direction * distance*0.7)
            if self.jump_state == 'jumped' and int(self.total_frames) > self.frame_cnt:
                self.jump_active = False
                self.double_jump = False
            self.jump(distance)
        elif not self.state == 'idle':
            self.x += (self.direction * distance)

        self.x = clamp(0, self.x, self.bg.w)
        self.y = clamp(0, self.y, self.bg.h)

        self.update_image_date()


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


    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def get_bb(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        return sx - 30, sy - 30, sx + 30, sy + 30


    def handle_event(self, event):

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT: self.button['left'] = True
            elif event.key == SDLK_RIGHT: self.button['right'] = True
            elif event.key == SDLK_UP: pass
            elif event.key == SDLK_a:
                if not self.jump_active:
                    self.jump_active = True
                    self.initialize_jump()
                elif not self.double_jump:
                    self.double_jump = True
                    self.initialize_jump()
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