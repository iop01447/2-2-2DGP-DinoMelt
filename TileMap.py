__author__ = 'dustinlee'

import json

from pico2d import *


from TileSet import load_tile_set
from object import Object
from tile import Tile


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
        self.objects = [Object(object['x']//2, (self.height * self.tileheight - object['y'])//2
                               , object['width']//2, object['height']//2,
                               object['type'], object['properties']['x limited']) for object in self.object_data]
        self.tilewidth = self.tilewidth // 2
        self.tileheight = self.tileheight // 2

        new_data = []
        for row in reversed(range(self.height)):
            new_data.append(self.data[row * self.width : row * self.width + self.width])
        self.data = new_data

        self.tiles = []
        for i in range(self.height):
            for j in range(self.width):
                self.tiles.append(Tile(i, j, self.data[i][j]))


    def clip_draw_to_origin(self, l, b, w, h, dx, dy):
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

    def objects_draw(self, window_left, window_bottom):
        for object in self.objects:
            object.draw(window_left, window_bottom)
        pass


def load_tile_map(name):
    tile_map = TileMap()
    tile_map.load(name)

    return tile_map



