# play_mode.py

from pico2d import *
import game_framework
import game_world
import logo_mode
import thank_you
import world_start_mode
from ball import Ball
from grass import Grass
from enemy.koomba import Koomba
from enemy.turtle import Turtle
from enemy.boss_turtle import Boss_turtle  # Boss_turtle 임포트
from items.mushroom import Mushroom
from mario import Mario, reset_mario, Idle, Run, Jump, Dead  # 상태 클래스 임포트 추가
from props.brick import Brick
from props.castle import Castle
from props.fake_brick import Fake_brick
from props.mushroom_box import Mushroom_box
from props.random_box import Random_box
from props.gun_box import Gun_box
from props.clean_box import Clean_box
from props.flag import Flag  # Flag 임포트 추가
from items.star import Star
from items.coin import Coin
from states import game_state, reset_game  # GameState 및 reset_game 임포트
from utils.camera import Camera
from utils.config import MarioConfig  # 수정된 부분
from utils.dashboard import Dashboard
from utils.bgm import BGMManager
import game_over

# ===== 상수 정의 =====
BOSS_TRIGGER_X = 4300  # 보스 등장 트리거 x 좌표 (원래 9000에서 5250으로 변경 예정)
BOSS_EVENT_DURATION = 2.0  # 보스 등장 이벤트 지속 시간 (초)
FADE_DURATION = 1.0  # 페이드 아웃 지속 시간 (초)
WIN_SEQUENCE_DELAY = 6.0  # 승리 시퀀스 지연 시간 (초)
CASTLE_X = 4300  # 캐슬의 x 좌표
CASTLE_Y = 226    # 캐슬의 y 좌표
CASTLE_SCALE = 2.0  # 캐슬의 스케일 팩터
FLAG_X = 4100  # Flag의 x 좌표
FLAG_Y = 176   # Flag의 y 좌표
FLAG_SCALE = 0.5  # Flag의 스케일 팩터
# ======================

# 전역 변수 선언
camera = None  # 전역 카메라 객체
dashboard = None  # 전역 대시보드 객체
bgm_manager = None  # 배경음악 관리자 객체
objects_to_add = []  # 추가할 객체 리스트
mario_dead = False  # Mario의 사망 상태 플래그
death_timer = None  # Mario 사망 시각 기록

# 보스 이벤트 관련 변수
boss_event_triggered = False
boss_event_completed = False  # 보스 이벤트 완료 플래그 추가
boss_event_start_time = None

# 음악 페이드 아웃 관련 변수
is_fading_out = False
fade_start_time = None
fade_duration = FADE_DURATION  # 페이드 아웃 지속 시간 (초)
initial_volume_int = MarioConfig.GAME_MUSIC_VOLUME  # 초기 볼륨 (정수)

# 보스 사망 시 승리 시퀀스 관련 변수 추가
win_sequence_started = False
is_win_fading_out = False
win_fade_start_time = None
win_timer_start_time = None

# 보스 사망 상태 변수 추가
boss_dead = False  # 보스의 사망 상태를 나타내는 변수

# 배경 이미지 전역 변수 추가
background = None

def handle_events():
    global mario
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            # [디버깅] Quit 이벤트 감지
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            # [디버깅] Escape 키 눌림
            game_framework.quit()
        elif event.type in (SDL_KEYDOWN, SDL_KEYUP):
            # [디버깅] 키 이벤트 발생
            mario.handle_event(event)  # 키 이벤트만 마리오에게 전달

