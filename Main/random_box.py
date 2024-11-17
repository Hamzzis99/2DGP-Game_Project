# random_box.py

from pico2d import load_image, draw_rectangle
import game_world

class Random_box:
    image = None  # 클래스 변수로 이미지 로드 공유

    def __init__(self, x, y):
        if Random_box.image is None:
            Random_box.image = load_image('Items.png')  # Items 이미지 로드
        self.x = x
        self.y = y
        self.sprite_x = 48      # 스프라이트 시트 내 x 좌표
        self.sprite_y = 240     # 스프라이트 시트 내 y 좌표
        self.width = 16         # 원본 스프라이트 너비
        self.height = 16        # 원본 스프라이트 높이
        self.scale = 3          # 이미지 확대 배율
        self.changed = False

    def update(self):
        pass  # Random_box는 정적이므로 업데이트할 필요 없음

    def draw(self):
        # 이미지 그리기
        Random_box.image.clip_draw(
            self.sprite_x, self.sprite_y, self.width, self.height,
            self.x, self.y, self.width * self.scale, self.height * self.scale
        )
        # 디버깅용 히트박스 그리기
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_top_bb())
        draw_rectangle(*self.get_bottom_bb())
        draw_rectangle(*self.get_left_bb())
        draw_rectangle(*self.get_right_bb())

    # 히트박스 메서드들
    def get_bb(self):
        return self.x - (self.width * self.scale) / 2, self.y - (self.height * self.scale) / 2, self.x + (self.width * self.scale) / 2, self.y + (self.height * self.scale) / 2

    def get_top_bb(self):
        half_width = (self.width * self.scale) / 2
        top = self.y + (self.height * self.scale) / 2
        return (
            self.x - half_width, top,
            self.x + half_width, top + 4  # 상단 4 픽셀 확장
        )

    def get_bottom_bb(self):
        half_width = (self.width * self.scale) / 2
        bottom = self.y - (self.height * self.scale) / 2
        return (
            self.x - half_width, bottom - 4,  # 하단 4 픽셀 확장
            self.x + half_width, bottom
        )

    def get_left_bb(self):
        half_height = (self.height * self.scale) / 2
        left = self.x - (self.width * self.scale) / 2
        return (
            left - 4, self.y - half_height,  # 왼쪽 4 픽셀 확장
            left, self.y + half_height
        )

    def get_right_bb(self):
        half_height = (self.height * self.scale) / 2
        right = self.x + (self.width * self.scale) / 2
        return (
            right, self.y - half_height,
            right + 4, self.y + half_height  # 오른쪽 4 픽셀 확장
        )

    def handle_collision(self, group, other, hit_position):
        if group == 'mario:random_box_bottom' and not self.changed:
            print("Random Box가 마리오에게 밑에서 맞았습니다. 스프라이트를 변경합니다.")
            self.sprite_x = 0
            self.sprite_y = 240
            self.changed = True  # 상태를 변경하여 이후에는 다시 변경되지 않도록 함
