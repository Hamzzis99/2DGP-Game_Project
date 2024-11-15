# states.py
from pico2d import draw_rectangle
from sdl2 import SDLK_LEFT, SDLK_RIGHT
from state_machine import right_down, left_down, right_up, left_up, s_down

# 상수 정의는 상태 클래스보다 먼저
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

class Idle:
    @staticmethod
    def enter(mario, e):
        mario.dir = 0
        mario.frame = 0
        if e is not None and isinstance(e, tuple):
            if left_up(e) or right_down(e):
                mario.face_dir = -1
            elif right_up(e) or left_down(e) or s_down(e):
                mario.face_dir = 1

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        pass

    @staticmethod
    def draw(mario):
        frame_width = 16
        frame_height = 16
        frame_x = 276
        frame_y = 342
        if mario.face_dir == -1:
            mario.image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                mario.x, mario.y, frame_width * 3, frame_height * 3
            )
        else:
            mario.image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, mario.x, mario.y,
                frame_width * 3, frame_height * 3
            )

class Run:
    @staticmethod
    def enter(mario, e):
        if e is not None and isinstance(e, tuple):
            if right_down(e) or left_up(e):
                mario.dir, mario.face_dir = 1, 1
            elif left_down(e) or right_up(e):
                mario.dir, mario.face_dir = -1, -1
        mario.run_frame_x_positions = [290, 304, 321]

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * mario.game_framework.frame_time) % len(mario.run_frame_x_positions)
        mario.x += mario.dir * RUN_SPEED_PPS * mario.game_framework.frame_time
        # 화면 경계 제한 (화면 너비 800 가정)
        mario.x = max(0, min(800, mario.x))

    @staticmethod
    def draw(mario):
        frame_width = 16
        frame_height = 16
        frame_y = 342
        frame_x = mario.run_frame_x_positions[int(mario.frame)]
        if mario.face_dir == -1:
            mario.image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                mario.x, mario.y, frame_width * 3, frame_height * 3
            )
        else:
            mario.image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, mario.x, mario.y,
                frame_width * 3, frame_height * 3
            )

class Jump:
    JUMP_VELOCITY = 350  # 점프 속도 조정
    GRAVITY = -700       # 중력 조정

    @staticmethod
    def enter(mario, e):
        if e is not None and isinstance(e, tuple):
            if s_down(e):
                mario.jump_speed = Jump.JUMP_VELOCITY
                mario.is_jumping = True
                print("Jump 상태: 점프 시작")
            if right_down(e):
                mario.dir = 1
                mario.face_dir = 1
            elif left_down(e):
                mario.dir = -1
                mario.face_dir = -1
        mario.jump_frame_x_positions = [336, 353, 321]
        mario.frame = 0

    @staticmethod
    def exit(mario, e):
        mario.jump_speed = 0
        mario.is_jumping = False
        print("Jump 상태: 점프 종료")

    @staticmethod
    def do(mario):
        # 수직 이동 처리
        mario.y += mario.jump_speed * mario.game_framework.frame_time
        mario.jump_speed += Jump.GRAVITY * mario.game_framework.frame_time

        # 수평 이동 처리
        if mario.dir != 0:
            mario.x += mario.dir * RUN_SPEED_PPS * mario.game_framework.frame_time
            # 화면 경계 제한 (화면 너비 800 가정)
            mario.x = max(0, min(800, mario.x))

        # 착지 조건
        if mario.y <= 90:
            mario.y = 90
            # 현재 눌려 있는 방향키에 따라 상태 전환
            if SDLK_LEFT in mario.pressed_keys and SDLK_RIGHT not in mario.pressed_keys:
                mario.dir = -1
                mario.face_dir = -1
                mario.state_machine.set_state(Run)
            elif SDLK_RIGHT in mario.pressed_keys and SDLK_LEFT not in mario.pressed_keys:
                mario.dir = 1
                mario.face_dir = 1
                mario.state_machine.set_state(Run)
            else:
                mario.dir = 0
                mario.state_machine.set_state(Idle)

        # 애니메이션 프레임 업데이트
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * mario.game_framework.frame_time) % 3

    @staticmethod
    def draw(mario):
        frame_width = 16
        frame_height = 16
        frame_y = 342
        frame_x = mario.jump_frame_x_positions[int(mario.frame)]
        if mario.face_dir == -1:
            mario.image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                mario.x, mario.y, frame_width * 3, frame_height * 3
            )
        else:
            mario.image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, mario.x, mario.y,
                frame_width * 3, frame_height * 3
            )

    @staticmethod
    def handle_event(mario, e):
        # 현재 눌려 있는 키 상태를 기반으로 방향 설정
        left_pressed = SDLK_LEFT in mario.pressed_keys
        right_pressed = SDLK_RIGHT in mario.pressed_keys

        if left_pressed and not right_pressed:
            mario.dir = -1
            mario.face_dir = -1
            print("Jump 상태: 왼쪽 방향키 입력 감지")
        elif right_pressed and not left_pressed:
            mario.dir = 1
            mario.face_dir = 1
            print("Jump 상태: 오른쪽 방향키 입력 감지")
        else:
            mario.dir = 0
            print("Jump 상태: 방향키 뗌 또는 양쪽 방향키 동시 입력")
