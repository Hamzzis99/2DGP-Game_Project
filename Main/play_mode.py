from pico2d import *
import game_framework

import game_world
from game_world import add_collision_pair
from grass import Grass
from mario import Mario

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            Mario.handle_event(event)

def finish():
    game_world.clear()
    pass


#def colide(boy, ball):
    #pass


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
