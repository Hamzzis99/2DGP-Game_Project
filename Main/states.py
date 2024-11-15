# states.py
from pico2d import load_image, draw_rectangle
from sdl2 import SDLK_LEFT, SDLK_RIGHT
from state_machine import right_down, left_down, right_up, left_up, s_down

# 상수 정의는 상태 클래스보다 먼저
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixels = 0.3 meters
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

class Idle:
    @staticmethod
    def enter(mario, event):
        mario.dir = 0
        mario.frame = 0
        if event and isinstance(event, tuple):
            if left_up(event) or right_down(event):
                mario.face_dir = -1
            elif right_up(event) or left_down(event) or s_down(event):
                mario.face_dir = 1

    @staticmethod
    def exit(mario, event):
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
    def enter(mario, event):
        if event and isinstance(event, tuple):
            if right_down(event) or left_up(event):
                mario.dir, mario.face_dir = 1, 1
            elif left_down(event) or right_up(event):
                mario.dir, mario.face_dir = -1, -1
        mario.run_frame_x_positions = [290, 304, 321]
        mario.frame = 0

    @staticmethod
    def exit(mario, event):
        pass

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * mario.game_framework.frame_time) % len(mario.run_frame_x_positions)
        mario.x += mario.dir * RUN_SPEED_PPS * mario.game_framework.frame_time

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
    JUMP_VELOCITY = 200
    GRAVITY = -300

    @staticmethod
    def enter(mario, event):
        mario.jump_speed = Jump.JUMP_VELOCITY
        mario.jump_frame_x_positions = [336, 353, 321]
        mario.frame = 0
        if event and isinstance(event, tuple):
            if right_down(event):
                mario.dir = 1
                mario.face_dir = 1
            elif left_down(event):
                mario.dir = -1
                mario.face_dir = -1

    @staticmethod
    def exit(mario, event):
        mario.jump_speed = 0

    @staticmethod
    def do(mario):
        mario.y += mario.jump_speed * mario.game_framework.frame_time
        mario.jump_speed += Jump.GRAVITY * mario.game_framework.frame_time

        # 점프 종료 조건: y <=90
        if mario.y <= 90:
            mario.y = 90
            if SDLK_LEFT in mario.pressed_keys:
                mario.dir = -1
                mario.face_dir = -1
                mario.state_machine.set_state(Run)
            elif SDLK_RIGHT in mario.pressed_keys:
                mario.dir = 1
                mario.face_dir = 1
                mario.state_machine.set_state(Run)
            else:
                mario.state_machine.set_state(Idle)

        # Jump 상태에서도 수평 이동 처리
        if mario.dir != 0:
            mario.x += mario.dir * RUN_SPEED_PPS * mario.game_framework.frame_time

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
    def handle_event(mario, event):
        # Jump 상태에서는 방향키 입력을 자체적으로 처리하여 방향을 변경
        if right_down(event):
            mario.dir = 1
            mario.face_dir = 1
            print("Jump 상태: 오른쪽 방향키 입력 감지")
        elif left_down(event):
            mario.dir = -1
            mario.face_dir = -1
            print("Jump 상태: 왼쪽 방향키 입력 감지")
        elif right_up(event) or left_up(event):
            mario.dir = 0
            print("Jump 상태: 방향키 뗌 감지")
