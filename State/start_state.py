from pico2d import *

from Framework import game_framework
from State import title_state

name = "StartState"
background_img = None
image = None
logo_time = 0.0


def enter():
    global background_img
    global image
    open_canvas(1280, 720)
    background_img = load_image('Graphics\/background.png')
    image = load_image('Graphics\/logo.png')

# push_state가 아닌 change_state로 하면 여기 exit()부터 실행됨.
def exit():
    global background_img
    global image
    del(image)
    del(background_img)
    close_canvas()


def update(frame_time):
    global logo_time

    if(logo_time>1.0):
        logo_time = 0
        # game_framework.quit()
        game_framework.push_state(title_state)
    delay(0.01)
    logo_time += 0.01


def draw():
    global background_img
    global image
    clear_canvas()
    cw = get_canvas_width()
    ch = get_canvas_height()
    background_img.draw(cw/2, ch/2, cw, ch)
    image.draw(cw/2, ch/2, 533, 562)
    update_canvas()




def handle_events():
    events = get_events()
    pass


# push_state하면 pause()가 실행됨. 남겨두고 싶은 정보를 저장하는 함수.
def pause(): pass


# push_state를 한 후 거기서 exit()되면 resume()가 실행됨.
def resume(): pass




