# mario.py

from pico2d import load_image, draw_rectangle, load_wav
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_s
import game_framework
import game_world
from config import MarioConfig
from state_machine import StateMachine, right_down, left_down, right_up, left_up, s_down
from game_object import GameObject
from utils.camera import Camera
import game_over

# 상수 정의
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # Meter per Minute
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)  # Meter per Second
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  # Pixel per Second
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

GRAVITY = -700  # 중력 가속도 (픽셀/초^2)

# 상태 클래스 정의 (Idle, Run, Jump 등)
class Idle:
    @staticmethod
    def enter(mario, e):
        mario.dir = 0
        mario.frame = 0
        if e is not None and isinstance(e, tuple):
            if left_down(e):
                mario.face_dir = -1
            elif right_down(e):
                mario.face_dir = 1
        #print("Idle 상태: 진입")  # 디버깅용

    @staticmethod
    def exit(mario, e):
        #print("Idle 상태: 종료")  # 디버깅용
        pass

    @staticmethod
    def do(mario):
        pass  # 수평 이동 없음

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

    @staticmethod
    def draw_with_camera(mario, camera: Camera):
        frame_width = 16
        frame_height = 16
        frame_x = 276
        frame_y = 342
        screen_x, screen_y = camera.apply(mario.x, mario.y)
        if mario.face_dir == -1:
            mario.image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                screen_x, screen_y, frame_width * 3, frame_height * 3
            )
        else:
            mario.image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, screen_x, screen_y,
                frame_width * 3, frame_height * 3
            )

class Run:
    @staticmethod
    def enter(mario, e):
        # 헬퍼 함수를 사용하여 이벤트에 따라 방향 설정
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            mario.dir, mario.face_dir, mario.action = 1, 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            mario.dir, mario.face_dir, mario.action = -1, -1, 0
        else:
            mario.dir = 0  # 이동하지 않음

        # 애니메이션 프레임 초기화
        mario.run_frame_x_positions = [290, 304, 321]
        mario.frame = 0
        #print("Run 상태: 진입")  # 디버깅용

    @staticmethod
    def exit(mario, e):
        #print("Run 상태: 종료")  # 디버깅용
        pass

    @staticmethod
    def do(mario):
        # 애니메이션 프레임 업데이트
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(
            mario.run_frame_x_positions)
        # 마리오 이동
        mario.x += mario.dir * RUN_SPEED_PPS * game_framework.frame_time
        # 월드 경계 내로 위치 클램프
        mario.x = max(0, min(MarioConfig.WORLD_WIDTH, mario.x))

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

    @staticmethod
    def draw_with_camera(mario, camera: Camera):
        frame_width = 16
        frame_height = 16
        frame_y = 342
        frame_x = mario.run_frame_x_positions[int(mario.frame)]
        screen_x, screen_y = camera.apply(mario.x, mario.y)
        if mario.face_dir == -1:
            mario.image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                screen_x, screen_y, frame_width * 3, frame_height * 3
            )
        else:
            mario.image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, screen_x, screen_y,
                frame_width * 3, frame_height * 3
            )


