# ball.py

from pico2d import *
import game_world
import game_framework
from utils.camera import Camera  # 카메라 임포트
from utils.config import MarioConfig

class Ball:
    image = None

    def __init__(self, x, y, velocity_x, velocity_y=0):
        print(f"Ball 객체 생성: 위치=({x}, {y}), 속도=({velocity_x}, {velocity_y})")
        if Ball.image is None:
            try:
                Ball.image = load_image('ball21x21.png')  # 이미지 경로와 파일명 확인
                print("Ball 이미지 로드 성공")
            except Exception as e:
                print(f"Ball 이미지 로드 실패: {e}")
        self.x, self.y = x, y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.width = 16
        self.height = 16

    def draw(self):
        pass  # draw 메서드에서는 아무것도 하지 않음

    def draw_with_camera(self, camera):
        if self.image:
            screen_x, screen_y = camera.apply(self.x, self.y)
            self.image.draw(screen_x, screen_y)
        else:
            print("Ball 이미지가 로드되지 않아 그릴 수 없습니다.")

    def get_bb_offset(self, camera):
        left, bottom, right, top = self.get_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def update(self):
        print(f"Ball 업데이트: 위치=({self.x}, {self.y})")
        self.x += self.velocity_x * game_framework.frame_time
        self.y += self.velocity_y * game_framework.frame_time

        if self.x < 0 or self.x > MarioConfig.WORLD_WIDTH or self.y < 0 or self.y > MarioConfig.WORLD_HEIGHT:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, \
               self.x + self.width / 2, self.y + self.height / 2

    def handle_collision(self, group, other):
        pass  # 충돌 처리는 현재 생략

