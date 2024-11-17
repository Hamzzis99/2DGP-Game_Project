# grass.py
from pico2d import load_image

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def update(self):
        pass  # Grass는 정적이므로 업데이트할 필요 없음

    def draw(self):
        self.image.draw(400, 30)

    def get_bb(self):
        # Grass의 충돌 박스 설정 (이미지 크기에 따라 조정 필요)
        # 여기서는 가로로 1600 픽셀, 세로로 50 픽셀로 설정
        return 0, 0, 1600-1, 50
