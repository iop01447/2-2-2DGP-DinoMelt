from pico2d import *
from stdafx import *
from monster_red import MonsterRed


class MonsterOrange(MonsterRed):
    IDLE, ATTACK = 0, 1
    image = [[0,0],[0,0]]
    bullet_image = None
    type = 'orange'

    def __init__(self, x, y, width, height, state, bg):
        self.width, self.height = width, height
        self.x, self.y = x + width//2, y + height//2
        self.bg = bg
        if state == 'left':
            self.state = [self.IDLE, self.LEFT]
        elif state == 'right':
            self.state = [self.IDLE, self.RIGHT]
        self.frame = 0
        self.total_frames = 0.0
        self.frame_cnt = 4
        self.life = 2
        # image
        if self.image == [[0,0],[0,0]]:
            self.image_load()
        if self.bullet_image == None:
            self.bullet_image = load_image('Graphics\/monster\/monster_bullet.png')
        # collide
        self.aabb = AABB(0, 0, 0, 0)
        self.big_aabb = AABB(0, 0, 0, 0)

    def image_load(self):
        self.image[self.IDLE][self.LEFT] = load_image(
            'Graphics\/monster\/monster_orange_idle_left.png')
        self.image[self.IDLE][self.RIGHT] = load_image(
            'Graphics\/monster\/monster_orange_idle_right.png')
        self.image[self.ATTACK][self.LEFT] = load_image(
            'Graphics\/monster\/monster_orange_attack_left.png')
        self.image[self.ATTACK][self.RIGHT] = load_image(
            'Graphics\/monster\/monster_orange_attack_right.png')

    def update_aabb(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        if self.state[1] == self.LEFT:
            sx += self.width//4
        else:
            sx -= self.width//4
        w = round(self.width * 0.2)
        h = round(self.height * 0.3)
        self.aabb = AABB(sx - w, sy - h, sx + w, sy + h)
        if self.state[1] == self.LEFT:
            self.big_aabb = AABB(sx - 500, sy - h, sx + w, sy + h)
        else:
            self.big_aabb = AABB(sx - w, sy - h, sx + 500, sy + h)

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.frame_cnt

        if not self.player == None and collide(self.player.aabb, self.big_aabb):
            self.state[0] = self.ATTACK
        else:
            self.state[0] = self.IDLE

        self.update_aabb()

    def draw(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom

        if self.state[0] == self.IDLE:
            self.frame_cnt = 4
            self.img_w = self.image[self.IDLE][self.LEFT].w // 4
            self.img_h = self.image[self.IDLE][self.LEFT].h

            self.image[self.state[0]][self.state[1]].clip_draw(
                self.frame * self.img_w, 0, self.img_w, self.img_h,
                sx, sy, self.width, self.height)

        elif self.state[0] == self.ATTACK:
            self.frame_cnt = 7
            self.img_col = 4
            self.img_w = self.image[self.ATTACK][self.LEFT].w // 4
            self.img_h = self.image[self.ATTACK][self.LEFT].h // 2

            col = self.frame % self.img_col
            row = self.frame // self.img_col

            self.image[self.state[0]][self.state[1]].clip_draw(
                col * self.img_w, self.img_h - row * self.img_h, self.img_w, self.img_h,
                sx, sy, self.width, self.height)