def init():
    global mario, camera, dashboard, bgm_manager, mario_dead, death_timer
    global boss_event_triggered, boss_event_start_time, boss_event_completed
    global is_fading_out, fade_start_time, initial_volume_int
    global win_sequence_started, is_win_fading_out, win_fade_start_time, win_timer_start_time
    global boss_dead  # 보스 사망 상태 변수 추가
    global background  # 배경 이미지 전역 변수

    mario_dead = False  # 초기화 시 dead 플래그 초기화
    death_timer = None  # 초기화 시 타이머 초기화
    boss_event_triggered = False  # 초기화 시 보스 이벤트 트리거 플래그 초기화
    boss_event_completed = False  # 초기화 시 보스 이벤트 완료 플래그 초기화
    boss_event_start_time = None  # 초기화 시 보스 이벤트 시작 시간 초기화
    is_fading_out = False  # 초기화 시 페이드 아웃 플래그 초기화
    fade_start_time = None  # 초기화 시 페이드 아웃 시작 시간 초기화
    initial_volume_int = MarioConfig.GAME_MUSIC_VOLUME  # 초기 볼륨 설정

    # 승리 시퀀스 초기화
    win_sequence_started = False
    is_win_fading_out = False
    win_fade_start_time = None
    win_timer_start_time = None

    boss_dead = False  # 보스 사망 상태 초기화

    game_world.clear()  # 게임 월드 초기화

    # 배경 이미지 로드
    background = load_image('map/map.png')  # 배경 이미지 경로 확인
    print("[디버깅] 배경 이미지 로드 완료.")

    # Grass 객체 생성 및 추가
    grasses = []
    grass_positions = [
        (0, 30, 600),
        (880, 30, 500),
        (1900, 30, 400),
        (2700, 30, 800),
        (4200, 30, 800),
        (5150, 30, 750),
        (6400, 30, 1100)
    ]
    for x, y, width in grass_positions:
        grass = Grass()
        grass.x = x
        grass.y = y
        grass.width = width
        grasses.append(grass)
        game_world.add_object(grass, 0)

    # Castle 객체 생성 및 추가
    castle = Castle(x=CASTLE_X, y=CASTLE_Y, scale=CASTLE_SCALE)
    game_world.add_object(castle, 0)  # 레이어 0에 추가 (배경 요소)

    # Flag 객체 생성 및 추가
    flag = Flag(x=FLAG_X, y=FLAG_Y, scale=FLAG_SCALE)
    game_world.add_object(flag, 0)  # 레이어 0에 추가 (배경 요소)

    dashboard = Dashboard()  # Dashboard 인스턴스 생성

    mario = Mario(dashboard)  # Dashboard 인스턴스를 Mario에게 전달
    game_world.add_object(mario, 1)

    # Koombas 추가
    koombas = [
        Koomba(630, 70, 450),
        Koomba(700, 70, 400),
        Koomba(700, 70, 300),
        Koomba(800, 70, 300),
        Koomba(900, 70, 200),

        Koomba(2325, 70, 300),
        Koomba(2325, 70, 400),
        Koomba(2375, 70, 700),
        Koomba(2375, 70, 600),
        Koomba(2475, 70, 600),
        Koomba(2475, 70, 500),
        Koomba(2475, 70, 500),
        Koomba(2575, 70, 400),

        # Fake Brick 함정
        Koomba(3268, 218, 200),
        Koomba(3308, 218, 100),

        # Boss Run 1
        Koomba(5530, 112, 0),

        # Boss Run 2
        Koomba(6516, 162, 100),
        Koomba(6524, 162, 150),

        Koomba(6544, 242, 100),
        Koomba(6554, 242, 100),
    ]
    game_world.add_objects(koombas, 1)

    # Turtle 추가
    turtlers = [
        Turtle(1715, 70, 350),  # x : 1715 y = 70, distance = 360
        Turtle(1760, 160, 220),
        Turtle(1795, 250, 170),

        Turtle(2325, 70, 500),
        Turtle(2525, 70, 300),
        #Turtle(2425, 70, 500),
        #Turtle(2525, 70, 400),
        Turtle(5558, 140, 0),
    ]
    game_world.add_objects(turtlers, 1)

    # 벽돌 추가
    bricks = [
        Brick(360, 100),
        Brick(386, 100),
        Brick(412, 100),
        Brick(438, 100),
        Brick(438, 180),  # 공중벽
        Brick(464, 100),
        Brick(490, 100),
        Brick(516, 100),

        # 징검다리
        Brick(1145, 70),
        Brick(1168, 98),
        Brick(1196, 126),
        Brick(1224, 156),
        Brick(1252, 184),
        Brick(1280, 210),
        Brick(1308, 210),
        Brick(1504, 210),
        Brick(1532, 210),
        Brick(1560, 182),
        Brick(1588, 154),
        Brick(1616, 126),
        Brick(1644, 98),
        Brick(1672, 80),

        # 거북이 함정 중간줄
        Brick(1759, 130),
        Brick(1787, 130),
        Brick(1815, 130),
        Brick(1843, 130),
        Brick(1871, 130),
        Brick(1899, 130),
        Brick(1927, 130),
        Brick(1955, 130),
        Brick(1983, 130),
        Brick(2011, 130),

        # 거북이 함정 3층
        Brick(1787, 220),
        Brick(1815, 220),
        Brick(1843, 220),
        Brick(1871, 220),
        Brick(1899, 220),
        Brick(1927, 220),
        Brick(1955, 220),
        Brick(1983, 220),

        # Gun Box 부분
        Brick(2150, 160),
        Brick(2262, 160),

        # Fake Brick 함정
        Brick(3100, 75),
        Brick(3128, 103),
        Brick(3156, 131),
        Brick(3184, 159),

        # 계단 인덱스 순서
        Brick(3212, 187),
        Brick(3240, 187),
        Brick(3268, 187),
        Brick(3492, 187),
        Brick(3520, 187),
        Brick(3548, 187),

        # Boss전
        Brick(5530, 84),
        Brick(5558, 112),
        Brick(5586, 140),
        Brick(5698, 140), # Fake Block 영역

        # Boss전 2차
        # Boss Area
        Brick(6514, 130),  # Gun Box 대체 Randombox
        Brick(6542, 130),  # Gun Box 대체 Randombox
        Brick(6658, 130),  # Gun Box 대체 Randombox
        Brick(6686, 130),  # Gun Box 대체 Randombox

        Brick(6544, 210),  # Gun Box 대체 Randombox
        Brick(6656, 210),  # Gun Box 대체 Randombox
    ]
    game_world.add_objects(bricks, 1)

    # Random Box 추가
    random_boxes = [
        Random_box(412, 180),  # 공중박스
        Random_box(464, 180),  # 공중박스

        Random_box(714, 143),  # 트롤박스
        Random_box(742, 143),  # 트롤박스

        # 징검다리 함정
        Random_box(1336, 210),
        Random_box(1476, 210),

        # Gun Box 다리
        Random_box(2122, 40),
        Random_box(2150, 40),
        Random_box(2178, 40),
        Random_box(2206, 40),
        Random_box(2234, 40),
        Random_box(2262, 40),
        Random_box(2290, 40),  # 트롤박스

        # Fake Brick 영역
        Random_box(3240, 187),  # Randombox
        Random_box(3492, 187),  # Random box 중간줄2층

        Random_box(3436, 277),  # Random box 3층

        # Boss Area 2층
        Random_box(6566, 130),  # Gun Box 대체 Randombox
        Random_box(6634, 130),  # Gun Box 대체 Randombox

        # Boss Area 3층
        Random_box(6572, 210),  # Gun Box 대체 Randombox
        Random_box(6600, 210),  # Gun Box 대체 Randombox
        Random_box(6628, 210),  # Gun Box 대체 Randombox
    ]
    game_world.add_objects(random_boxes, 1)

    # Gun Box 추가
    gun_boxes = [
        # Turtle 영역
        Gun_box(2206, 160),

        # FakeBrick 영역
        Gun_box(3268, 277),  # Gun Box 대체 Randombox

        #Boss Fight
        Gun_box(5200, 130),  # Gun Box 대체 Randombox
        Gun_box(5228, 130),  # Gun Box 대체 Randombox

        #BOSS GUN BOX
        Gun_box(6600, 129),  # Gun Box 대체 Randombox
    ]
    game_world.add_objects(gun_boxes, 1)

    # Clean Box 추가
    clean_boxes = [
        Clean_box(1364, 210),
        Clean_box(1392, 210),
        Clean_box(1420, 210),
        Clean_box(1448, 210),

        Clean_box(5614, 140),  # Fake Block 영역
        Clean_box(5642, 140),  # Fake Block 영역
        Clean_box(5670, 140),  # Fake Block 영역
    ]
    game_world.add_objects(clean_boxes, 1)  # 레이어 1에 Clean_box 추가

    # Fake Brick 추가
    fake_bricks = [
        # 첫번째 Fake Brick
        Fake_brick(3296, 187),
        Fake_brick(3324, 187),  # 2층
        Fake_brick(3352, 187),
        Fake_brick(3380, 187),
        Fake_brick(3408, 187),
        Fake_brick(3436, 187),
        Fake_brick(3464, 187),

        Fake_brick(3296, 277),
        Fake_brick(3324, 277),  # 다섯개 FakeBrick 영역
        Fake_brick(3352, 277),
        Fake_brick(3380, 277),
        Fake_brick(3408, 277)
    ]
    game_world.add_objects(fake_bricks, 1)



    mushroom_boxes = [
        # Mushroom Box
        Mushroom_box(30, 130),
    ]
    game_world.add_objects(mushroom_boxes, 1)

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

    for fake_brick in fake_bricks:
        game_world.add_collision_pair('mario:fake_brick_top', mario, fake_brick)
        game_world.add_collision_pair('mario:fake_brick_bottom', mario, fake_brick)
        game_world.add_collision_pair('mario:fake_brick_left', mario, fake_brick)
        game_world.add_collision_pair('mario:fake_brick_right', mario, fake_brick)


    for mushroom_box in mushroom_boxes:
        game_world.add_collision_pair('mario:mushroom_box_top', mario, mushroom_box)
        game_world.add_collision_pair('mario:mushroom_box_bottom', mario, mushroom_box)
        game_world.add_collision_pair('mario:mushroom_box_left', mario, mushroom_box)
        game_world.add_collision_pair('mario:mushroom_box_right', mario, mushroom_box)

    # Grass와 마리오의 충돌 쌍 등록
    game_world.add_collision_pair('mario:grass', mario, grasses)

    # 'fire_ball:turtle' 충돌 그룹 초기화
    game_world.add_collision_pair('fire_ball:turtle', [], turtlers)
    print("[디버깅] 'fire_ball:turtle' 충돌 그룹이 추가되었습니다:", 'fire_ball:turtle' in game_world.collision_pairs)
    print("[디버깅] fire_ball:turtle 그룹의 Turtlers 수:", len(game_world.collision_pairs['fire_ball:turtle'][1]))

    # 'fire_ball:koomba' 충돌 그룹 초기화
    game_world.add_collision_pair('fire_ball:koomba', [], koombas)
    print("[디버깅] 'fire_ball:koomba' 충돌 그룹이 추가되었습니다:", 'fire_ball:koomba' in game_world.collision_pairs)
    print("[디버깅] fire_ball:koomba 그룹의 Koombas 수:", len(game_world.collision_pairs['fire_ball:koomba'][1]))

    # 벽과 fire_ball의 충돌 그룹 등록
    # 'fire_ball:brick' 충돌 그룹 초기화
    game_world.add_collision_pair('fire_ball:brick', [], bricks)
    print("[디버깅] 'fire_ball:brick' 충돌 그룹이 추가되었습니다:", 'fire_ball:brick' in game_world.collision_pairs)
    print("[디버깅] fire_ball:brick 그룹의 Bricks 수:", len(game_world.collision_pairs['fire_ball:brick'][1]))

    # 'fire_ball:clean_box' 충돌 그룹 초기화
    game_world.add_collision_pair('fire_ball:clean_box', [], clean_boxes)
    print("[디버깅] 'fire_ball:clean_box' 충돌 그룹이 추가되었습니다:", 'fire_ball:clean_box' in game_world.collision_pairs)
    print("[디버깅] fire_ball:clean_box 그룹의 Clean_boxes 수:", len(game_world.collision_pairs['fire_ball:clean_box'][1]))

    # 'fire_ball:gun_box' 충돌 그룹 초기화
    game_world.add_collision_pair('fire_ball:gun_box', [], gun_boxes)
    print("[디버깅] 'fire_ball:gun_box' 충돌 그룹이 추가되었습니다:", 'fire_ball:gun_box' in game_world.collision_pairs)
    print("[디버깅] fire_ball:gun_box 그룹의 Gun_boxes 수:", len(game_world.collision_pairs['fire_ball:gun_box'][1]))

    # 'fire_ball:random_box' 충돌 그룹 초기화
    game_world.add_collision_pair('fire_ball:random_box', [], random_boxes)
    print("[디버깅] 'fire_ball:random_box' 충돌 그룹이 추가되었습니다:", 'fire_ball:random_box' in game_world.collision_pairs)
    print("[디버깅] fire_ball:random_box 그룹의 Random_boxes 수:", len(game_world.collision_pairs['fire_ball:random_box'][1]))

    # 배경음악 관리자 초기화
    bgm_manager = BGMManager()
    print("[디버깅] 배경음악 로딩 중...")
    bgm_manager.load_music('main_theme', 'resources/chetahman2.mp3')  # 기존 음악 로드
    bgm_manager.load_music('boss_theme', 'resources/boss_theme.mp3')  # 새로운 보스 음악 로드
    bgm_manager.load_music('win_music', 'resources/win_music.mp3')  # 승리 음악 로드
    bgm_manager.play('main_theme', MarioConfig.GAME_MUSIC_VOLUME)
    print("[디버깅] 배경음악 시작됨.")

    # 카메라 초기화
    camera = Camera(800, 600, MarioConfig.WORLD_WIDTH, MarioConfig.WORLD_HEIGHT)  # 수정된 부분
    # game_time = MarioConfig.GAME_TIME_LIMIT  # 제거 (game_state에서 관리)

