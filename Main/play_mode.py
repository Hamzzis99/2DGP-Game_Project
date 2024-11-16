# play_mode.py

from pico2d import *
import game_framework
import game_world
from grass import Grass
from koomba import Koomba
from mario import Mario

def handle_events():
    global mario
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            mario.handle_event(event)  # 마리오 인스턴스를 통해 이벤트 처리

def init():
    global mario

    grass = Grass()
    game_world.add_object(grass, 0)

    mario = Mario()
    game_world.add_object(mario, 1)

    koombas = [Koomba() for _ in range(5)]
    game_world.add_objects(koombas, 1)

    # 충돌 쌍 등록
    for koomba in koombas:
        # 마리오와 굼바의 Top 히트박스 충돌 쌍
        game_world.add_collision_pair('mario:koomba_top', mario, koomba)
        # 마리오와 굼바의 Bottom 히트박스 충돌 쌍
        game_world.add_collision_pair('mario:koomba_bottom', mario, koomba)

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()  # 객체들의 위치 업데이트
    game_world.handle_collisions()  # 충돌 처리

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass
