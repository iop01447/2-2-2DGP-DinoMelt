__author__ = 'dustinlee'

import json

from pico2d import *

class TileSet:

    def __init__(self):
        self.firstgid = 0

    def load(self, file_name):
        # fill here
        f = open(file_name)
        data = json.load(f)
        f.close()
        self.__dict__.update(data)
        print(self.__dict__)
        self.tile_images = []
        for i in range(1, self.tilecount + 1):
            self.tile_images.append(load_image(self.tiles[str(i)]['image']))
        self.tileheight = self.tileheight // 2
        self.tilewidth  = self.tilewidth // 2

def load_tile_set(file_name):
    # fill here
    tile_set = TileSet()
    tile_set.load(file_name)

    return tile_set

if __name__ =='__main__':
    # fill here
    open_canvas(800, 600)

    tile_set = load_tile_set('..\/tileset.json')
    columns = 5

    for i in range(tile_set.tilecount):
        col = i % columns  # 열
        row = i // columns  # 행
        tile_set.tile_images[i].draw_to_origin(0 + col * tile_set.tilewidth,
                                               400 - row * tile_set.tileheight,
                                               tile_set.tilewidth, tile_set.tileheight)

    update_canvas()
    delay(5)
    close_canvas()
