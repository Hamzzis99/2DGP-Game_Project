# mario.py

from pico2d import load_image, draw_rectangle, load_wav
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_s, SDLK_CAPSLOCK
import game_framework
import game_world
import play_mode
from ball import Ball
from items.coin import Coin
from items.star import Star
from utils.config import MarioConfig
from utils.dashboard import Dashboard
from state_machine import StateMachine, right_down, left_down, right_up, left_up, s_down, Dead, a_down
from game_object import GameObject
from utils.camera import Camera
from utils.score_text import ScoreText
from states import game_state  # game_state 임포트

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

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        pass  # 수평 이동 없음

    @staticmethod
    def draw(mario):
        if mario.gun_mode:
            frame_width = 20
            frame_height = 20
            frame_x = 26  # 수정된 x 좌표
            frame_y = 476  # 수정된 y 좌표
            image = mario.gun_image
        else:
            frame_width = 16
            frame_height = 16
            frame_x = 276
            frame_y = 342
            image = mario.image

        scaled_width = frame_width * mario.scale
        scaled_height = frame_height * mario.scale

        if mario.face_dir == -1:
            image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                mario.x, mario.y, scaled_width, scaled_height
            )
        else:
            image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, mario.x, mario.y,
                scaled_width, scaled_height
            )

    @staticmethod
    def draw_with_camera(mario, camera: Camera):
        if mario.gun_mode:
            frame_width = 20
            frame_height = 20
            frame_x = 26  # 수정된 x 좌표
            frame_y = 476  # 수정된 y 좌표
            image = mario.gun_image
        else:
            frame_width = 16
            frame_height = 16
            frame_x = 276
            frame_y = 342
            image = mario.image

        screen_x, screen_y = camera.apply(mario.x, mario.y)
        scaled_width = frame_width * mario.scale
        scaled_height = frame_height * mario.scale

        if mario.face_dir == -1:
            image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                screen_x, screen_y, scaled_width, scaled_height
            )
        else:
            image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, screen_x, screen_y,
                scaled_width, scaled_height
            )

    @staticmethod
    def handle_event(mario, e):
        if a_down(e) and mario.gun_mode:
            print("Idle 상태에서 a_down 이벤트 감지")
            mario.fire_ball()

class Run:
    @staticmethod
    def enter(mario, e):
        if right_down(e) or left_up(e):
            mario.dir, mario.face_dir, mario.action = 1, 1, 1
        elif left_down(e) or right_up(e):
            mario.dir, mario.face_dir, mario.action = -1, -1, 0
        else:
            mario.dir = 0

        if mario.gun_mode:
            mario.run_frame_x_positions = [100, 125, 146]
            mario.frame_y = 476
            mario.frame_width = 20
            mario.frame_height = 20
        else:
            mario.run_frame_x_positions = [290, 304, 321]
            mario.frame_y = 342
            mario.frame_width = 16
            mario.frame_height = 16
        mario.frame = 0

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(
            mario.run_frame_x_positions)
        mario.x += mario.dir * RUN_SPEED_PPS * game_framework.frame_time
        mario.x = max(0, min(MarioConfig.WORLD_WIDTH, mario.x))

    @staticmethod
    def draw(mario):
        frame_x = mario.run_frame_x_positions[int(mario.frame)]
        frame_y = mario.frame_y
        frame_width = mario.frame_width
        frame_height = mario.frame_height
        image = mario.gun_image if mario.gun_mode else mario.image

        scaled_width = frame_width * mario.scale
        scaled_height = frame_height * mario.scale

        if mario.face_dir == -1:
            image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                mario.x, mario.y, scaled_width, scaled_height
            )
        else:
            image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, mario.x, mario.y,
                scaled_width, scaled_height
            )

    @staticmethod
    def draw_with_camera(mario, camera: Camera):
        frame_x = mario.run_frame_x_positions[int(mario.frame)]
        frame_y = mario.frame_y
        frame_width = mario.frame_width
        frame_height = mario.frame_height
        image = mario.gun_image if mario.gun_mode else mario.image

        screen_x, screen_y = camera.apply(mario.x, mario.y)
        scaled_width = frame_width * mario.scale
        scaled_height = frame_height * mario.scale

        if mario.face_dir == -1:
            image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                screen_x, screen_y, scaled_width, scaled_height
            )
        else:
            image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, screen_x, screen_y,
                scaled_width, scaled_height
            )

    @staticmethod
    def handle_event(mario, e):
        if a_down(e) and mario.gun_mode:
            print("Run 상태에서 a_down 이벤트 감지")
            mario.fire_ball()

