# grass.py

from pico2d import load_image, draw_rectangle
from game_object import GameObject
from utils.camera import Camera

class Grass(GameObject):
    def __init__(self):
        self.image = load_image('img/grass.png')
        self.x = 800  # 중앙 위치로 조정 (화면 너비의 절반)
        self.y = 30
        self.width = 1600  # 바닥의 너비
        self.height = 50   # 바닥의 높이
        self.scale = 1.0    # 스케일 조정 (필요에 따라 조정)

    def update(self):
        pass  # Grass는 정적이므로 업데이트할 필요 없음

    def draw(self):
        # 원래 draw 메서드는 화면 중앙에 그립니다.
        self.image.draw(self.x, self.y, self.width, self.height)
        # 충돌 박스 그리기 (디버깅용)
        #draw_rectangle(*self.get_bb())

    def draw_with_camera(self, camera: Camera):
        # Grass는 전체 바닥을 그려야 하므로, 월드 전체를 커버하도록 그립니다.
        # 카메라의 위치를 고려하여 바닥의 시작과 끝을 계산합니다.
        screen_x, screen_y = camera.apply(self.x, self.y)
        # 바닥 이미지를 화면에 맞게 그립니다.
        self.image.draw(screen_x, screen_y, self.width, self.height)
        # 충돌 박스 그리기 (디버깅용)
        #draw_rectangle(*self.get_bb_offset(camera))

    def get_bb(self):
        # 전체 Grass의 충돌 박스
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2

    def get_bb_offset(self, camera: Camera):
        # 카메라 오프셋을 적용한 충돌 박스
        left, bottom, right, top = self.get_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y
