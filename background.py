from pico2d import *

from tile import load_tile_map


class TileBackground:

    def __init__(self, width, height):
        self.tile_map = load_tile_map('map.json', 'tileset.json')
        self.image = load_image('Graphics\map.png')
        self.speed = 0
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
    #    self.width = width      # in tiles
    #    self.height = height    # in tiles
        self.w = self.image.w
        self.h = self.image.h


    def set_center_object(self, player):
        self.center_object = player


    def draw(self):
        self.image.clip_draw_to_origin(
            self.window_left, self.window_bottom,
            self.canvas_width, self.canvas_height, 0, 0
        )


    def update(self, frame_time):
        self.window_left = clamp(
            0, int(self.center_object.x) - self.canvas_width // 2,
               self.w - self.canvas_width
        )
        self.window_bottom = clamp(
            0, int(self.center_object.y) - self.canvas_height // 2,
               self.h - self.canvas_height
        )


    def handle_event(self, event):
        pass



