from pico2d import *

from Framework import game_framework
from Map.background import TileBackground as Background
from Player.player import Player
from State import pause_state

name = "MainState"

# background_width = 73   # in tiles
# background_height = 56  # in tiles
# tile_width = 130 // 2
# tile_height = 130 // 2

player = None
background = None
debugging_draw = False
minimap_draw = False
bgm = None
minimap_sound = None


def create_world():
    global player, background, bgm, minimap_sound
    player = Player()
    background = Background()
    background.set_center_object(player)
    player.set_background(background)
    # sound
    bgm = load_music('Sound\/Plepur.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()
    minimap_sound = load_wav('Sound\/minimap.wav')
    minimap_sound.set_volume(128)


def destroy_world():
    global player, background, minimap_sound
    del(player)
    del(background)
    del(minimap_sound)


def enter():
    open_canvas(1280, 720)
    hide_cursor()
    game_framework.reset_time()
    create_world()


def exit():
    destroy_world()
    close_canvas()


def pause():
    global bgm
    bgm.pause()
    if player.meet_boss:
        player.original_initialize()


def resume():
    global bgm, player
    bgm.resume()
    if player.meet_boss:
        bgm.repeat_play()
        if not player.boss_clear:
            player.new_life_sound.play()
            player.check_point_initialize()


def handle_events():
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
                minimap_sound.play()
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
    if debugging_draw:
        debugging_draw_scene()
    if minimap_draw:
        background.draw_minimap()


def draw():
    clear_canvas()
    draw_scene()
    update_canvas()





