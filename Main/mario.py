# mario.py

from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_s
import game_framework
import game_world
from config import MarioConfig
from state_machine import StateMachine, right_down, left_down, right_up, left_up, s_down

# 상수 정의
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

# 상태 클래스 정의
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
    JUMP_VELOCITY = 350  # 점프 속도
    GRAVITY = -700       # 중력 가속도

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
                frame_x, frame_y, frame_width, frame_height, mario.x, mario.y,
                frame_width * 3, frame_height * 3
            )

    @staticmethod
    def handle_event(mario, e):
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

# 마리오 클래스 정의
class Mario:
    def __init__(self):
        self.x, self.y = MarioConfig.START_X, MarioConfig.START_Y  # 초기 위치
        self.face_dir = 1         # 방향: 1(오른쪽), -1(왼쪽)
        self.dir = 0              # 이동 방향: -1(왼쪽), 0(정지), 1(오른쪽)
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, s_down: Jump},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, s_down: Jump},
            Jump: {
                right_down: Jump,
                left_down: Jump,
                right_up: Jump,
                left_up: Jump,
                s_down: Jump  # 이중 점프 방지
            }
        })
        self.pressed_keys = set()  # 현재 눌려 있는 키
        self.frame = 0             # 애니메이션 프레임
        self.game_framework = game_framework  # frame_time 접근을 위해 할당
        self.is_jumping = False    # 점프 상태 플래그
        self.jump_speed = 0        # 점프 중 수직 속도

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_s):
                self.pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_s):
                self.pressed_keys.discard(event.key)
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        # 충돌 박스 그리기 (디버깅용)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y - 30, self.x + 25, self.y + 30

    def handle_collision(self, group, other, hit_position):
        if group == 'mario:koomba_top':
            print("마리오가 굼바를 밟았습니다. 굼바를 제거하고 점프합니다.")
            game_world.remove_object(other)  # 굼바 제거
            self.jump_speed = Jump.JUMP_VELOCITY  # 점프 속도 설정
            self.is_jumping = True
            self.state_machine.set_state(Jump)  # 점프 상태로 변경
        elif group == 'mario:koomba_bottom':
            print("마리오가 굼바와 충돌했습니다. 게임을 종료합니다.")
            game_framework.quit()
