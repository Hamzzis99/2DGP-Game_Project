# props/flag.py

from pico2d import load_image

class Flag:
    def __init__(self, x=0, y=0, scale=0.0):
        self.image = load_image('img/flag.png')  # 이미지 경로 확인
        self.x = x
        self.y = y
        self.original_width = 500  # 원본 이미지 너비
        self.original_height = 500  # 원본 이미지 높이
        self.scale = scale  # 스케일 팩터

    def update(self):
        # Flag는 정적인 객체이므로 업데이트 로직이 필요 없다면 pass
        pass

    def draw_with_camera(self, camera):
        # 카메라 위치를 고려하여 그리기
        screen_x, screen_y = camera.apply(self.x, self.y)
        scaled_width = self.original_width * self.scale
        scaled_height = self.original_height * self.scale
        self.image.draw(screen_x, screen_y, scaled_width, scaled_height)
