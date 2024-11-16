# koomba.py

import random
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
        self.frame_x_positions = [296, 315]
        self.frame_y_position = 196
        self.frame_width = 16
        self.frame_height = 20

    def __init__(self):
        self.x, self.y = random.randint(400, 800), 70  # 초기 위치 설정
        self.load_images()
        self.frame = random.randint(0, 1)  # 초기 프레임 (0 또는 1)
        self.dir = random.choice([-1, 1])  # 이동 방향: -1(왼쪽), 1(오른쪽)
        self.alive = True  # 살아있는 상태
        self.stomped = False  # 굼바가 밟혔는지 여부
        self.stomp_timer = 0  # 밟힌 후 경과 시간
        self.frame_time = 0  # 애니메이션 시간

    def update(self):
        if self.stomped:
            self.stomp_timer -= game_framework.frame_time
            if self.stomp_timer <= 0:
                self.alive = False
                game_world.remove_object(self)  # 게임 월드에서 제거
            return  # 밟힌 상태에서는 이동하지 않음

        if not self.alive:
            return  # 살아있지 않으면 업데이트하지 않음

        # 애니메이션 프레임 업데이트
        self.frame_time += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        self.frame = int(self.frame_time) % len(self.frame_x_positions)

        # 위치 업데이트
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time

        # 화면 경계를 벗어나면 방향 전환
        if self.x > 800:
            self.dir = -1
        elif self.x < 400:
            self.dir = 1

        # 위치 클램프
        self.x = clamp(600, self.x, 800)

    def draw(self):
        if not self.alive:
            return  # 살아있지 않으면 그리지 않음

        if self.stomped:
            # 납작해진 굼바 이미지 그리기
            stomped_frame_x = 335  # 납작해진 굼바의 스프라이트 x 좌표
            stomped_frame_y = 196  # 납작해진 굼바의 스프라이트 y 좌표
            frame_width = 16
            frame_height = 16
            dest_width, dest_height = 32, 32  # 화면에 그릴 크기

            Koomba.image.clip_draw(
                stomped_frame_x, stomped_frame_y, frame_width, frame_height,
                self.x, self.y, dest_width, dest_height
            )
        else:
            # 현재 프레임 인덱스 (0 또는 1)
            frame_x = self.frame_x_positions[self.frame]
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

        # 디버깅용 충돌 박스 그리기 활성화
        draw_rectangle(*self.get_top_bb())
        draw_rectangle(*self.get_bottom_bb())

    def handle_event(self, event):
        pass  # 현재는 이벤트를 처리하지 않습니다.

    def get_top_bb(self):
        # Top 히트박스: 굼바의 머리 부분
        return self.x - 13, self.y + 10, self.x + 13, self.y + 25  # (left, bottom, right, top)

    def get_bottom_bb(self):
        # Bottom 히트박스: 굼바의 몸통 부분
        return self.x - 15, self.y - 15, self.x + 15, self.y + 20  # (left, bottom, right, top)

    def get_bb(self):
        # 전체 히트박스 (디폴트, 필요 시 사용)
        return self.x - 15, self.y - 25, self.x + 15, self.y + 25

    def handle_collision(self, group, other, hit_position):
        if not self.alive:
            return

        if group == 'mario:koomba_top':
            print("굼바가 마리오에게 밟혔습니다.")
            self.stomped = True
            self.stomp_timer = 1.0  # 1초 후에 제거
            # self.alive = False  # alive 상태는 유지하여 업데이트 및 그리기가 계속되도록 함
        elif group == 'mario:koomba_bottom':
            print("굼바가 마리오와 충돌했습니다.")
            # 추가적인 동작이 필요하다면 여기에 구현
        pass
