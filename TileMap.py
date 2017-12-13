__author__ = 'dustinlee'

import json

from pico2d import *


from TileSet import load_tile_set
from stdafx import *


class TileMap:

    def load(self, name):
        # fill here
        f = open(name)
        info = json.load(f)
        f.close()

        self.__dict__.update(info)
        print(self.tilesets[0])
        self.tile_set = load_tile_set(self.tilesets[0]['source'])
        self.firstgid = self.tilesets[0]['firstgid']
        self.data = self.layers[0]['data']
        self.object_data = self.layers[1]['objects']
        self.tilewidth = self.tilewidth // 2
        self.tileheight = self.tileheight // 2

        new_data = []
        for row in reversed(range(self.height)):
            new_data.append(self.data[row * self.width : row * self.width + self.width])
        self.data = new_data

    # self.window_left, self.window_bottom, self.canvas_width, self.canvas_height
    def clip_draw_to_origin(self, l, b, w, h):
        # fill here
        tl = l // self.tilewidth
        tb = b // self.tileheight
        tw = (l + w) // self.tilewidth - tl + 1
        th = (b + h) // self.tileheight - tb + 1

        lo = l % self.tilewidth
        bo = b % self.tileheight

        for x in range(tl, min(tl + tw, self.width)):
            for y in range(tb, min(tb + th, self.height)):
                if not self.data[y][x] == 0:
                    self.tile_set.tile_images[self.data[y][x] - self.firstgid - 1].draw_to_origin(
                    (x - tl) * self.tilewidth - lo, (y - tb) * self.tileheight - bo,
                    self.tilewidth, self.tileheight
                    )

    def draw_bb(self, l, b, w, h):
        tl = l // self.tilewidth
        tb = b // self.tileheight
        tw = (l + w) // self.tilewidth - tl + 1
        th = (b + h) // self.tileheight - tb + 1

        lo = l % self.tilewidth
        bo = b % self.tileheight

        for x in range(tl, min(tl + tw, self.width)):
            for y in range(tb, min(tb + th, self.height)):
                if not self.data[y][x] == 0:
                    sx = (x - tl) * self.tilewidth - lo
                    sy = (y - tb) * self.tileheight - bo
                    if self.data[y][x] in range(2, 7):
                        draw_rectangle(sx, sy, sx + self.tilewidth, sy + self.tileheight)
                    else:
                        draw_rectangle(sx, sy, sx + self.tilewidth, sy + self.tileheight//2)

    def collide_check(self, l, b, w, h, player):
        tl = l // self.tilewidth
        tb = b // self.tileheight
        tw = (l + w) // self.tilewidth - tl + 1
        th = (b + h) // self.tileheight - tb + 1

        lo = l % self.tilewidth
        bo = b % self.tileheight

        for x in range(tl, min(tl + tw, self.width)):
            for y in range(tb, min(tb + th, self.height)):
                if not self.data[y][x] == 0:
                    sx = (x - tl) * self.tilewidth - lo
                    sy = (y - tb) * self.tileheight - bo
                    if self.data[y][x] in range(2, 7):
                        aabb = AABB(sx, sy, sx + self.tilewidth, sy + self.tileheight)
                    else:
                        aabb = AABB(sx, sy, sx + self.tilewidth, sy + self.tileheight//2)
                    if collide(player.aabb, aabb):
                        return True
        return False


def load_tile_map(name):
    tile_map = TileMap()
    tile_map.load(name)

    return tile_map



