from pico2d import *

from Map.TileMap import load_tile_map
from Object.object import Object
from SourceFiles.stdafx import *


class TileBackground:
    bgm = None
    minimap_image = None
    background_image = None

    def __init__(self):
        self.tile_map = load_tile_map('..\/Map.json')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.window_left = 0
        self.window_bottom = 0
        self.w = self.tile_map.width * self.tile_map.tilewidth
        self.h = self.tile_map.height * self.tile_map.tileheight
        # sound
        self.bgm = load_music('..\/Sound\/Plepur.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
        # image
        self.minimap_image = load_image('..\/Graphics\/Map.png')
        self.background_image = load_image('..\/Graphics\/background.png')
        # objects
        self.objects = []
        for object in self.tile_map.object_data:
            x_limited = 0
            state = 0
            if object['type'] in ('red', 'blue',):
                x_limited = object['properties']['x limited'] // 2
            elif object['type'] in ('orange', ):
                state = object['properties']['state']
            self.objects.append(Object(object['x'] // 2, (self.tile_map.height * self.tile_map.tileheight * 2 - object['y']) // 2
                                       , object['width'] // 2, object['height'] // 2, object['type'], x_limited, state, self))

    def set_center_object(self, player):
        self.center_object = player
        for object in self.objects:
            object.set_player(player)
        self.max_window_left = self.w - self.canvas_width
        self.max_window_bottom = self.h - self.canvas_height

    # draw
    def draw(self):
        self.background_image.draw_to_origin(0, 0, self.canvas_width, self.canvas_height)
        self.tile_map.clip_draw_to_origin(self.window_left, self.window_bottom, self.canvas_width, self.canvas_height)
        self.objects_draw()

    def draw_minimap(self):
        self.minimap_image.draw(self.canvas_width - (self.w * 0.05//2), self.canvas_height - (self.h * 0.05//2), self.w * 0.05, self.h * 0.05)
        x = self.center_object.x * 0.05
        y = self.center_object.y * 0.05
        x += self.canvas_width - self.w * 0.05
        y += self.canvas_height - self.h * 0.05
        draw_rectangle(x - 5, y - 5, x + 5, y + 5)

    def draw_bb(self):
        self.tile_map.draw_bb(self.window_left, self.window_bottom, self.canvas_width, self.canvas_height)
        self.objects_draw_bb()

    def objects_draw(self):
        for object in self.objects:
            object.draw()

    def objects_draw_bb(self):
        for object in self.objects:
            object.draw_bb()

    # canvas 영역
    def get_bb(self):
        return 0, 0, self.canvas_width, self.canvas_height

    # update
    def update(self, frame_time):
        self.window_left = clamp(0, int(self.center_object.x) - self.canvas_width // 2, self.max_window_left)
        self.window_bottom = clamp(0, int(self.center_object.y) - self.canvas_height // 2, self.max_window_bottom)
        self.objects_update(frame_time)

    # Object
    def objects_update(self, frame_time):
        for object in self.objects:
            object.update(frame_time)

    def player_monster_collide_check(self):
        for o in self.objects:
            if o.type != 'orb' and o.object.exsist:
                if collide(self.center_object.aabb, o.object.aabb):
                    return True
                if o.type == 'orange' and collide(self.center_object.aabb, o.object.bullet.aabb):
                    return True
        return False

    def player_orb_collide_check(self):
        for o in self.objects:
            if o.type == 'orb' and o.object.exsist:
                if collide(self.center_object.aabb, o.object.aabb):
                    return True
        return False

    def handle_event(self, event):
        pass


