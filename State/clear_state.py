from pico2d import *

from Framework import game_framework

# enter exit pause resume handle_events update draw

clear_img = None
background_img = None
bgm = None

def enter():
    global background_img, bgm, clear_img
    clear_img = load_image('Graphics\/game_clear.png')
    bgm = load_music('Sound\/El Fin de la Era Plastozoica.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()
    pass

def exit():
    global background_img, bgm, clear_img
    del(background_img)
    del(clear_img)
    del(bgm)
    pass

def pause():
    pass

def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.type == SDL_KEYUP and event.key == SDLK_SPACE:
                game_framework.quit()

def update(frame_time):
    pass

def draw():
    global background_img, clear_img
    cw = get_canvas_width()
    ch = get_canvas_height()

    clear_canvas()
    clear_img.draw(cw/2, ch/2, cw, ch)
    update_canvas()