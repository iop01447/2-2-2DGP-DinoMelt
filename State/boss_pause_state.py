from pico2d import *

from Framework import game_framework
from State import boss_state

# enter exit pause resume handle_events update draw

pause_img = None
switch = True
total_frame_time = 0.0

def enter():
    global pause_img
    pause_img = load_image('..\/Graphics\/pause.png')
    pass

def exit():
    global  pause_img
    del(pause_img)
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
            elif event.type == SDL_KEYUP and event.key == SDLK_p:
                game_framework.pop_state()

def update(frame_time):
    global total_frame_time
    global switch
    total_frame_time += frame_time
    if total_frame_time > 1:
        total_frame_time = 0
        switch = not switch

def draw():
    global pause_img
    cw = get_canvas_width()
    ch = get_canvas_height()

    clear_canvas()
    boss_state.draw_scene()
    if switch:
        pause_img.draw(cw/2, ch/2)
    update_canvas()