# mario.py
from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_s
import game_framework
from state_machine import StateMachine, right_down, left_down, right_up, left_up, s_down

# 상태 클래스들을 Mario 클래스 외부로 이동

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
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(mario.run_frame_x_positions)
        mario.x += mario.dir * RUN_SPEED_PPS * game_framework.frame_time

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
    def enter(mario, e):
        mario.jump_speed = Jump.JUMP_VELOCITY
        mario.jump_frame_x_positions = [336, 353, 321]
        mario.frame = 0
        # 방향 설정
        if e is not None and isinstance(e, tuple):
            if right_down(e):
                mario.dir = 1
                mario.face_dir = 1
            elif left_down(e):
                mario.dir = -1
                mario.face_dir = -1

    @staticmethod
    def exit(mario, e):
        mario.jump_speed = 0
        # mario.dir = 0  # 기존의 dir 초기화 제거

    @staticmethod
    def do(mario):
        mario.y += mario.jump_speed * game_framework.frame_time
        mario.jump_speed += Jump.GRAVITY * game_framework.frame_time

        # 점프 종료 조건: y <=90
        if mario.y <= 90:
            mario.y = 90
            # 점프가 끝난 후 현재 눌려 있는 방향키에 따라 상태 전환
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

        if mario.dir != 0:
            mario.x += mario.dir * RUN_SPEED_PPS * game_framework.frame_time

        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

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
        if right_down(e):
            mario.dir = 1
            mario.face_dir = 1
        elif left_down(e):
            mario.dir = -1
            mario.face_dir = -1
        elif right_up(e) or left_up(e):
            mario.dir = 0

class Mario:
    def __init__(self):
        self.x, self.y = 400, 90  # 초기 Y 좌표 직접 설정
        self.face_dir = 1
        self.dir = 0  # 이동 방향: -1 (왼쪽), 0 (정지), 1 (오른쪽)
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {
                right_down: Run,
                left_down: Run,
                left_up: Run,
                right_up: Run,
                s_down: Jump
            },
            Run: {
                right_down: Idle,
                left_down: Idle,
                right_up: Idle,
                left_up: Idle,
                s_down: Jump
            },
            Jump: {
                right_down: Jump,  # 방향키 누름 (오른쪽)
                left_down: Jump,   # 방향키 누름 (왼쪽)
                right_up: Jump,    # 방향키 뗌 (오른쪽)
                left_up: Jump      # 방향키 뗌 (왼쪽)
            }
        })
        self.pressed_keys = set()  # 현재 눌려 있는 키 추적

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 키 상태 추적
        if event.type == SDL_KEYDOWN:
            if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_s):
                self.pressed_keys.add(event.key)
                # print(f"Key Down: {event.key}, Pressed Keys: {self.pressed_keys}")  # 디버깅용
        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_s):
                self.pressed_keys.discard(event.key)
                # print(f"Key Up: {event.key}, Pressed Keys: {self.pressed_keys}")  # 디버깅용
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y + 30, self.x + 25, self.y - 30

    def handle_collision(self, group, other):
        pass
