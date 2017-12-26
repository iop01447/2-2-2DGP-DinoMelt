from pico2d import *
from SourceFiles.stdafx import *


class MiniMap:
    background_image = None
    image = []

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()

        # image
        self.image.append(load_image('Graphics\/map\/map1.png'))
        self.image.append(load_image('Graphics\/map\/map2.png'))
        self.image.append(load_image('Graphics\/map\/map3.png'))
        self.image.append(load_image('Graphics\/map\/map4.png'))
        self.image.append(load_image('Graphics\/map\/map5.png'))
        self.image.append(load_image('Graphics\/map\/map6.png'))
        self.image.append(load_image('Graphics\/map\/map7.png'))
        self.image.append(load_image('Graphics\/map\/map8.png'))
        self.image.append(load_image('Graphics\/map\/map9.png'))
        self.image.append(load_image('Graphics\/map\/map10.png'))
        self.image.append(load_image('Graphics\/map\/map11.png'))
        self.image.append(load_image('Graphics\/map\/map12.png'))
        self.image.append(load_image('Graphics\/map\/map13.png'))
        self.image.append(load_image('Graphics\/map\/map14.png'))
        self.background_image = load_image('Graphics\/map\/background.png')

        self.img_w = self.background_image.w
        self.img_h = self.background_image.h

    def background_draw(self):
        self.background_image.opacify(0.5)
        self.background_image.draw(self.canvas_width/2, self.canvas_height/2, self.canvas_width, self.canvas_height)
        self.background_image.opacify(1)
        self.background_image.draw(self.canvas_width/2, self.canvas_height/2)

    def draw(self, index):
        index -= 1
        self.image[index].draw(self.canvas_width/2, self.canvas_height/2)