from pico2d import *


class Tile:
    tile_width = 130 // 2
    tile_height = 130 // 2
    tile_map_image_h = 3640

    def __init__(self, line, row, value):
        self.line = line
        self.row = row
        self.value = value
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.window_left = 0
        self.window_bottom = 0
        self.line = 56 - self.line - 1


    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def get_bb(self):
        min_x, min_y = self.row * self.tile_width, self.line * self.tile_height
        max_x, max_y = (self.row + 1) * self.tile_width, (self.line + 1) * self.tile_height
        min_x -= self.window_left
        max_x -= self.window_left
        min_y = self.tile_map_image_h - self.window_bottom - min_y
        max_y = self.tile_map_image_h - self.window_bottom - max_y
        min_y, max_y = max_y, min_y

        if self.value in range(2, 7):
            pass
        else:
            max_y -= Tile.tile_height//2

        return min_x, min_y, max_x, max_y


    def update(self, window_left, window_bottom):
        self.window_left = window_left
        self.window_bottom = window_bottom