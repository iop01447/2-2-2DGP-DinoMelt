from pico2d import *

class Player():
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    TIME_PER_ACTION = 0.2
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 9

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.idle_left_image = load_image('Graphics\idle\idle_left.png')
        self.idle_right_image = load_image('Graphics\idle\idle_right.png')
        self.frame = 0
        self.total_frames = 0

    def update(self, frame_time):
       # self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time
        self.total_frames += Player.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 9

    def draw(self):
        self.idle_right_image.clip_draw(self.frame * 140, 0, 280//2, 180//2, 100, 150)