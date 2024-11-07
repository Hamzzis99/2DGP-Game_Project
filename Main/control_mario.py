from pico2d import *

from mario import Mario
from grass import Grass


# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            if event.type in (SDL_KEYDOWN, SDL_KEYUP):
                mario.handle_event(event)  # 입력 이벤트를 마리오에게 전달합니다.


def reset_world():
    global running
    global grass
    global world
    global mario

    running = True
    world = []

    grass = Grass()
    world.append(grass)

    mario = Mario()
    world.append(mario)


def update_world():
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas()
reset_world()
# 게임 루프
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# 마무리 코드
close_canvas()
