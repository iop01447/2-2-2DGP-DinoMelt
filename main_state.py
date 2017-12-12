from pico2d import *

import game_framework

import title_state
import pause_state

from player import Player
from background import TileBackground as Background
from tile import Tile
from stdafx import *

name = "MainState"

# background_width = 73   # in tiles
# background_height = 56  # in tiles
# tile_width = 130 // 2
# tile_height = 130 // 2

player = None
background = None
debugging_draw = False
minimap_draw = False


def create_world():
    global player, background
    player = Player()
    background = Background()
    background.set_center_object(player)
    player.set_background(background)


def destroy_world():
    global player, background
    del(player)
    del(background)


def enter():
    open_canvas(1280, 720, sync=True)
    hide_cursor()
    game_framework.reset_time()
    create_world()


def exit():
    destroy_world()
    close_canvas()


def pause():
    pass


def resume():
    pass


def handle_events(frame_time):
    global debugging_draw
    global minimap_draw
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                #game_framework.change_state(title_state)
                game_framework.quit()
            elif event.type == SDL_KEYUP and event.key == SDLK_p:
                game_framework.push_state(pause_state)
            elif event.type == SDL_KEYUP and event.key == SDLK_g:
                debugging_draw = not debugging_draw
            elif event.type == SDL_KEYUP and event.key == SDLK_m:
                minimap_draw = not minimap_draw
            else:
                player.handle_event(event)
                background.handle_event(event)


def update(frame_time):
    player.update(frame_time)
    background.update(frame_time)


def debugging_draw_scene():
    player.draw_bb()
    background.draw_bb()


def draw_scene():
    background.draw()
    player.draw()
    player.life_draw()
    if debugging_draw:
        debugging_draw_scene()
    if minimap_draw:
        background.draw_minimap()


def draw():
    clear_canvas()
    draw_scene()
    update_canvas()





