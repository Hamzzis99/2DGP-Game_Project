# states.py
from pico2d import draw_rectangle
from state_machine import right_down, left_down, right_up, left_up, s_down
from sdl2 import SDLK_LEFT, SDLK_RIGHT

# Constants
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_PPS = (RUN_SPEED_KMPH * 1000 / 60 / 60) * PIXEL_PER_METER
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

class Idle:
    @staticmethod
    def enter(mario, e):
        mario.dir = 0
        mario.frame = 0

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
                frame_x, frame_y, frame_width, frame_height,
                mario.x, mario.y, frame_width * 3, frame_height * 3
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
                frame_x, frame_y, frame_width, frame_height,
                mario.x, mario.y, frame_width * 3, frame_height * 3
            )

class Jump:
    JUMP_VELOCITY = 350
    GRAVITY = -700

    @staticmethod
    def enter(mario, e):
        if e is not None and isinstance(e, tuple):
            if s_down(e):
                mario.jump_speed = Jump.JUMP_VELOCITY
                mario.is_jumping = True
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

    @staticmethod
    def do(mario):
        mario.y += mario.jump_speed * mario.game_framework.frame_time
        mario.jump_speed += Jump.GRAVITY * mario.game_framework.frame_time

        if mario.dir != 0:
            mario.x += mario.dir * RUN_SPEED_PPS * mario.game_framework.frame_time
            mario.x = max(0, min(800, mario.x))

        if mario.y <= 90:
            mario.y = 90
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
                frame_x, frame_y, frame_width, frame_height,
                mario.x, mario.y, frame_width * 3, frame_height * 3
            )