class Jump:
    JUMP_VELOCITY = 350  # 점프 초기 속도

    @staticmethod
    def enter(mario, e):
        if e is not None and isinstance(e, tuple):
            if s_down(e):
                mario.velocity_y = Jump.JUMP_VELOCITY
                mario.jump_sound.play()
            if left_down(e):
                mario.dir = -1
                mario.face_dir = -1
            elif right_down(e):
                mario.dir = 1
                mario.face_dir = 1

        if mario.gun_mode:
            mario.jump_frame_x_positions = [173]
            mario.frame_y = 476
            mario.frame_width = 20
            mario.frame_height = 20
        else:
            mario.jump_frame_x_positions = [336, 353, 321]
            mario.frame_y = 342
            mario.frame_width = 16
            mario.frame_height = 16
        mario.frame = 0

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        if SDLK_LEFT in mario.pressed_keys and SDLK_RIGHT not in mario.pressed_keys:
            mario.dir = -1
            mario.face_dir = -1
        elif SDLK_RIGHT in mario.pressed_keys and SDLK_LEFT not in mario.pressed_keys:
            mario.dir = 1
            mario.face_dir = 1
        else:
            mario.dir = 0

        mario.x += mario.dir * RUN_SPEED_PPS * game_framework.frame_time
        mario.x = max(0, min(MarioConfig.WORLD_WIDTH, mario.x))

        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(
            mario.jump_frame_x_positions)

    @staticmethod
    def draw(mario):
        frame_x = mario.jump_frame_x_positions[int(mario.frame) % len(mario.jump_frame_x_positions)]
        frame_y = mario.frame_y
        frame_width = mario.frame_width
        frame_height = mario.frame_height
        image = mario.gun_image if mario.gun_mode else mario.image

        scaled_width = frame_width * mario.scale
        scaled_height = frame_height * mario.scale

        if mario.face_dir == -1:
            image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                mario.x, mario.y, scaled_width, scaled_height
            )
        else:
            image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, mario.x, mario.y,
                scaled_width, scaled_height
            )

    @staticmethod
    def draw_with_camera(mario, camera: Camera):
        frame_x = mario.jump_frame_x_positions[int(mario.frame) % len(mario.jump_frame_x_positions)]
        frame_y = mario.frame_y
        frame_width = mario.frame_width
        frame_height = mario.frame_height
        image = mario.gun_image if mario.gun_mode else mario.image

        screen_x, screen_y = camera.apply(mario.x, mario.y)
        scaled_width = frame_width * mario.scale
        scaled_height = frame_height * mario.scale

        if mario.face_dir == -1:
            image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                screen_x, screen_y, scaled_width, scaled_height
            )
        else:
            image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, screen_x, screen_y,
                scaled_width, scaled_height
            )

    @staticmethod
    def handle_event(mario, e):
        if a_down(e) and mario.gun_mode:
            print("Jump 상태에서 a_down 이벤트 감지")
            mario.fire_ball()

