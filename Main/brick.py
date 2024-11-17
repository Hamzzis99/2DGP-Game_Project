# brick.py

from pico2d import load_image

class Brick:
    image = None  # 클래스 변수로 이미지 로드 공유

    def __init__(self, x, y):
        if Brick.image is None:
            # 스프라이트 시트 'Items.png'에서 (0, 240) 위치의 (16x16) 크기 스프라이트를 불러옵니다.
            Brick.image = load_image('Items.png')
        self.x = x
        self.y = y
        self.sprite_x = 0      # 스프라이트 시트 내 x 좌표
        self.sprite_y = 240    # 스프라이트 시트 내 y 좌표
        self.width = 16        # 스프라이트 너비
        self.height = 16       # 스프라이트 높이

    def update(self):
        pass  # Brick은 정적이므로 업데이트할 필요 없음

    def draw(self):
        # 스프라이트 시트에서 (sprite_x, sprite_y) 위치의 (width, height) 크기 영역을 잘라서 그립니다.
        # 화면에 그릴 크기는 필요에 따라 조정 (예: 3배 확장)
        Brick.image.clip_draw(self.sprite_x, self.sprite_y, self.width, self.height, self.x, self.y, self.width * 3, self.height * 3)

    def get_bb(self):
        # 전체 Brick의 충돌 박스 (16x16 크기 확장)
        half_width = (self.width * 3) / 2
        half_height = (self.height * 3) / 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_top_bb(self):
        # Brick 상단의 충돌 박스 (상단 약간 확장)
        half_width = (self.width * 3) / 2
        return self.x - half_width, self.y + (self.height * 3) / 2, self.x + half_width, self.y + (self.height * 3) / 2 + 4

    def get_bottom_bb(self):
        # Brick 하단의 충돌 박스 (하단 약간 확장)
        half_width = (self.width * 3) / 2
        return self.x - half_width, self.y - (self.height * 3) / 2 - 4, self.x + half_width, self.y - (self.height * 3) / 2

    def get_left_bb(self):
        # Brick 왼쪽의 충돌 박스 (왼쪽 약간 확장)
        half_height = (self.height * 3) / 2
        return self.x - (self.width * 3) / 2 - 4, self.y - half_height, self.x - (self.width * 3) / 2, self.y + half_height

    def get_right_bb(self):
        # Brick 오른쪽의 충돌 박스 (오른쪽 약간 확장)
        half_height = (self.height * 3) / 2
        return self.x + (self.width * 3) / 2, self.y - half_height, self.x + (self.width * 3) / 2 + 4, self.y + half_height
