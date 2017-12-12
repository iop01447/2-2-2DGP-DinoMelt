__author__ = 'dustinlee'

import json

from pico2d import *


from TileSet import load_tile_set
from ball import ObjectBall as Ball


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
        self.objects = self.layers[1]['objects']
        self.balls = [Ball(object['x'], self.height * self.tileheight - object['y'] - object['height'], object['width'], object['height']) for object in self.objects]

        new_data = []
        for row in reversed(range(self.height)):
            new_data.append(self.data[row * self.width : row * self.width + self.width])
        self.data = new_data


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
                self.tile_set.tile_images[self.data[y][x] - self.firstgid].draw_to_origin(
                    (x - tl) * self.tilewidth - lo, (y - tb) * self.tileheight - bo
                )

    def objects_draw(self, window_left, window_bottom):
        for ball in self.balls:
            ball.draw(window_left, window_bottom)
        pass


def load_tile_map(name):
    tile_map = TileMap()
    tile_map.load(name)

    return tile_map


# if __name__ =='__main__':
#     tile_map = load_tile_map('desert_map.json')
#     print(tile_map.objects)



