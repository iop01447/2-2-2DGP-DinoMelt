from pico2d import *
from tile_map import load_tile_map
from tile import Tile
from stdafx import *
from object import Object

class TileBackground:
    image = None
    tile_map = None
    bgm = None

    def __init__(self):
        if self.image == None:
            self.image = load_image('Graphics\map.png')
        self.speed = 0
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.window_left = 0
        self.window_bottom = 0
        self.w = self.image.w
        self.h = self.image.h
        # tile map
        self.tiles = []
        if self.tile_map == None:
            self.tile_map = load_tile_map('map.json', 'tileset.json')
        for i in range(self.tile_map.map_height):
            for j in range(self.tile_map.map_width):
                self.tiles.append(Tile(i, j, self.tile_map.map2d[i][j]))
        # tile map ㅠㅠ 수정해야되는데 시간이 없다
        name = 'map.json'
        f = open(name)
        info = json.load(f)
        f.close()

        self.__dict__.update(info)
        print(self.tilesets[0])
        self.firstgid = self.tilesets[0]['firstgid']
        self.data = self.layers[0]['data']
        self.object_data = self.layers[1]['objects']
        self.objects = [Object(object['x']//2, (self.height * 130 - object['y'] - object['height'])//2, object['width']//2,
                           object['height']//2, object['type'], object['properties']['x limited']) for object in self.object_data]
        # sound
        self.bgm = load_music('Sound\/Plepur.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

    def set_center_object(self, player):
        self.center_object = player

    def draw(self):
        self.image.clip_draw_to_origin(
            self.window_left, self.window_bottom,
            self.canvas_width, self.canvas_height, 0, 0
        )

    def objects_draw(self):
        for object in self.objects:
            object.draw(self.window_left, self.window_bottom)

    def draw_bb(self):
        for tile in self.tiles:
            if collide(tile, self) and tile.value != 0:
                tile.draw_bb()

    def draw_minimap(self):
        size = 0.05
        self.image.draw(self.canvas_width - (self.w * size//2), self.canvas_height - (self.h * size//2), self.w * size, self.h * size)
        x = self.center_object.x * 0.05
        y = self.center_object.y * 0.05
        x += self.canvas_width - self.w * size
        y += self.canvas_height - self.h * size
        draw_rectangle(x - 10, y - 10, x + 10, y + 10)

    # canvas 영역
    def get_bb(self):
        return 0, 0, self.canvas_width, self.canvas_height

    def tile_update(self):
        for tile in self.tiles:
            tile.update(self.window_left, self.window_bottom)

    def update(self, frame_time):
        self.window_left = clamp(
            0, int(self.center_object.x) - self.canvas_width // 2,
               self.w - self.canvas_width
        )
        self.window_bottom = clamp(
            0, int(self.center_object.y) - self.canvas_height // 2,
               self.h - self.canvas_height
        )
        self.tile_update()

    def handle_event(self, event):
        pass



