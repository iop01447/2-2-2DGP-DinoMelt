from pico2d import *

from SourceFiles.stdafx import *
from Framework import game_framework
from State import boss_state
from State import main_state

class Boss:
    LEFT, RIGHT = 0, 1
    JUMP_MODE, SLIDE_MODE = 0, 1

    # run speed
    PIXEL_PER_METER = (130.0 / 1.5)  # 130 pixel 1.5 m
    WALK_SPEED_KMPH = 5.0  # Km / Hour
    WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
    WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
    WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)
    RUN_SPEED_PPS = WALK_SPEED_PPS * 2

    # frame speed
    TIME_PER_ACTION = 0.1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 1

    image = [0,0]
    dead_effect_img = None

    def __init__(self):
        # image
        self.frame = 0
        self.total_frames = 0.0
        self.frame_cnt = 5
        if self.image == [0,0]:
            self.image_load()
        if self.dead_effect_img == None:
            self.dead_effect_img = load_image('..\/Graphics\/monster\/dead_effect.png')
        self.img_w = self.image[self.LEFT].w//self.frame_cnt
        self.img_h = self.image[self.LEFT].h

        # state
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.min_x = 130 + self.img_w//2
        self.max_x = self.canvas_width - 130 - self.img_w//2
        self.min_y = 130 + self.img_h//2
        # self.max_y = self.canvas_height - self.img_h//2
        self.x, self.y = self.canvas_width//2, self.min_y
        self.state = self.RIGHT
        self.life = 50
        self.pattern = self.JUMP_MODE
        self.width, self.height = self.img_w, self.img_h

        # collide
        self.aabb = AABB(0,0,0,0)
        self.big_aabb = AABB(0,0,0,0)

        # attacked and dead
        self.attacked_effect = False
        self.being_attacked_time = 0
        self.dying_effect = False
        self.dying_time = 0
        self.original_height = self.height

    def image_load(self):
        self.image[self.LEFT] = load_image('..\/Graphics\/Monster\/boss_left.png')
        self.image[self.RIGHT] = load_image('..\/Graphics\/Monster\/boss_right.png')

    def update_aabb(self):
        w = round(self.img_w * 0.1)
        h = round(self.img_h * 0.2)
        self.aabb = AABB(self.x - w, self.y - h*2, self.x + w, self.y)

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

    def draw(self):
        self.image[self.state].clip_draw(
            self.frame * self.img_w, 0, self.img_w, self.img_h,
            self.x, self.y, self.width, self.height)

        if self.attacked_effect:
            self.dead_effect_img.draw(self.x, self.y, self.width, self.height)

    def draw_bb(self):
        draw_rectangle(*self.aabb.get_bb())

    def be_attacked(self):
        self.being_attacked_time = 0
        self.life -= 1
        if self.life <= 0:
            self.dying_effect = True
            self.attacked_effect = False
            return
        self.attacked_effect = True

    def being_attacked(self, frame_time):
        self.being_attacked_time += frame_time

        if self.being_attacked_time > 1:
            self.being_attacked_time = 0
            self.attacked_effect = False

    def dying(self, frame_time):
        self.dying_time += frame_time
        self.height = self.original_height * (1 - self.dying_time) + 0 * self.dying_time

        if self.height <= 1:
            self.height = self.original_height
            self.dying_time = 0
            self.dying_effect = False
            main_state.player.boss_clear = True
            boss_state.is_pop_state = True
            print('boss die')

