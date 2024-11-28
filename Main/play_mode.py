# play_mode.py

from pico2d import *
import game_framework
import game_world
import logo_mode
from ball import Ball
from grass import Grass
from enemy.koomba import Koomba
from enemy.turtle import Turtle
from enemy.boss_turtle import Boss_turtle  # Boss_turtle 임포트
from mario import Mario, reset_mario
from props.brick import Brick
from props.random_box import Random_box
from props.gun_box import Gun_box
from props.clean_box import Clean_box
from items.star import Star
from items.coin import Coin
from states import game_state
from utils.camera import Camera
from utils.config import MarioConfig
from utils.dashboard import Dashboard
from utils.bgm import BGMManager
import game_over

# 전역 변수 선언
camera = None          # 전역 카메라 객체
dashboard = None       # 전역 대시보드 객체
game_time = None       # 게임 시간 (초)
bgm_manager = None     # 배경음악 관리자 객체
objects_to_add = []    # 추가할 객체 리스트
mario_dead = False     # Mario의 사망 상태 플래그
death_timer = None     # Mario 사망 시각 기록

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
    global mario, camera, dashboard, game_time, bgm_manager, mario_dead, death_timer

    mario_dead = False          # 초기화 시 dead 플래그 초기화
    death_timer = None          # 초기화 시 타이머 초기화

    game_world.clear()  # 게임 월드 초기화

    # Boss_turtle 추가 (지정된 x, y 좌표로)
    boss = Boss_turtle(0, 300)  # 원래 20 스케일 및 초기 y 위치 조정
    game_world.add_object(boss, 1)

    # Grass 객체 6개 생성 (x 간격은 50으로 설정)
    grass1 = Grass()
    grass1.x = 0
    grass1.y = 30
    grass1.width = 600

    grass2 = Grass()
    grass2.x = 880
    grass2.y = 30
    grass2.width = 500

    grass3 = Grass()
    grass3.x = 1900
    grass3.y = 30
    grass3.width = 400

    grass4 = Grass()
    grass4.x = 2900
    grass4.y = 30
    grass4.width = 100

    grass5 = Grass()
    grass5.x = 3600
    grass5.y = 30
    grass5.width = 100

    grass6 = Grass()
    grass6.x = 4500
    grass6.y = 30
    grass6.width = 100

    # Grass 객체들을 게임 월드에 추가
    game_world.add_object(grass1, 0)
    game_world.add_object(grass2, 0)
    game_world.add_object(grass3, 0)
    game_world.add_object(grass4, 0)
    game_world.add_object(grass5, 0)
    game_world.add_object(grass6, 0)

    # Grass 객체들을 하나의 리스트로 묶음
    grasses = [grass1, grass2, grass3, grass4, grass5, grass6]

    dashboard = Dashboard()  # Dashboard 인스턴스 생성

    mario = Mario(dashboard)  # Dashboard 인스턴스를 Mario에게 전달
    game_world.add_object(mario, 1)

    # Koombas 추가 (지정된 x, y 좌표로)
    koombas = [
        Koomba(650, 70, 100),
        Koomba(680, 70, 100),
        #Koomba(500, 70),
        #Koomba(600, 70),
        #Koomba(1000, 70)
    ]
    game_world.add_objects(koombas, 1)

    # Turtle 추가 (지정된 x, y 좌표로)
    turtlers = [
        #Turtle(350, 70),
        #Turtle(450, 70),
        #Turtle(1000, 70)
    ]
    game_world.add_objects(turtlers, 1)

    # 벽돌 추가 (32x32 픽셀로 스프라이트 크기 두 배로 확장됨)
    # 모든 prop들은 x값을 26씩 떨어뜨리면 됨.
    bricks = [
        Brick(360, 100),
        Brick(386, 100),
        Brick(412, 100),
        Brick(438, 100),
        Brick(438, 180), # 공중벽
        Brick(464, 100),
        Brick(490, 100),
        Brick(516, 100),
        Brick(810, 90),
        Brick(836, 90),
        Brick(1145, 70),
        Brick(1168, 98),
        Brick(1196, 126),
        Brick(1224, 156),
        Brick(1252, 184),
        Brick(1280, 210),
        Brick(1308, 210),
        Brick(1336, 210),
        Brick(1364, 210),
        #Brick(1392, 210),
        #Brick(1420, 210),
        #Brick(1448, 210),
        Brick(1476, 210),
        Brick(1504, 210),
        Brick(1532, 210),

        Brick(1560, 182),
        Brick(1588, 154),
        Brick(1616, 126),
        Brick(1644, 98),
        Brick(1672, 80),

    ]

    # 브릭 생성: y=70, x=0, 24, 48, 72, 96
    #bricks = [Brick(x, 70) for x in range(0, 24 * 100, 24)]

    game_world.add_objects(bricks, 1)
    # 모든 prop들은 x값을 28씩 떨어뜨리면 됨.
    # Random Box 추가
    random_boxes = [
        Random_box(412, 180), #공중박스
        Random_box(464, 180), #공중박스
        
        #Random_box(626, 130),
        Random_box(714, 143), # 트롤박스
        Random_box(742, 143)  # 트롤박스
    ]
    game_world.add_objects(random_boxes, 1)

    # Gun Box 추가
    gun_boxes = [
        #Gun_box(742, 143),
        #Gun_box(750, 100)
    ]
    game_world.add_objects(gun_boxes, 1)

    # Clean Box 추가
    clean_boxes = [
        Clean_box(1392, 210),
        Clean_box(1420, 210),
        Clean_box(1448, 210)
    ]
    game_world.add_objects(clean_boxes, 1)  # 레이어 1에 Clean_box 추가

    # Boss_turtle 추가 (지정된 x, y 좌표로) - 이미 추가되었으므로 중복 제거

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

    for clean_box in clean_boxes:
        game_world.add_collision_pair('mario:clean_box_top', mario, clean_box)
        game_world.add_collision_pair('mario:clean_box_bottom', mario, clean_box)
        game_world.add_collision_pair('mario:clean_box_left', mario, clean_box)
        game_world.add_collision_pair('mario:clean_box_right', mario, clean_box)

    # Boss_turtle과 Mario 간의 충돌 쌍 등록
    game_world.add_collision_pair('mario:boss_turtle', mario, boss)

    # Boss_turtle과 Ball 간의 충돌 쌍 등록
    game_world.add_collision_pair('fire_ball:boss_turtle', [], [boss])
    print("'fire_ball:boss_turtle' 충돌 그룹이 추가되었습니다:", 'fire_ball:boss_turtle' in game_world.collision_pairs)
    print("fire_ball:boss_turtle 그룹의 Boss_turtles 수:", len(game_world.collision_pairs['fire_ball:boss_turtle'][1]))

    # Grass와 마리오의 충돌 쌍 등록
    game_world.add_collision_pair('mario:grass', mario, grasses)

    # 'fire_ball:turtle' 충돌 그룹 초기화
    game_world.add_collision_pair('fire_ball:turtle', [], turtlers)
    print("'fire_ball:turtle' 충돌 그룹이 추가되었습니다:", 'fire_ball:turtle' in game_world.collision_pairs)
    print("fire_ball:turtle 그룹의 Turtlers 수:", len(game_world.collision_pairs['fire_ball:turtle'][1]))

    # 'fire_ball:koomba' 충돌 그룹 초기화
    game_world.add_collision_pair('fire_ball:koomba', [], koombas)
    print("'fire_ball:koomba' 충돌 그룹이 추가되었습니다:", 'fire_ball:koomba' in game_world.collision_pairs)
    print("fire_ball:koomba 그룹의 Koombas 수:", len(game_world.collision_pairs['fire_ball:koomba'][1]))

    # 벽과 fire_ball의 충돌 그룹 등록
    # 'fire_ball:brick' 충돌 그룹 초기화
    game_world.add_collision_pair('fire_ball:brick', [], bricks)
    print("'fire_ball:brick' 충돌 그룹이 추가되었습니다:", 'fire_ball:brick' in game_world.collision_pairs)
    print("fire_ball:brick 그룹의 Bricks 수:", len(game_world.collision_pairs['fire_ball:brick'][1]))

    # 'fire_ball:clean_box' 충돌 그룹 초기화
    game_world.add_collision_pair('fire_ball:clean_box', [], clean_boxes)
    print("'fire_ball:clean_box' 충돌 그룹이 추가되었습니다:", 'fire_ball:clean_box' in game_world.collision_pairs)
    print("fire_ball:clean_box 그룹의 Clean_boxes 수:", len(game_world.collision_pairs['fire_ball:clean_box'][1]))

    # 'fire_ball:gun_box' 충돌 그룹 초기화
    game_world.add_collision_pair('fire_ball:gun_box', [], gun_boxes)
    print("'fire_ball:gun_box' 충돌 그룹이 추가되었습니다:", 'fire_ball:gun_box' in game_world.collision_pairs)
    print("fire_ball:gun_box 그룹의 Gun_boxes 수:", len(game_world.collision_pairs['fire_ball:gun_box'][1]))

    # 'fire_ball:random_box' 충돌 그룹 초기화
    game_world.add_collision_pair('fire_ball:random_box', [], random_boxes)
    print("'fire_ball:random_box' 충돌 그룹이 추가되었습니다:", 'fire_ball:random_box' in game_world.collision_pairs)
    print("fire_ball:random_box 그룹의 Random_boxes 수:", len(game_world.collision_pairs['fire_ball:random_box'][1]))

    # 배경음악 관리자 초기화
    bgm_manager = BGMManager()
    print("Loading background music...")  # 디버깅 출력
    bgm_manager.load_music('main_theme', 'resources/chetahman2.mp3')  # 변환된 파일 경로
    bgm_manager.play('main_theme', MarioConfig.GAME_MUSIC_VOLUME)
    print("Background music started.")  # 디버깅 출력

    camera = Camera(800, 600, MarioConfig.WORLD_WIDTH, MarioConfig.WORLD_HEIGHT)
    game_time = MarioConfig.GAME_TIME_LIMIT

