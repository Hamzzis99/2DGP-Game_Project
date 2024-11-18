# brick.py

from pico2d import load_image, draw_rectangle
from game_object import GameObject
from utils.camera import Camera

class Brick(GameObject):
    image = None  # 클래스 변수로 이미지 로드 공유

    def __init__(self, x, y):
        if Brick.image is None:
            # 스프라이트 시트 'Items.png'에서 (0, 240) 위치의 (16x16) 크기 스프라이트를 불러옵니다.
            Brick.image = load_image('img/tiles.png')
        self.x = x
        self.y = y
        self.sprite_x = 0      # 스프라이트 시트 내 x 좌표
        self.sprite_y = 432    # 스프라이트 시트 내 y 좌표
        self.width = 16        # 스프라이트 너비
        self.height = 16       # 스프라이트 높이
        self.scale = 1.5       # 이미지 확대 배율 변경 (1.5로 조정)

    def update(self):
        pass  # Brick은 정적이므로 업데이트할 필요 없음

    def draw(self):
        Brick.image.clip_draw(
            self.sprite_x, self.sprite_y, self.width, self.height,
            self.x, self.y, self.width * self.scale, self.height * self.scale
        )
        # 충돌 박스 그리기 (디버깅용)
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_top_bb())
        draw_rectangle(*self.get_bottom_bb())
        draw_rectangle(*self.get_left_bb())
        draw_rectangle(*self.get_right_bb())

    def draw_with_camera(self, camera: Camera):
        screen_x, screen_y = camera.apply(self.x, self.y)
        Brick.image.clip_draw(
            self.sprite_x, self.sprite_y, self.width, self.height,
            screen_x, screen_y, self.width * self.scale, self.height * self.scale
        )
        # 충돌 박스 그리기 (디버깅용)
        draw_rectangle(*self.get_bb_offset(camera))
        draw_rectangle(*self.get_top_bb_offset(camera))
        draw_rectangle(*self.get_bottom_bb_offset(camera))
        draw_rectangle(*self.get_left_bb_offset(camera))
        draw_rectangle(*self.get_right_bb_offset(camera))

    def get_bb(self):
        # 전체 Brick의 충돌 박스
        return self.x - (self.width * self.scale) / 2, self.y - (self.height * self.scale) / 2, \
               self.x + (self.width * self.scale) / 2, self.y + (self.height * self.scale) / 2

    def get_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_top_bb(self):
        # Brick 상단의 충돌 박스 (좌우로 1픽셀씩 줄이고 y 범위도 축소)
        half_width = (self.width * self.scale) / 2 - 1
        return self.x - half_width, self.y + (self.height * self.scale) / 2 - 2, \
               self.x + half_width, self.y + (self.height * self.scale) / 2 + 2

    def get_top_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_top_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_bottom_bb(self):
        # Brick 하단의 충돌 박스 (좌우로 1픽셀씩 줄이고 y 범위도 축소)
        half_width = (self.width * self.scale) / 2 - 1
        return self.x - half_width, self.y - (self.height * self.scale) / 2 - 2, \
               self.x + half_width, self.y - (self.height * self.scale) / 2 + 2

    def get_bottom_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bottom_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_left_bb(self):
        # Brick 왼쪽의 충돌 박스 (위아래로 1픽셀씩 줄임)
        half_width = (self.width * self.scale) / 2
        half_height = (self.height * self.scale) / 2 - 1  # 상하로 1픽셀씩 줄임
        return self.x - half_width - 1, self.y - half_height, self.x - half_width, self.y + half_height

    def get_left_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_left_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_right_bb(self):
        # Brick 오른쪽의 충돌 박스 (위아래로 1픽셀씩 줄임)
        half_width = (self.width * self.scale) / 2
        half_height = (self.height * self.scale) / 2 - 1  # 상하로 1픽셀씩 줄임
        return self.x + half_width, self.y - half_height, self.x + half_width + 1, self.y + half_height

    def get_right_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_right_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y
