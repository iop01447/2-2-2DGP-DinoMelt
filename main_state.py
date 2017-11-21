import random
import json
import os

from pico2d import *

import game_framework
import title_state
import pause_state
import Map

name = "MainState"

font = None
map = None

def enter():
    global map
    global boy
    global player
    map = Map.Map()
    pass


def exit():
    global map
    del(map)


def pause():
    pass


def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYUP and event.key == SDLK_p:
            game_framework.push_state(pause_state)


def update(frame_time):
    map.update(frame_time)

def draw_scene():
    map.draw()


def draw():
    clear_canvas()
    draw_scene()
    update_canvas()