def finish():
    global bgm_manager
    if bgm_manager:
        bgm_manager.stop()
    game_world.reset()  # game_world 완전 초기화
    print("play_mode의 finish()가 호출되었습니다.")  # 디버깅 출력

def update():
    global game_time, objects_to_add, mario_dead, death_timer

    game_world.update()            # 객체들의 위치 업데이트
    game_world.handle_collisions() # 충돌 처리
    camera.update(mario)           # 카메라 위치 업데이트

    # Mario의 dead 상태 확인 및 타이머 설정
    if mario.dead and not mario_dead:
        mario_dead = True
        death_timer = get_time()  # 사망 시각 기록
        print("Mario is dead. Stopping music and starting death timer.")
        if bgm_manager:
            bgm_manager.stop()  # 배경음악 명시적으로 중지
        game_state.lives -= 1  # 목숨 감소
        print(f"Mario has {game_state.lives} lives remaining.")

    # Mario가 사망한 상태이고, 타이머가 시작되었으며, 3초가 경과했을 때 게임 오버로 전환
    if mario_dead and death_timer is not None:
        elapsed_time = get_time() - death_timer
        if elapsed_time >= 3.0:  # 3초 지연
            if game_state.lives > 0:
                print("Lives remaining. Restarting the game.")
                game_framework.change_mode(logo_mode)
            else:
                print("No lives remaining. Game Over.")
                game_framework.change_mode(game_over)

    # 추가할 객체 처리
    for obj in objects_to_add:
        game_world.add_object(obj, 1)
        # 충돌 쌍 등록
        if isinstance(obj, Coin):
            game_world.add_collision_pair('mario:coin', mario, obj)
        elif isinstance(obj, Star):
            game_world.add_collision_pair('mario:star', mario, obj)
        elif isinstance(obj, Ball):
            # 기존의 'fire_ball:turtle', 'fire_ball:koomba' 그룹에 추가
            if 'fire_ball:turtle' in game_world.collision_pairs:
                game_world.collision_pairs['fire_ball:turtle'][0].append(obj)
            if 'fire_ball:koomba' in game_world.collision_pairs:
                game_world.collision_pairs['fire_ball:koomba'][0].append(obj)
            # 벽과의 충돌 그룹에 Ball 객체 추가
            if 'fire_ball:brick' in game_world.collision_pairs:
                game_world.collision_pairs['fire_ball:brick'][0].append(obj)
            if 'fire_ball:clean_box' in game_world.collision_pairs:
                game_world.collision_pairs['fire_ball:clean_box'][0].append(obj)
            if 'fire_ball:gun_box' in game_world.collision_pairs:
                game_world.collision_pairs['fire_ball:gun_box'][0].append(obj)
            if 'fire_ball:random_box' in game_world.collision_pairs:
                game_world.collision_pairs['fire_ball:random_box'][0].append(obj)
            # Boss_turtle과의 충돌 그룹에 Ball 객체 추가
            if 'fire_ball:boss_turtle' in game_world.collision_pairs:
                game_world.collision_pairs['fire_ball:boss_turtle'][0].append(obj)
        # 추가적인 객체 유형이 필요하면 여기서 추가
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

def draw():
    clear_canvas()
    game_world.render_with_camera(camera)  # 카메라를 고려하여 렌더링
    dashboard.draw(camera)                 # 대시보드 그리기
    update_canvas()

def pause():
    pass

def resume():
    pass

