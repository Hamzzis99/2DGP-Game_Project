# play_mode.py

from pico2d import *
import game_framework
import game_world
from grass import Grass
from koomba import Koomba
from mario import Mario
from brick import Brick
from random_box import Random_box
from utils.camera import Camera
from config import MarioConfig  # MarioConfig 임포트
from dashboard import Dashboard  # Dashboard 클래스 임포트

camera = None  # 전역 카메라 객체
dashboard = None  # 전역 대시보드 객체
game_time = None  # 게임 시간 (초)


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
    global mario, camera, dashboard, game_time

    grass = Grass()
    game_world.add_object(grass, 0)

    mario = Mario()
    game_world.add_object(mario, 1)

    koombas = [Koomba() for _ in range(5)]
    game_world.add_objects(koombas, 1)

    # 벽돌 추가 (32x32 픽셀로 스프라이트 크기 두 배로 확장됨)
    bricks = [
        Brick(300, 100),
        Brick(350, 100),
        Brick(400, 100),
        Brick(450, 100),
        Brick(500, 100)
    ]
    game_world.add_objects(bricks, 1)

    # Random Box 추가
    random_boxes = [
        Random_box(600, 150),
        Random_box(650, 150)
    ]
    game_world.add_objects(random_boxes, 1)

    # 충돌 쌍 등록
    for koomba in koombas:
        # 마리오와 굼바의 Top 히트박스 충돌 쌍 등록
        game_world.add_collision_pair('mario:koomba_top', mario, koomba)
        # 마리오와 굼바의 Bottom 히트박스 충돌 쌍 등록
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

    for random_box in random_boxes:
        game_world.add_collision_pair('mario:random_box_top', mario, random_box)
        game_world.add_collision_pair('mario:random_box_bottom', mario, random_box)
        game_world.add_collision_pair('mario:random_box_left', mario, random_box)
        game_world.add_collision_pair('mario:random_box_right', mario, random_box)

    # Grass와 마리오의 충돌 쌍 등록
    game_world.add_collision_pair('mario:grass', mario, grass)

    # 카메라 초기화 (화면 크기: 800x600, 월드 크기: 1600x600)
    camera = Camera(800, 600, MarioConfig.WORLD_WIDTH, MarioConfig.WORLD_HEIGHT)

    # Dashboard 초기화
    dashboard = Dashboard()

    # 게임 시간 초기화 (config.py에서 설정한 값 사용)
    game_time = MarioConfig.GAME_TIME_LIMIT


def finish():
    game_world.clear()
    pass


def update():
    global game_time

    game_world.update()  # 객체들의 위치 업데이트
    game_world.handle_collisions()  # 충돌 처리
    camera.update(mario)  # 카메라 위치 업데이트

    # 게임 시간 업데이트
    game_time -= game_framework.frame_time
    if game_time <= 0:
        game_time = 0
        dashboard.set_time(int(game_time))  # 시간 설정
        dashboard.update()
        print("시간이 다 되었습니다. 게임을 종료합니다.")
        game_framework.quit()

    # 대시보드에 현재 게임 시간 설정
    dashboard.set_time(int(game_time))  # 정수로 전달

    # 대시보드 업데이트
    dashboard.update()

    print(f"Game Time: {game_time}")  # 디버그 출력


def draw():
    clear_canvas()
    game_world.render_with_camera(camera)  # 카메라를 고려하여 렌더링
    dashboard.draw(camera)  # 대시보드 그리기

    if game_time <= 0:
        # "TIME UP" 메시지 표시
        dashboard.font.draw("TIME UP!", 400, 300, None, scaling_factor=4)  # 중앙에 크게 표시

    update_canvas()


def pause():
    pass


def resume():
    pass
