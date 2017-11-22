from pico2d import *

import game_framework

import title_state
import pause_state

from player import Player
from background import TileBackground as Background


name = "MainState"


background_width = 73   # in tiles
background_height = 56  # in tiles
tile_width = 130
tile_height = 130


player = None
background = None


def create_world():
    global player, background
    player = Player()
    background = Background(background_width, background_height)
  #  background = Background()
    background.set_center_object(player)
    player.set_background(background)


def destroy_world():
    global player, background
    del(player)
    del(background)


def enter():
    open_canvas(11 * tile_width, 7 * tile_height)
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
            else:
                player.handle_event(event)
                background.handle_event(event)


def update(frame_time):
    player.update(frame_time)
    background.update(frame_time)


def draw_scene():
    background.draw()
    player.draw()


def draw():
    clear_canvas()
    draw_scene()
    update_canvas()





