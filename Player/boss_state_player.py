from Player.player import Player
from SourceFiles.stdafx import *
from State import boss_state
from pico2d import *
from SourceFiles.bullet import BossState_PlayerBullet as Bullet
from Framework import game_framework
from State import boss_state
from State import main_state


class BossState_Player(Player):
    map_aabb = AABB(0,0,0,0)
    boss = None

    def initialize(self):
        self.x = self.canvas_width//2
        self.y = self.canvas_height
        self.map_aabb = AABB(130, 130, self.canvas_width - 130, self.canvas_height)
        self.bullet = Bullet()
        self.width, self.height = 0, 0

    def set_boss(self, boss):
        self.boss = boss

    def tile_map_collide_check(self):
        # self.x = clamp(130 + 25, self.x, self.canvas_width - 130 - 25)
        # self.y = clamp(130 + 30, self.y, self.canvas_height - 30)
        if self.x < self.map_aabb.min_x + 25: return True
        elif self.x > self.map_aabb.max_x - 25: return True
        elif self.y < self.map_aabb.min_y + 30: return True
        elif self.y > self.map_aabb.max_y - 20: return True
        return False

    def bullet_tile_map_collide_check(self):
        if self.bullet.x < self.map_aabb.min_x: return True
        elif self.bullet.x > self.map_aabb.max_x: return True
        return False

    def monster_collide_check(self):
        return collide(self.aabb, self.boss.aabb)

    def bullet_monster_collide_check(self):
        return collide(self.bullet.aabb, self.boss.aabb)

    def update_aabb(self):
        sx = self.x
        sy = self.y
        self.aabb = AABB(sx - 25, sy- 30, sx + 25, sy + 20)

    def update(self, frame_time):
        if self.dying_effect:
            self.dying(frame_time)
            return

        self.update_image_date() # 애니메이션 데이터

        distance = Player.RUN_SPEED_PPS * frame_time

        self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.frame_cnt

        # 점프
        if self.jump_active:
            if self.jump_state == 'jumped' and int(self.total_frames) > self.frame_cnt:
                self.jump_active = False
                self.walk_sound.play()
            self.jump(frame_time)

        # 이동
        if not self.state == 'idle':
            self.x += self.direction * distance

        # 중력
        if not self.jump_active:
            self.y -= distance

        # 공격
        if self.bullet_active:
            self.bullet.update(frame_time)
            if self.bullet_tile_map_collide_check():
                self.attack_sound.play()
                self.bullet_active = False
            if self.bullet_monster_collide_check():
                self.attack_sound.play()
                self.bullet_active = False
                self.boss.be_attacked()
        if self.attack_active:
            if int(self.total_frames) ==  self.frame_cnt:
                self.attack_active = False

        # 몬스터와 부딪힐 때
        if self.monster_collide_check():
            if not self.attacked_effect:
                print('player dead')
                self.life -= 1
                self.attacked_effect = True
                self.attacked_sound.play()
            if self.life < 1:
                if self.unbeatable: self.life = 1
                else:
                    boss_state.bgm.pause()
                    self.dead_sound.play()
                    self.attacked_effect = False
                    self.dying_effect = True
                    self.original_height = self.height

        if self.attacked_effect:
            self.being_attacked(frame_time)

        self.x = clamp(130+25, self.x, self.canvas_width-130-25)
        self.y = clamp(130+30, self.y, self.canvas_height-30)

        self.update_aabb()

    # effect
    def attack_initialize(self):
        self.total_frames = 0
        self.bullet_active = True
        self.bullet.initialize(self.x, self.y, self.direction)

    def dying(self, frame_time):
        self.dying_time += frame_time
        t = self.dying_time / 2.4
        self.height = self.original_height * (1 - t) + 0 * t
        self.height = int(self.height)

        if self.height <= 2.4:
            self.height = self.original_height
            self.dying_time = 0
            self.dying_effect = False
            self.new_life_sound.play()
            self.life = 3
            boss_state.is_pop_state = True

    def draw(self):
        self.draw_ui()

        sx = self.x
        sy = self.y
        state = self.state

        if self.jump_active:
            state = self.jump_state
        if self.attack_active:
            state = 'attack'

            #  debug_print('State = %s, direction = %d, frame = %d, width = %d' % (State, self.direction, self.frame, self.width))
            #  print(State, self.direction, self.width, self.height, sx, sy)
        if self.dying_effect:
            Player.image[state][self.direction].clip_draw(
                self.frame * self.width, 0, self.width, self.original_height, sx, sy, self.width, self.height)
        else:
            Player.image[state][self.direction].clip_draw(
                self.frame * self.width, 0, self.width, self.height, sx, sy)

        if self.bullet_active:
            self.bullet.draw()

    def draw_ui(self):
        if self.unbeatable:
            self.draw_unbeatable()
        self.draw_life()