# mario.py

from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_s
import game_framework
import game_world
from config import MarioConfig
from state_machine import StateMachine, right_down, left_down, right_up, left_up, s_down

# 상수 정의
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # Meter per Minute
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)  # Meter per Second
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  # Pixel per Second
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
            if left_down(e) or right_down(e):
                if left_down(e):
                    mario.face_dir = -1
                elif right_down(e):
                    mario.face_dir = 1
        print("Idle 상태: 진입")  # 디버깅용

    @staticmethod
    def exit(mario, e):
        print("Idle 상태: 종료")  # 디버깅용
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
        # 현재 눌려 있는 키에 따라 방향 설정
        if SDLK_LEFT in mario.pressed_keys and SDLK_RIGHT not in mario.pressed_keys:
            mario.dir, mario.face_dir = -1, -1
        elif SDLK_RIGHT in mario.pressed_keys and SDLK_LEFT not in mario.pressed_keys:
            mario.dir, mario.face_dir = 1, 1
        else:
            mario.dir = 0
        mario.run_frame_x_positions = [290, 304, 321]
        print("Run 상태: 진입")  # 디버깅용

    @staticmethod
    def exit(mario, e):
        print("Run 상태: 종료")  # 디버깅용
        pass

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(mario.run_frame_x_positions)
        mario.x += mario.dir * RUN_SPEED_PPS * game_framework.frame_time
        mario.x = max(0, min(800, mario.x))  # 화면 경계 내로 클램프

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
                print("Jump 상태: 점프 시작")  # 디버깅용
            if left_down(e):
                mario.dir = -1
                mario.face_dir = -1
            elif right_down(e):
                mario.dir = 1
                mario.face_dir = 1
        mario.jump_frame_x_positions = [336, 353, 321]
        mario.frame = 0
        print("Jump 상태: enter 메소드 호출")  # 디버깅용

    @staticmethod
    def exit(mario, e):
        mario.jump_speed = 0
        mario.is_jumping = False
        print("Jump 상태: 점프 종료")  # 디버깅용

    @staticmethod
    def do(mario):
        # 점프 물리 적용
        mario.y += mario.jump_speed * game_framework.frame_time
        mario.jump_speed += Jump.GRAVITY * game_framework.frame_time
        print(f"Jump.do: y={mario.y}, jump_speed={mario.jump_speed}")  # 디버깅용

        # 현재 눌려 있는 키에 따라 방향 설정
        if SDLK_LEFT in mario.pressed_keys and SDLK_RIGHT not in mario.pressed_keys:
            mario.dir = -1
            mario.face_dir = -1
        elif SDLK_RIGHT in mario.pressed_keys and SDLK_LEFT not in mario.pressed_keys:
            mario.dir = 1
            mario.face_dir = 1
        else:
            mario.dir = 0

        # 좌우 이동
        if mario.dir != 0:
            mario.x += mario.dir * RUN_SPEED_PPS * game_framework.frame_time
            mario.x = max(0, min(800, mario.x))  # 화면 경계 내로 클램프

        # y축 제한을 제거하여 충돌 처리에 맡김

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
        self.is_jumping = False    # 점프 상태 플래그
        self.jump_speed = 0        # 점프 중 수직 속도

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_s):
                self.pressed_keys.add(event.key)
                print(f"Key Down: {event.key}")  # 디버깅용
        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_s):
                self.pressed_keys.discard(event.key)
                print(f"Key Up: {event.key}")  # 디버깅용
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
        elif group == 'mario:brick_top':
            print("마리오가 Brick 상단과 충돌했습니다. Brick 위에 착지합니다.")
            if self.jump_speed < 0:  # Mario가 아래로 이동 중일 때만 충돌 처리
                mario_bb = self.get_bb()
                brick_bb = other.get_top_bb()
                self.y = brick_bb[3] + (mario_bb[3] - mario_bb[1]) / 2  # Brick의 top 위치에 맞춤
                self.is_jumping = False
                self.jump_speed = 0
                # 현재 눌려 있는 키에 따라 상태 설정
                if SDLK_LEFT in self.pressed_keys and SDLK_RIGHT not in self.pressed_keys:
                    self.dir = -1
                    self.face_dir = -1
                    self.state_machine.set_state(Run)
                elif SDLK_RIGHT in self.pressed_keys and SDLK_LEFT not in self.pressed_keys:
                    self.dir = 1
                    self.face_dir = 1
                    self.state_machine.set_state(Run)
                else:
                    self.dir = 0
                    self.state_machine.set_state(Idle)
        elif group == 'mario:brick_bottom':
            print("마리오가 Brick 하단과 충돌했습니다.")
            if self.jump_speed > 0:  # Mario가 위로 이동 중일 때만 충돌 처리
                mario_bb = self.get_bb()
                brick_bb = other.get_bottom_bb()
                self.y = brick_bb[1] - (mario_bb[3] - mario_bb[1]) / 2  # Brick의 bottom 위치에 맞춤
                self.jump_speed = 0  # 점프 속도 초기화
        elif group == 'mario:brick_left':
            print("마리오가 Brick 왼쪽과 충돌했습니다.")
            # Mario가 오른쪽으로 이동 중일 때만 충돌 처리
            if self.dir > 0:
                mario_bb = self.get_bb()
                brick_bb = other.get_left_bb()
                self.x = brick_bb[0] - (mario_bb[2] - mario_bb[0]) / 2  # Brick의 left 위치에 맞춤
                self.dir = 0  # 이동 방향 초기화
        elif group == 'mario:brick_right':
            print("마리오가 Brick 오른쪽과 충돌했습니다.")
            # Mario가 왼쪽으로 이동 중일 때만 충돌 처리
            if self.dir < 0:
                mario_bb = self.get_bb()
                brick_bb = other.get_right_bb()
                self.x = brick_bb[2] + (mario_bb[2] - mario_bb[0]) / 2  # Brick의 right 위치에 맞춤
                self.dir = 0  # 이동 방향 초기화
        elif group == 'mario:grass':
            print("마리오가 Grass와 충돌했습니다. Grass 위에 착지합니다.")
            mario_bb = self.get_bb()
            grass_bb = other.get_bb()
            self.y = grass_bb[3] + (mario_bb[3] - mario_bb[1]) / 2  # Grass의 top 위치에 맞춤
            self.is_jumping = False
            self.jump_speed = 0
            # 현재 눌려 있는 키에 따라 상태 설정
            if SDLK_LEFT in self.pressed_keys and SDLK_RIGHT not in self.pressed_keys:
                self.dir = -1
                self.face_dir = -1
                self.state_machine.set_state(Run)
            elif SDLK_RIGHT in self.pressed_keys and SDLK_LEFT not in self.pressed_keys:
                self.dir = 1
                self.face_dir = 1
                self.state_machine.set_state(Run)
            else:
                self.dir = 0
                self.state_machine.set_state(Idle)
        else:
            pass  # 다른 충돌 그룹에 대한 처리 필요 시 추가

