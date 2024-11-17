# play_mode.py

from pico2d import *
import game_framework
import game_world
from grass import Grass
from koomba import Koomba
from mario import Mario
from brick import Brick  # 수정된 Brick 클래스

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

    # 벽돌 추가 (32x32 픽셀로 스프라이트 크기 두 배로 확장됨)
    bricks = [
        Brick(300, 150),
        Brick(350, 150),
        Brick(400, 150),
        Brick(450, 150),
        Brick(500, 150)
    ]
    game_world.add_objects(bricks, 1)

    # 충돌 쌍 등록
    for koomba in koombas:
        # 마리오와 굼바의 Top 히트박스 충돌 쌍
        game_world.add_collision_pair('mario:koomba_top', mario, koomba)
        # 마리오와 굼바의 Bottom 히트박스 충돌 쌍
        game_world.add_collision_pair('mario:koomba_bottom', mario, koomba)

    for brick in bricks:
        # 마리오와 Brick의 상단 충돌 쌍 등록
        game_world.add_collision_pair('mario:brick_top', mario, brick)
        # 마리오와 Brick의 하단 충돌 쌍 등록
        game_world.add_collision_pair('mario:brick_bottom', mario, brick)
        # 마리오와 Brick의 왼쪽 충돌 쌍 등록
        game_world.add_collision_pair('mario:brick_left', mario, brick)
        # 마리오와 Brick의 오른쪽 충돌 쌍 등록
        game_world.add_collision_pair('mario:brick_right', mario, brick)

    # Grass와 마리오의 충돌 쌍 등록
    game_world.add_collision_pair('mario:grass', mario, grass)

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
