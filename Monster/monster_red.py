from pico2d import *

from SourceFiles.stdafx import *


class MonsterRed:
    LEFT, RIGHT = 0, 1
    type = 'red'

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

    player = None

    def __init__(self, x, y, width, height, x_limited, bg):
        self.exsist = True
        self.width, self.height = width, height
        self.min_x = x + self.width//2
        self.max_x = x_limited - self.width//2
        self.x, self.y = self.min_x, y + height//2
        self.bg = bg
        self.state = self.RIGHT
        self.frame = 0
        self.total_frames = 0.0
        self.frame_cnt = 8
        self.life = 2
        # image
        if self.image == [0,0]:
            self.image_load()
        if self.dead_effect_img == None:
            self.dead_effect_img = load_image('..\/Graphics\/monster\/dead_effect.png')
        self.img_col = 4
        self.img_w = self.image[self.LEFT].w//4
        self.img_h = self.image[self.LEFT].h//2
        # collide
        self.aabb = AABB(0,0,0,0)
        self.big_aabb = AABB(0,0,0,0)
        # dead
        self.attacked_effect = False
        self.being_attacked_time = 0
        self.dying_effect = False
        self.dying_time = 0
        self.original_height = self.height

    def set_player(self, player):
        if self.player == None:
            self.player = player

    def image_load(self):
        self.image[self.LEFT] = load_image('..\/Graphics\/Monster\/monster_red_left.png')
        self.image[self.RIGHT] = load_image('..\/Graphics\/Monster\/monster_red_right.png')

    def update_aabb(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        w = round(self.width * 0.3)
        h = round(self.height * 0.3)
        self.aabb = AABB(sx - w, sy - h, sx + w, sy + h)
        self.big_aabb = AABB(sx - 300, sy - h, sx + 300, sy + h)

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

        if not self.player == None and collide(self.player.aabb, self.big_aabb):
            if self.player.x < self.x:
                self.state = self.LEFT
                self.x -= distance*1.5
            else:
                self.state = self.RIGHT
                self.x += distance*1.5

        self.update_aabb()

    def draw(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        col = self.frame % self.img_col
        row = self.frame // self.img_col

        self.image[self.state].clip_draw(
            col * self.img_w, (1 - row) * self.img_h, self.img_w, self.img_h,
            sx, sy, self.width, self.height)

        if self.attacked_effect:
            self.dead_effect_img.draw(sx, sy)

    def draw_bb(self):
        draw_rectangle(*self.aabb.get_bb())
        draw_rectangle(*self.big_aabb.get_bb())

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
            self.die()

    def die(self):
        self.exsist = False