def finish():
    global bgm_manager
    if bgm_manager:
        bgm_manager.stop()
    game_world.reset()  # game_world 완전 초기화
    print("[디버깅] play_mode의 finish()가 호출되었습니다.")  # 디버깅 출력

def update():
    global objects_to_add, mario_dead, death_timer
    global boss_event_triggered, boss_event_start_time, boss_event_completed
    global is_fading_out, fade_start_time, initial_volume_int
    global win_sequence_started, is_win_fading_out, win_fade_start_time, win_timer_start_time
    global boss_dead  # 보스 사망 상태 변수 추가

    game_world.update()  # 객체들의 위치 업데이트
    game_world.handle_collisions()  # 충돌 처리
    camera.update(mario)  # 카메라 위치 업데이트

    # 보스 등장 이벤트 트리거링
    if not boss_event_triggered and not boss_event_completed and mario.x > BOSS_TRIGGER_X:
        boss_event_triggered = True
        boss_event_start_time = get_time()
        mario.dir = 0  # 마리오의 방향을 0으로 설정하여 움직임 중지
        mario.state_machine.set_state(Idle)  # 마리오 상태를 Idle로 변경
        camera.start_shake(duration=BOSS_EVENT_DURATION, magnitude=10)  # 카메라 흔들기 시작
        is_fading_out = True  # 페이드 아웃 시작
        fade_start_time = get_time()  # 페이드 아웃 시작 시간 기록
        initial_volume_int = bgm_manager.get_volume() if bgm_manager else MarioConfig.GAME_MUSIC_VOLUME  # 현재 볼륨 가져오기
        print("[디버깅] 마리오 x > BOSS_TRIGGER_X 넘음 보스 등장 디버깅")

    # 페이드 아웃 처리
    if is_fading_out:
        elapsed_time = get_time() - fade_start_time
        if elapsed_time < fade_duration:
            # 선형으로 볼륨 감소
            new_volume = initial_volume_int * (1 - elapsed_time / fade_duration)
            new_volume_int = int(new_volume)  # 정수로 변환
            bgm_manager.set_volume(new_volume_int)
            #print(f"[디버깅] Fading out music... Volume: {new_volume_int}")
        else:
            # 페이드 아웃 완료
            bgm_manager.set_volume(0)  # 볼륨을 0으로 설정
            bgm_manager.stop()
            is_fading_out = False
            #print("[디버깅] Music has been faded out and stopped.")

            # 새로운 보스 음악 재생
            if bgm_manager:
                bgm_manager.play('boss_theme', MarioConfig.GAME_MUSIC_VOLUME)
                print("[디버깅] 보스 테마 뮤직 시작.")

    # 보스 등장 이벤트 동안 Mario의 움직임을 잠시 중지
    if boss_event_triggered and boss_event_start_time is not None:
        elapsed_time = get_time() - boss_event_start_time
        if elapsed_time < BOSS_EVENT_DURATION:
            # BOSS_EVENT_DURATION 초 동안 Mario의 움직임을 잠시 중지 (이미 dir=0으로 설정됨)
            pass  # 추가 로직이 필요하다면 여기에 작성
        elif elapsed_time >= BOSS_EVENT_DURATION and not boss_event_completed:
            # 흔들기 종료
            camera.is_shaking = False
            boss_event_triggered = False
            boss_event_start_time = None
            boss_event_completed = True  # 보스 이벤트 완료 플래그 설정
            print("[디버깅] Boss Appearance Event Ended: Camera shaking stopped.")

            # 보스의 등장
            boss = Boss_turtle(scale=20.0, initial_y=300)  # 보스 생성 (scale=20, y=300)
            boss.x = 4100  # (보스 등장) 보스의 x 좌표 설정
            game_world.add_object(boss, 1)

            # 보스와의 충돌 쌍 등록
            game_world.add_collision_pair('mario:boss_turtle', mario, boss)
            game_world.add_collision_pair('fire_ball:boss_turtle', [], [boss])
            print("[디버깅] Boss Appearance Event Completed.")

    # 보스의 사망 여부를 확인하고 승리 시퀀스 시작
    if not win_sequence_started and boss_event_completed:
        boss = game_world.find_object_by_type(Boss_turtle)
        if boss:
            if boss.dead:
                win_sequence_started = True
                mario.dir = 0  # 마리오의 움직임을 중지
                mario.state_machine.set_state(Idle)  # 마리오 상태를 Idle로 변경
                is_win_fading_out = True
                win_fade_start_time = get_time()
                initial_volume_int = bgm_manager.get_volume() if bgm_manager else MarioConfig.GAME_MUSIC_VOLUME
                print("[디버깅] 보스가 죽었습니다. 승리 시퀀스 시작.")
        else:
            print("[디버깅] 보스가 탐색되지 않음. 보스 호출 망가짐.")

    # 승리 시퀀스: 보스 테마 페이드 아웃
    if is_win_fading_out:
        elapsed_time = get_time() - win_fade_start_time
        if elapsed_time < FADE_DURATION:
            # 선형으로 볼륨 감소
            new_volume = initial_volume_int * (1 - elapsed_time / FADE_DURATION)
            new_volume_int = int(new_volume)  # 정수로 변환
            bgm_manager.set_volume(new_volume_int)
            print(f"[디버깅] 보스 테마 뮤직 페이드 아웃 중... 볼륨: {new_volume_int}")
        else:
            # 페이드 아웃 완료
            bgm_manager.set_volume(0)  # 볼륨을 0으로 설정
            bgm_manager.stop()
            is_win_fading_out = False
            print("[디버깅] 보스 테마 뮤직 페이드 아웃 완료 및 중지됨.")

            # 승리 음악 재생
            if bgm_manager:
                bgm_manager.play('win_music', MarioConfig.GAME_MUSIC_VOLUME)
                print("[디버깅] 승리 음악 시작됨.")
                win_timer_start_time = get_time()  # 타이머 시작

            # 보스 객체 제거
            boss = game_world.find_object_by_type(Boss_turtle)
            if boss:
                game_world.remove_object(boss)
                print("[디버깅] Boss Turtle이 게임 월드에서 제거되었습니다.")

    # 승리 음악 재생 후 6초 후에 thank_you 화면으로 전환
    if win_timer_start_time is not None:
        elapsed_time = get_time() - win_timer_start_time
        if elapsed_time >= WIN_SEQUENCE_DELAY:
            print("[디버깅] 승리 시퀀스 완료. thank_you 화면으로 전환.")
            game_framework.change_mode(thank_you)

    # Mario의 dead 상태 확인 및 타이머 설정
    if mario.dead and not mario_dead:
        mario_dead = True
        death_timer = get_time()  # 사망 시각 기록
        print("[디버깅] Mario가 사망했습니다. 음악 중지 및 사망 타이머 시작.")
        if bgm_manager:
            bgm_manager.stop()  # 배경음악 명시적으로 중지
        game_state.lives -= 1  # 목숨 감소
        print(f"[디버깅] Mario의 남은 목숨: {game_state.lives}")

    # Mario가 사망한 상태이고, 타이머가 시작되었으며, 3초가 경과했을 때 게임 재시작 또는 게임 오버로 전환
    if mario_dead and death_timer is not None:
        elapsed_time = get_time() - death_timer
        if elapsed_time >= 3.0:  # 3초 지연
            if game_state.lives > 0:
                print("[디버깅] 목숨이 남아있습니다. 게임을 재시작합니다.")
                reset_game()  # GameState를 초기화하지 않고, 게임 상태를 유지
                game_framework.change_mode(world_start_mode)  # 초기 화면으로 변경하여 게임 재시작
            else:
                print("[디버깅] 목숨이 남아있지 않습니다. 게임 오버 화면으로 전환합니다.")
                game_framework.change_mode(game_over)

    # 추가할 객체 처리
    for obj in objects_to_add:
        game_world.add_object(obj, 1)
        # 충돌 쌍 등록
        if isinstance(obj, Coin):
            game_world.add_collision_pair('mario:coin', mario, obj)
        elif isinstance(obj, Star):
            game_world.add_collision_pair('mario:star', mario, obj)
        elif isinstance(obj, Mushroom):
            game_world.add_collision_pair('mario:mushroom', mario, obj)
            game_world.add_collision_pair('fire_ball:mushroom', [], [obj])
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
    game_state.game_time -= game_framework.frame_time
    if game_state.game_time <= 0 and not mario.dead:
        game_state.game_time = 0
        dashboard.set_time(int(game_state.game_time))
        dashboard.update()
        print("[디버깅] 시간이 다 되었습니다! Mario가 사망합니다.")
        if bgm_manager:
            bgm_manager.stop()  # 배경음악 중지

        # 마리오를 죽은 상태로 변경하고 사망 애니메이션 시작
        mario.dead = True
        mario.state_machine.set_state(Dead())
        # mario_dead = True  # 이 줄을 제거합니다.
        death_timer = get_time()
        print("[디버깅] Mario가 시간 초과로 사망했습니다. 사망 애니메이션 시작.")

    # 대시보드에 현재 게임 시간 설정
    dashboard.set_time(int(game_state.game_time))  # 정수로 전달

    # 대시보드 업데이트
    dashboard.update()

def draw():
    clear_canvas()

    # 배경 그리기
    if background:
        # 배경 이미지를 게임 월드의 중앙에 맞추어 그립니다.
        # 배경 이미지의 중앙은 (MarioConfig.WORLD_WIDTH // 2, MarioConfig.WORLD_HEIGHT // 2)
        # 카메라의 위치에 따라 배경을 고정시키려면, 배경은 카메라의 움직임과 무관하게 그립니다.
        # 여기서는 배경을 월드의 중앙에 고정하여 그립니다.
        background.draw(MarioConfig.WORLD_WIDTH // 2, MarioConfig.WORLD_HEIGHT // 2, MarioConfig.WORLD_WIDTH, MarioConfig.WORLD_HEIGHT)
        # 배경은 항상 가장 먼저 그려져야 다른 객체들이 그 위에 표시됩니다.

    game_world.render_with_camera(camera)  # 카메라를 고려하여 렌더링
    dashboard.draw(camera)  # 대시보드 그리기
    update_canvas()

def pause():
    pass

def resume():
    pass