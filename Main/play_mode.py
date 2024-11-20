# play_mode.py
import game_over

# 1. 최상단에 objects_to_add 리스트 정의
objects_to_add = []
mario_dead = False

from pico2d import *
import game_framework
import game_world
from grass import Grass
from koomba import Koomba
from boss_turtle import Turtle  # Turtle 클래스 임포트
from mario import Mario, reset_mario
from brick import Brick
from random_box import Random_box
from gun_box import Gun_box  # Gun_box 임포트
from star import Star        # Star 클래스 임포트
from coin import Coin        # Coin 클래스 임포트
from utils.camera import Camera
from config import MarioConfig  # MarioConfig 임포트
from dashboard import Dashboard  # Dashboard 클래스 임포트
from bgm import BGMManager  # bgm.py에서 BGMManager 임포트

# 전역 변수 선언
camera = None          # 전역 카메라 객체
dashboard = None       # 전역 대시보드 객체
game_time = None       # 게임 시간 (초)
bgm_manager = None     # 배경음악 관리자 객체


def handle_events():
    global mario
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            #print("Quit event detected")
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            #print("Escape key pressed")
            game_framework.quit()
        elif event.type in (SDL_KEYDOWN, SDL_KEYUP):
            #print(f"Key Event: {event.type}, Key: {event.key}")  # 디버깅 출력
            mario.handle_event(event)  # 키 이벤트만 마리오에게 전달


def init():
    global mario, camera, dashboard, game_time, bgm_manager, mario_dead

    mario_dead = False  # 초기화 시 dead 플래그 초기화

    if 'mario' in globals():
        reset_mario(mario)
        game_world.clear()

    grass = Grass()
    game_world.add_object(grass, 0)

    dashboard = Dashboard()  # Dashboard 인스턴스 생성

    mario = Mario(dashboard)  # Dashboard 인스턴스를 Mario에게 전달
    game_world.add_object(mario, 1)

    koombas = [Koomba() for _ in range(5)]
    game_world.add_objects(koombas, 1)

    # Turtle 추가
    turtlers = [Turtle() for _ in range(3)]  # 원하는 개수만큼 Turtle 생성
    game_world.add_objects(turtlers, 1)      # 레이어 1에 추가

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

    # Gun Box 추가
    gun_boxes = [
        Gun_box(700, 150),
        Gun_box(750, 150)
    ]
    game_world.add_objects(gun_boxes, 1)

    # 충돌 쌍 등록
    for koomba in koombas:
        # 마리오와 Koomba의 Top 히트박스 충돌 쌍 등록
        game_world.add_collision_pair('mario:koomba_top', mario, koomba)
        # 마리오와 Koomba의 Bottom 히트박스 충돌 쌍 등록
        game_world.add_collision_pair('mario:koomba_bottom', mario, koomba)

    for turtle in turtlers:
        # 마리오와 Turtle의 충돌 쌍 등록
        game_world.add_collision_pair('mario:turtle', mario, turtle)

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

    for gun_box in gun_boxes:
        game_world.add_collision_pair('mario:gun_box_top', mario, gun_box)
        game_world.add_collision_pair('mario:gun_box_bottom', mario, gun_box)
        game_world.add_collision_pair('mario:gun_box_left', mario, gun_box)
        game_world.add_collision_pair('mario:gun_box_right', mario, gun_box)

    # Grass와 마리오의 충돌 쌍 등록
    game_world.add_collision_pair('mario:grass', mario, grass)

    # 배경음악 관리자 초기화
    bgm_manager = BGMManager()
    print("Loading background music...")  # 디버깅 출력
    bgm_manager.load_music('main_theme', 'resources/chetahman2.mp3')  # 변환된 파일 경로
    bgm_manager.play('main_theme', MarioConfig.GAME_MUSIC_VOLUME)
    print("Background music started.")  # 디버깅 출력

    camera = Camera(800, 600, MarioConfig.WORLD_WIDTH, MarioConfig.WORLD_HEIGHT)
    #dashboard = Dashboard()
    game_time = MarioConfig.GAME_TIME_LIMIT


def finish():
    global bgm_manager
    if bgm_manager:
        bgm_manager.stop()
    game_world.reset()  # game_world 완전 초기화
    print("play_mode의 finish()가 호출되었습니다.")  # 디버깅 출력


def update():
    global game_time, objects_to_add, mario_dead

    game_world.update()            # 객체들의 위치 업데이트
    game_world.handle_collisions() # 충돌 처리
    camera.update(mario)           # 카메라 위치 업데이트

    # Mario의 dead 상태 확인
    if mario.dead and not mario_dead:
        mario_dead = True
        print("Mario is dead. Stopping music and triggering game over.")
        if bgm_manager:
            bgm_manager.stop()  # 배경음악 명시적으로 중지
        game_framework.change_mode(game_over)  # 게임 오버로 전환

    # 추가할 객체 처리
    for obj in objects_to_add:
        game_world.add_object(obj, 1)
        # 충돌 쌍 등록
        if isinstance(obj, Coin):
            game_world.add_collision_pair('mario:coin', mario, obj)
        elif isinstance(obj, Star):
            game_world.add_collision_pair('mario:star', mario, obj)
    objects_to_add.clear()

    # 게임 시간 업데이트
    game_time -= game_framework.frame_time
    if game_time <= 0:
        game_time = 0
        dashboard.set_time(int(game_time))
        dashboard.update()
        print("Time is up! Game Over.")
        if bgm_manager:
            bgm_manager.stop()  # 배경음악 중지
        game_framework.change_mode(game_over)

    # 대시보드에 현재 게임 시간 설정
    dashboard.set_time(int(game_time))  # 정수로 전달

    # 대시보드 업데이트
    dashboard.update()

    #print(f"Game Time: {game_time}")  # 디버그 출력

    # 아래 중복된 조건문 제거
    # if mario_dead:
    #     print("mario_dead flag is True. Changing mode to game_over.")
    #     game_framework.change_mode(game_over)


def draw():
    clear_canvas()
    game_world.render_with_camera(camera)  # 카메라를 고려하여 렌더링
    dashboard.draw(camera)                 # 대시보드 그리기
    update_canvas()


def pause():
    pass


def resume():
    pass