class Jump:
    JUMP_VELOCITY = 350  # 점프 초기 속도

    @staticmethod
    def enter(mario, e):
        if e is not None and isinstance(e, tuple):
            if s_down(e):
                mario.velocity_y = Jump.JUMP_VELOCITY
                mario.jump_sound.play()  # 점프 사운드 재생
                #print("Jump 상태: 점프 시작")  # 디버깅용
            # 방향 키 처리
            if left_down(e):
                mario.dir = -1
                mario.face_dir = -1
            elif right_down(e):
                mario.dir = 1
                mario.face_dir = 1
        mario.jump_frame_x_positions = [336, 353, 321]
        mario.frame = 0
        #print("Jump 상태: enter 메소드 호출")  # 디버깅용

    @staticmethod
    def exit(mario, e):
        #print("Jump 상태: 점프 종료")  # 디버깅용
        pass

    @staticmethod
    def do(mario):
        # 수평 이동 처리
        if SDLK_LEFT in mario.pressed_keys and SDLK_RIGHT not in mario.pressed_keys:
            mario.dir = -1
            mario.face_dir = -1
        elif SDLK_RIGHT in mario.pressed_keys and SDLK_LEFT not in mario.pressed_keys:
            mario.dir = 1
            mario.face_dir = 1
        else:
            mario.dir = 0

        mario.x += mario.dir * RUN_SPEED_PPS * game_framework.frame_time
        mario.x = max(0, min(MarioConfig.WORLD_WIDTH, mario.x))  # 월드 경계 내로 클램프

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
    def draw_with_camera(mario, camera: Camera):
        frame_width = 16
        frame_height = 16
        frame_y = 342
        frame_x = mario.jump_frame_x_positions[int(mario.frame)]
        screen_x, screen_y = camera.apply(mario.x, mario.y)
        if mario.face_dir == -1:
            mario.image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                screen_x, screen_y, frame_width * 3, frame_height * 3
            )
        else:
            mario.image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, screen_x, screen_y,
                frame_width * 3, frame_height * 3
            )

