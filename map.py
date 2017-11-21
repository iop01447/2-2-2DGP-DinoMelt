from pico2d import *
import json
import Tile
import Player

class Map():
    def __init__(self):
      #  filename = '"map.json", "r"'
        self.tilesize = 130//2

        try:
            with open("map.json", "r") as mapfile:
                self.mapdict = json.loads(mapfile.read())
                self.layers = self.mapdict["layers"]
                self.mapheight = self.mapdict["height"] * self.tilesize
                self.mapwidth = self.mapdict["width"] * self.tilesize
        except IOError:
            print("Cannot open map file {}".format("map.json", "r"))

        self.image = load_image('Graphics\map.png')
        #self.canvas_width = self.tilesize * 11
        #self.canvas_height = self.tilesize * 7
        self.canvas_width = 800
        self.canvas_height = 600
        x = (6*self.tilesize + 7*self.tilesize)//2
        y = ((self.mapdict["height"]-13)*self.tilesize + (self.mapdict["height"]-14)*self.tilesize)//2
        self.player = Player.Player(x, y)
        self.build()

    def build(self):
        data = self.layers[0]["data"]
        index = 0
        self.all_tiles = {}

        for y in range(0, self.mapdict["height"]):
            for x in range(0, self.mapdict["width"]):
                id_key = data[index]
                if id_key != 0:
                    self.all_tiles[index] = Tile.Tile(x, y, self.tilesize, self.mapdict["height"])
                index += 1

    def draw(self):
        self.window_bottom = self.player.y - self.canvas_height//2
        self.window_left = self.player.x - self.canvas_width//2
        self.image.clip_draw_to_origin(
            self.window_left, self.window_bottom,
        self.canvas_width, self.canvas_height, 0, 0)

        self.player.draw()

    def update(self, frame_time):
        self.player.update(frame_time)
