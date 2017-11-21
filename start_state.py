import game_framework
import title_state
from pico2d import *


name = "StartState"
image = None
logo_time = 0.0


def enter():
    global image
    open_canvas()
    image = load_image('kpu_credit.png')


# push_state가 아닌 change_state로 하면 여기 exit()부터 실행됨.
def exit():
    global image
    del(image)
    close_canvas()


def update():
    global logo_time

    if(logo_time>1.0):
        logo_time = 0
        # game_framework.quit()
        game_framework.push_state(title_state)
    delay(0.01)
    logo_time += 0.01


def draw():
    global image
    clear_canvas()
    image.draw(400, 300)
    update_canvas()




def handle_events():
    events = get_events()
    pass


# push_state하면 pause()가 실행됨. 남겨두고 싶은 정보를 저장하는 함수.
def pause(): pass


# push_state를 한 후 거기서 exit()되면 resume()가 실행됨.
def resume(): pass