# 마리오 클래스 정의
class Mario(GameObject):
    def __init__(self, dashboard):
        self.dashboard = dashboard  # Dashboard 인스턴스 참조 설정

        self.x, self.y = MarioConfig.START_X, MarioConfig.START_Y  # 초기 위치
        self.face_dir = 1  # 방향: 1(오른쪽), -1(왼쪽)
        self.dir = 0  # 이동 방향: -1(왼쪽), 0(정지), 1(오른쪽)
        self.image = load_image('img/character.png')
        self.jump_sound = load_wav('sound/jump.ogg')
        self.jump_sound.set_volume(32)  # 필요에 따라 볼륨 조절
        self.brick_sound = load_wav('sound/brick.ogg')
        self.brick_sound.set_volume(32)  # 필요에 따라 볼륨 조절
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
                # s_down 이벤트는 점프 상태에서 추가 점프를 방지하기 위해 생략
            }
        })
        self.pressed_keys = set()  # 현재 눌려 있는 키
        self.frame = 0  # 애니메이션 프레임
        self.velocity_y = 0  # 수직 속도 추가
        self.dead = False  # Mario의 사망 상태 추가



    def update(self):
        frame_time = game_framework.frame_time
        self.state_machine.update()

        # 중력 적용
        self.velocity_y += GRAVITY * game_framework.frame_time
        self.y += self.velocity_y * game_framework.frame_time

        # 바닥 이하로 내려가지 않도록 위치 제한
        if self.y < 0:
            self.y = 0
            self.velocity_y = 0

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_s):
                self.pressed_keys.add(event.key)
                #print(f"Key Down: {event.key}")  # 디버깅용
        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_s):
                self.pressed_keys.discard(event.key)
                #print(f"Key Up: {event.key}")  # 디버깅용
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        # 충돌 박스 그리기 (디버깅용)
        draw_rectangle(*self.get_bb())

    def draw_with_camera(self, camera: Camera):
        self.state_machine.draw_with_camera(camera)
        # 충돌 박스 그리기 (디버깅용)
        draw_rectangle(*self.get_bb_offset(camera))

    def get_bb(self):
        width = 16 * 3  # 이미지의 폭 * 스케일
        height = 16 * 3  # 이미지의 높이 * 스케일
        half_width = width / 2
        half_height = height / 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def handle_collision(self, group, other, hit_position):
        if group == 'mario:koomba_top':
            if not other.stomped:
                other.stomped = True  # Koomba를 밟혔음으로 표시
                self.dashboard.increment_score(100)  # 점수 100점 추가
                self.velocity_y = Jump.JUMP_VELOCITY  # Mario 점프 속도 설정
                self.state_machine.set_state(Jump)  # Mario 상태를 Jump로 변경
                print(f"Score increased by 100. Total Score: {self.dashboard.points}")  #

        elif group == 'mario:koomba_bottom':
            #print("마리오가 굼바와 충돌했습니다. 게임을 종료합니다.")
            #game_framework.quit()
            #game_framework.change_mode(game_over)
            self.dead = True
        elif group == 'mario:turtle':
            #print("마리오가 보스와 충돌했습니다. 게임을 종료합니다.")
            #game_framework.quit()  # 게임 종료
            #game_framework.change_mode(game_over)  # 게임 오버 화면으로 전환
            self.dead = True

        elif group in ['mario:grass', 'mario:brick_top', 'mario:random_box_top', 'mario:gun_box_top']:
            #print(f"마리오가 {group} 상단과 충돌했습니다. 착지합니다.")
            if self.velocity_y <= 0:  # 마리오가 아래로 이동 중일 때만 충돌 처리
                mario_bb = self.get_bb()
                obj_bb = other.get_bb()
                self.y = obj_bb[3] + (mario_bb[3] - mario_bb[1]) / 2  # 오브젝트의 top 위치에 맞춤
                self.velocity_y = 0  # 수직 속도 0으로 설정
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

        elif group in ['mario:brick_bottom', 'mario:random_box_bottom', 'mario:gun_box_bottom']:
            #print(f"마리오가 {group} 하단과 충돌했습니다.")
            if self.velocity_y > 0:  # 마리오가 위로 이동 중일 때만 충돌 처리
                self.brick_sound.play()  # 점프 사운드 재생
                mario_bb = self.get_bb()
                obj_bb = other.get_bb()
                self.y = obj_bb[1] - (mario_bb[3] - mario_bb[1]) / 2  # 오브젝트의 bottom 위치에 맞춤
                self.velocity_y = 0  # 수직 속도 초기화

        elif group in ['mario:brick_left', 'mario:random_box_left', 'mario:gun_box_left']:
            #print(f"마리오가 {group} 왼쪽과 충돌했습니다.")
            if self.dir > 0:  # 마리오가 오른쪽으로 이동 중일 때만 충돌 처리
                mario_bb = self.get_bb()
                obj_bb = other.get_bb()
                self.x = obj_bb[0] - (mario_bb[2] - mario_bb[0]) / 2  # 오브젝트의 left 위치에 맞춤
                self.dir = 0  # 이동 방향 초기화

        elif group in ['mario:brick_right', 'mario:random_box_right', 'mario:gun_box_right']:
            #print(f"마리오가 {group} 오른쪽과 충돌했습니다.")
            if self.dir < 0:  # 마리오가 왼쪽으로 이동 중일 때만 충돌 처리
                mario_bb = self.get_bb()
                obj_bb = other.get_bb()
                self.x = obj_bb[2] + (mario_bb[2] - mario_bb[0]) / 2  # 오브젝트의 right 위치에 맞춤
                self.dir = 0  # 이동 방향 초기화
        elif group == 'mario:coin':
            self.points += 100  # 또는 원하는 점수
            game_world.remove_object(other)  # 코인 제거
            print("코인을 수집했습니다!")

        else:
            pass  # 다른 충돌 그룹에 대한 처리 필요 시 추가

def reset_mario(mario):
    mario.x = MarioConfig.START_X
    mario.y = MarioConfig.START_Y
    mario.face_dir = 1
    mario.dir = 0
    mario.velocity_y = 0
    mario.state_machine.set_state(Idle)  # 기본 상태로 변경
    mario.pressed_keys.clear()  # 눌려 있는 키 초기화
    mario.frame = 0
def reset_game():
    global mario
    game_world.remove_object(mario)  # 기존 마리오 객체 제거
    mario = Mario()  # 새로운 마리오 객체 생성
    game_world.add_object(mario, 1)
def init():
    global mario, running
    # 마리오 객체 초기화 코드 추가
    reset_mario(mario)  # 또는 reset_game() 호출
    running = True

