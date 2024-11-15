# koomba.py

import random
import math
import game_framework
import game_world

from pico2d import *

# Koomba Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Koomba Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2.0  # 두 가지 프레임으로 애니메이션


class Koomba:
    image = None  # 스프라이트 시트 이미지

    def load_images(self):
        if Koomba.image is None:
            Koomba.image = load_image('character.png')  # 스프라이트 시트 로드

        # 애니메이션 프레임 좌표 설정
        # 두 가지 행동을 위한 두 개의 프레임 좌표
        self.frame_x_positions = [296, 315]
        self.frame_y_position = 196
        self.frame_width = 16
        self.frame_height = 20

    def __init__(self):
        self.x, self.y = random.randint(400, 800), 70  # 초기 위치 설정
        self.load_images()
        self.frame = random.randint(0, 1)  # 초기 프레임 (0 또는 1)
        self.dir = random.choice([-1, 1])  # 이동 방향: -1(왼쪽), 1(오른쪽)

    def update(self):
        # 애니메이션 프레임 업데이트
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(self.frame_x_positions)

        # 위치 업데이트
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time

        # 화면 경계를 벗어나면 방향 전환
        if self.x > 800:
            self.dir = -1
        elif self.x < 400:
            self.dir = 1

        # 위치 클램프
        self.x = clamp(400, self.x, 800)

    def draw(self):
        # 현재 프레임 인덱스 (0 또는 1)
        current_frame = int(self.frame) % len(self.frame_x_positions)
        frame_x = self.frame_x_positions[current_frame]
        frame_y = self.frame_y_position

        # 그릴 크기 설정
        dest_width, dest_height = 32, 32  # 화면에 그릴 크기

        if self.dir < 0:
            # 왼쪽으로 이동 중이면 프레임을 수평 반전하여 그립니다.
            Koomba.image.clip_composite_draw(
                frame_x, frame_y, self.frame_width, self.frame_height, 0, 'h',
                self.x, self.y, dest_width, dest_height
            )
        else:
            # 오른쪽으로 이동 중이면 프레임을 그대로 그립니다.
            Koomba.image.clip_draw(
                frame_x, frame_y, self.frame_width, self.frame_height,
                self.x, self.y, dest_width, dest_height
            )

        # 디버깅용 충돌 박스 그리기 (필요 시 주석 해제)
        # draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass  # 현재는 이벤트를 처리하지 않습니다.

    def get_bb(self):
        # 충돌 박스는 현재 사용되지 않으므로 기본 충돌 박스를 반환합니다.
        return self.x - 100, self.y - 100, self.x + 80, self.y + 100  # 기본 충돌 박스
