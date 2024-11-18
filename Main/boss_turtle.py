# boss_turtle.py

from pico2d import load_image, clamp
from game_object import GameObject
from utils.camera import Camera
import random
import game_framework
import game_world
from config import TurtleConfig  # TurtleConfig 임포트

# Turtle Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Turtle Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2.0  # 두 가지 프레임으로 애니메이션


class Turtle(GameObject):
    image = None  # 스프라이트 시트 이미지

    def load_images(self):
        if Turtle.image is None:
            Turtle.image = load_image('character.png')  # 스프라이트 시트 로드

        # 애니메이션 프레임 좌표 설정
        self.normal_frame_x_positions = [293, 312]
        self.normal_frame_y_position = 169
        self.transform1_frame_x_positions = [160, 141]
        self.transform1_frame_y_position = 169
        self.transform2_frame_x_positions = [141, 160]
        self.transform2_frame_y_position = 169
        self.frame_width = 20
        self.frame_height = 29

    def __init__(self):
        self.x, self.y = random.randint(400, 600), 70  # 초기 위치 설정
        self.load_images()
        self.frame = random.randint(0, 1)  # 초기 프레임 (0 또는 1)
        self.dir = random.choice([-1, 1])  # 이동 방향: -1(왼쪽), 1(오른쪽)
        self.alive = True  # 살아있는 상태
        self.state = 'normal'  # 현재 상태: 'normal', 'transform1', 'transform2'
        self.timer = TurtleConfig.TURTLE_TRANSFORM_INTERVAL  # 상태 전환 타이머
        self.frame_time = 0.0  # 애니메이션 시간
        self.frame_x_positions = self.normal_frame_x_positions
        self.frame_y_position = self.normal_frame_y_position

    def update(self):
        frame_time = game_framework.frame_time  # 전역 frame_time 사용

        if self.state == 'normal':
            self.timer -= frame_time
            print(f"Turtle normal. Timer: {self.timer:.2f}s")
            if self.timer <= 0:
                self.state = 'transform1'
                self.frame_x_positions = self.transform1_frame_x_positions
                self.frame_y_position = self.transform1_frame_y_position
                self.dir = 0  # 제자리 멈춤
                self.timer = TurtleConfig.TURTLE_TRANSFORM_DURATION  # 5초 동안 변신
                print("Turtle entered transform1 state.")

        elif self.state == 'transform1':
            self.timer -= frame_time
            print(f"Turtle transform1. Timer: {self.timer:.2f}s")
            if self.timer <= 0:
                self.state = 'transform2'
                self.frame_x_positions = self.transform2_frame_x_positions
                self.frame_y_position = self.transform2_frame_y_position
                self.timer = 0.0  # transform2는 즉시 다음 상태로 전환
                print("Turtle entered transform2 state.")

        elif self.state == 'transform2':
            # transform2 상태에서는 바로 normal 상태로 돌아감
            self.state = 'normal'
            self.frame_x_positions = self.normal_frame_x_positions
            self.frame_y_position = self.normal_frame_y_position
            self.dir = random.choice([-1, 1])  # 이동 방향 재설정
            self.timer = TurtleConfig.TURTLE_TRANSFORM_INTERVAL  # 다음 변신을 위한 타이머 리셋
            print("Turtle reverted to normal state.")

        # 상태가 'transform1' 또는 'transform2'일 때는 이동 및 애니메이션을 하지 않음
        if self.state in ['transform1', 'transform2']:
            return

        if not self.alive:
            return

        # 애니메이션 프레임 업데이트
        self.frame_time += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.frame_time) % len(self.frame_x_positions)

        # 위치 업데이트
        self.x += RUN_SPEED_PPS * self.dir * frame_time

        # 화면 경계를 벗어나면 방향 전환
        if self.x > 1400:
            self.dir = -1
        elif self.x < 200:
            self.dir = 1

        # 위치 클램프
        self.x = clamp(200, self.x, 1400)  # 이동 범위를 200~1400으로 설정

    def draw_with_camera(self, camera: Camera):
        if not self.alive:
            return  # 살아있지 않으면 그리지 않음

        screen_x, screen_y = camera.apply(self.x, self.y)

        # 현재 프레임 인덱스 (0 또는 1)
        frame_x = self.frame_x_positions[self.frame]
        frame_y = self.frame_y_position

        # 그릴 크기 설정
        dest_width, dest_height = 32, 32  # 화면에 그릴 크기

        if self.dir < 0:
            # 왼쪽으로 이동 중이면 프레임을 수평 반전하여 그립니다.
            Turtle.image.clip_composite_draw(
                frame_x, frame_y, self.frame_width, self.frame_height, 0, 'h',
                screen_x, screen_y, dest_width, dest_height
            )
        else:
            # 오른쪽으로 이동 중이면 프레임을 그대로 그립니다.
            Turtle.image.clip_draw(
                frame_x, frame_y, self.frame_width, self.frame_height,
                screen_x, screen_y, dest_width, dest_height
            )

        # 디버깅용 충돌 박스 그리기 활성화 (릴리즈 시 주석 처리)
        # draw_rectangle(*self.get_top_bb_offset(camera))
        # draw_rectangle(*self.get_bottom_bb_offset(camera))

    def get_bb(self):
        width = 16 * 2  # 이미지의 폭 * 스케일 (16 * 2 = 32)
        height = 20 * 1.6  # 이미지의 높이 * 스케일 (20 * 1.6 = 32)
        half_width = width / 2
        half_height = height / 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_top_bb(self):
        # Top 히트박스: Turtle의 머리 부분
        return self.x - 13, self.y + 10, self.x + 13, self.y + 25  # (left, bottom, right, top)

    def get_top_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_top_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_bottom_bb(self):
        # Bottom 히트박스: Turtle의 몸통 부분
        return self.x - 15, self.y - 15, self.x + 15, self.y + 20  # (left, bottom, right, top)

    def get_bottom_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bottom_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def handle_collision(self, group, other, hit_position):
        # Turtle의 handle_collision 메서드를 pass로 유지
        pass