# 마리오 클래스 정의
class Mario(GameObject):
    def __init__(self, dashboard):
        self.dashboard = dashboard  # Dashboard 인스턴스 참조 설정

        self.x, self.y = MarioConfig.START_X, MarioConfig.START_Y  # 초기 위치
        self.face_dir = 1  # 방향: 1(오른쪽), -1(왼쪽)
        self.dir = 0  # 이동 방향: -1(왼쪽), 0(정지), 1(오른쪽)
        self.image = load_image('img/character.png')
        self.gun_image = load_image('img/gun_mario.png')  # gun_mode용 이미지
        self.jump_sound = load_wav('sound/jump.ogg')
        self.jump_sound.set_volume(32)
        self.brick_sound = load_wav('sound/brick.ogg')
        self.brick_sound.set_volume(32)
        self.dead_sound = load_wav('sound/death.wav')
        self.dead_sound.set_volume(32)
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
            }
        })
        self.pressed_keys = set()  # 현재 눌려 있는 키
        self.frame = 0  # 애니메이션 프레임
        self.velocity_y = 0  # 수직 속도 추가
        self.dead = False  # Mario의 사망 상태 추가
        self.gun_mode = True  # gun_mode 상태 추가
        self.scale = 2  # 스케일 값 추가

    def update(self):
        frame_time = game_framework.frame_time
        self.state_machine.update()  # 상태 머신 업데이트는 항상 호출

        self.velocity_y += GRAVITY * frame_time
        self.y += self.velocity_y * frame_time

        if not self.dead:
            if self.y < 0:
                self.dead = True
                self.state_machine.set_state(Dead())
                print("마리오의 y축값이 0이하여서 사망하였습니다.")
        else:
            pass  # 죽은 상태에서는 추가 로직 없음

    def handle_event(self, event):
        if self.dead:
            return
        if event.type == SDL_KEYDOWN:
            # print(f"Key Down: {event.key}")
            if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_s):
                self.pressed_keys.add(event.key)
            elif event.key == SDLK_CAPSLOCK:
                print(f"마리오의 위치: x={self.x}, y={self.y}")
        elif event.type == SDL_KEYUP:
            # print(f"Key Up: {event.key}")
            if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_s):
                self.pressed_keys.discard(event.key)
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        if self.dead:
            self.state_machine.draw()
        else:
            self.state_machine.draw()
            draw_rectangle(*self.get_bb())

    def draw_with_camera(self, camera: Camera):
        self.state_machine.draw_with_camera(camera)
        draw_rectangle(*self.get_bb_offset(camera))

    def get_bb(self):
        if self.gun_mode:
            width = 20 * self.scale
            height = 20 * self.scale
        else:
            width = 16 * self.scale
            height = 16 * self.scale
        half_width = width / 2
        half_height = height / 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def handle_collision(self, group, other, hit_position):
        if self.dead:
            return

        if group == 'mario:koomba_top':
            if not other.stomped:
                other.stomped = True
                game_state.score += 100
                print(f"Score increased by 100. Total Score: {game_state.score}")

                score_text = ScoreText(self.x, self.y + 30, "+100")
                game_world.add_object(score_text, 2)
                print("ScoreText 추가됨: +100")

                self.velocity_y = Jump.JUMP_VELOCITY
                self.state_machine.set_state(Jump)

        elif group == 'mario:koomba_bottom':
            print(f"Mario가 Koomba에게 당했습니다. 남은 목숨: {game_state.lives}")
            self.dead = True
            self.state_machine.set_state(Dead())

        elif group == 'mario:turtle':
            print(f"Mario가 Turtle과 충돌했습니다. 남은 목숨: {game_state.lives}")
            self.dead = True
            self.state_machine.set_state(Dead())
        elif group == 'mario:boss_turtle':
            print(f"Mario가 Turtle과 충돌했습니다. 남은 목숨: {game_state.lives}")
            self.dead = True
            self.state_machine.set_state(Dead())

        elif group in ['mario:grass', 'mario:brick_top', 'mario:random_box_top', 'mario:gun_box_top']:
            if self.velocity_y <= 0:
                mario_bb = self.get_bb()
                obj_bb = other.get_bb()
                self.y = obj_bb[3] + (mario_bb[3] - mario_bb[1]) / 2
                self.velocity_y = 0
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
            if self.velocity_y > 0:
                if group == 'mario:random_box_bottom' and not other.changed:
                    print("Random Box가 마리오에게 밑에서 맞았습니다. 스프라이트를 변경하고 코인을 생성합니다.")
                    other.changed = True

                    coin = Coin(other.x, other.y + (other.height * other.scale))
                    game_world.add_object(coin, 1)
                    game_state.score += 1000
                    print("마리오에게 1000점이 추가되었습니다!")

                    score_text = ScoreText(self.x, self.y + 50, "+1000")
                    game_world.add_object(score_text, 2)
                    print("ScoreText 추가됨: +1000")

                elif group == 'mario:gun_box_bottom' and not other.changed:
                    print("Gun Box가 마리오에게 밑에서 맞았습니다. 스프라이트를 변경하고 스타를 생성합니다.")
                    other.changed = True

                    star = Star(
                        other.x,
                        other.y + (other.height * other.scale)
                    )
                    play_mode.objects_to_add.append(star)
                else:
                    self.brick_sound.play()
                    mario_bb = self.get_bb()
                    obj_bb = other.get_bb()
                    self.y = obj_bb[1] - (mario_bb[3] - mario_bb[1]) / 2
                    self.velocity_y = 0

        elif group in ['mario:brick_left', 'mario:random_box_left', 'mario:gun_box_left']:
            if self.dir > 0:
                mario_bb = self.get_bb()
                obj_bb = other.get_bb()
                self.x = obj_bb[0] - (mario_bb[2] - mario_bb[0]) / 2
                self.dir = 0

        elif group in ['mario:brick_right', 'mario:random_box_right', 'mario:gun_box_right']:
            if self.dir < 0:
                mario_bb = self.get_bb()
                obj_bb = other.get_bb()
                self.x = obj_bb[2] + (mario_bb[2] - mario_bb[0]) / 2
                self.dir = 0

        elif group == 'mario:coin':
            game_state.score += 1000
            game_world.remove_object(other)
            print("코인을 수집했습니다!")

            score_text = ScoreText(self.x, self.y + 50, "+1000")
            game_world.add_object(score_text, 2)
            print("ScoreText 추가됨: +1000")

        elif group == 'mario:star':
            Star.collect_sound.play()
            game_world.remove_object(other)
            print("스타를 수집했습니다!")
            self.gun_mode = True

        else:
            pass

    def fire_ball(self):
        print("fire_ball 메서드가 호출되었습니다.")
        if self.face_dir == 1:
            ball_x = self.x + self.get_width() / 2
            velocity_x = 500
        else:
            ball_x = self.x - self.get_width() / 2
            velocity_x = -500
        ball_y = self.y

        ball = Ball(ball_x, ball_y, velocity_x)
        play_mode.objects_to_add.append(ball)  # Ball을 objects_to_add에 추가
        print("Ball 객체가 objects_to_add 리스트에 추가되었습니다.")

    def get_width(self):
        if self.gun_mode:
            return 20 * self.scale
        else:
            return 16 * self.scale

def reset_mario(mario):
    mario.x = MarioConfig.START_X
    mario.y = MarioConfig.START_Y
    mario.face_dir = 1
    mario.dir = 0
    mario.velocity_y = 0
    mario.state_machine.set_state(Idle)  # 기본 상태로 변경
    mario.pressed_keys.clear()  # 눌려 있는 키 초기화
    mario.frame = 0
    mario.gun_mode = False  # gun_mode 비활성화
