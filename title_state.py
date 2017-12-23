import game_framework
import main_state
from pico2d import *


name = "TitleState"
background_img = None
logo_img = []

running = True

# frame speed
TIME_PER_ACTION = 0.1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 1

frame = 0
total_frames = 0.0
frame_cnt = 3

font = None

def enter():
    global background_img
    global logo_img
    global font
    background_img = load_image('Graphics\/title\/title_background.png')
    logo_img.append(load_image('Graphics\/title\/Frame1.png'))
    logo_img.append(load_image('Graphics\/title\/Frame2.png'))
    logo_img.append(load_image('Graphics\/title\/Frame3.png'))
    font = load_font('pingwing.ttf', 30)


def exit():
    global background_img
    global logo_img
    global font
    del(background_img)
    for img in logo_img:
        del(img)
    del font


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                running = False
                # game_framework.quit()
            elif(event.type, event.key)==(SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)


def draw():
    global background_img
    global logo_img
    global font
    clear_canvas()
    background_img.draw(400,300)
    logo_img[frame].draw(400,300)
    font.draw(230, 100, 'PRESS SPACE TO START...', (255,255,255))
    update_canvas()


def update(frame_time):
    global total_frames
    global FRAMES_PER_ACTION
    global ACTION_PER_TIME
    global frame_cnt
    global frame

    total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
    frame = int(total_frames) % frame_cnt

    if not running:
        game_framework.quit()


def pause():
    pass


def resume():
    pass






