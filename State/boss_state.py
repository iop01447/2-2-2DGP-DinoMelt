from pico2d import *

from Framework import game_framework
from Player.boss_state_player import BossState_Player as Player
from Monster.boss import Boss
from State import boss_pause_state as pause_state

name = "BossState"

# enter exit pause resume handle_events update draw

background_img = None
bgm = None
player = None
boss = None
debugging_draw = False
is_pop_state = False


def enter():
    global background_img, bgm, player, boss
    background_img = load_image('Graphics\/boss_background.png')
    bgm = load_music('Sound\/Batalla de Plasticina.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()
    player = Player()
    boss = Boss()
    player.set_boss(boss)
    pass

def exit():
    global background_img, bgm, player, boss
    bgm.stop()
    del(background_img)
    del(bgm)
    del(player)
    del(boss)
    pass

def pause():
    global bgm
    bgm.pause()

def resume():
    global bgm
    bgm.resume()

def handle_events():
    global debugging_draw
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.type == SDL_KEYUP and event.key == SDLK_SPACE:
                game_framework.quit()
            elif event.type == SDL_KEYUP and event.key == SDLK_p:
                game_framework.push_state(pause_state)
            elif event.type == SDL_KEYUP and event.key == SDLK_g:
                debugging_draw = not debugging_draw
            else:
                player.handle_event(event)

def update(frame_time):
    player.update(frame_time)
    boss.update(frame_time)
    if is_pop_state:
        game_framework.pop_state()

def debugging_draw_scene():
    player.draw_bb()
    boss.draw_bb()

def draw_scene():
    global background_img, player, boss
    cw = get_canvas_width()
    ch = get_canvas_height()
    background_img.draw(cw / 2, ch / 2)
    boss.draw()
    player.draw()
    if debugging_draw:
        debugging_draw_scene()


def draw():
    clear_canvas()
    draw_scene()
    update_canvas()
