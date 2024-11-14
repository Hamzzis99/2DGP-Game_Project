from pico2d import *
import game_framework

import game_world
from game_world import add_collision_pair
from grass import Grass
from mario import Mario

# boy = None

def handle_events():
    global mario  # mario 변수를 사용하기 위해 global 선언
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            mario.handle_event(event)  # 인스턴스를 통해 메서드 호출

def init():
    global mario

    grass = Grass()
    game_world.add_object(grass, 0)

    mario = Mario()
    game_world.add_object(mario, 1)


#def colide(boy, buit()all):
    #pass


def finish():
    game_world.clear()
    pass

def update():
    game_world.update() # 객체들의 위치가 다 결정됐다. 따라서 이어서 충돌 검사를 하면 됨.
    # fill here
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass

def resume():
    pass
