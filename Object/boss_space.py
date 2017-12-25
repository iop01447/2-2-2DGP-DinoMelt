from pico2d import *

from SourceFiles.stdafx import *
from State import boss_state
from Framework import game_framework

class BossSpace:
    player = None

    def __init__(self, x, y, width, height, bg):
        self.width, self.height = width, height
        self.x, self.y = x + width//2, y + height//2
        self.bg = bg
        # collide
        self.aabb = AABB(0,0,0,0)

    def set_player(self, player):
        if self.player == None:
            self.player = player

    def update_aabb(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        w = round(self.width * 0.5)
        h = round(self.height * 0.5)
        self.aabb = AABB(sx - w, sy - h, sx + w, sy + h)

    def update(self, frame_time):
        self.update_aabb()
        self.player_collide_check()

    def player_collide_check(self):
        if self.player == None: return
        if collide(self.player.aabb, self.aabb):
           game_framework.push_state(boss_state)

    def draw(self):
        pass

    def draw_bb(self):
        draw_rectangle(*self.aabb.get_bb())