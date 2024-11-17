from pico2d import load_image, draw_rectangle
import game_world
from coin import Coin

class Random_box:
    image = None  # 클래스 변수로 이미지 로드 공유

    def __init__(self, x, y):
        if Random_box.image is None:
            Random_box.image = load_image('Items.png')  # Items 이미지 로드
        self.x = x
        self.y = y
        self.sprite_x = 48      # 스프라이트 시트 내 x 좌표 (초기 상태)
        self.sprite_y = 240     # 스프라이트 시트 내 y 좌표
        self.width = 16         # 원본 스프라이트 너비
        self.height = 16        # 원본 스프라이트 높이
        self.scale = 3          # 이미지 확대 배율
        self.changed = False    # 상태 변화 여부

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

    def update(self):
        pass  # Random_box은 정적이므로 업데이트할 필요 없음

    def draw(self):
        # 스프라이트 시트에서 (sprite_x, sprite_y) 위치의 (width, height) 크기 영역을 잘라서 그립니다.
        # 화면에 그릴 크기는 필요에 따라 조정 (예: 3배 확장)
        Random_box.image.clip_draw(self.sprite_x, self.sprite_y, self.width, self.height, self.x, self.y, self.width * 3, self.height * 3)

    def get_bb(self):
        # 전체 Random_box의 충돌 박스 (16x16 크기 확장)
        half_width = (self.width * 3) / 2
        half_height = (self.height * 3) / 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_top_bb(self):
        # Random_box 상단의 충돌 박스 (상단 약간 확장)
        half_width = (self.width * 3) / 2
        return self.x - half_width, self.y + (self.height * 3) / 2, self.x + half_width, self.y + (self.height * 3) / 2 + 4

    def get_bottom_bb(self):
        # Random_box 하단의 충돌 박스 (하단 약간 확장)
        half_width = (self.width * 3) / 2
        return self.x - half_width, self.y - (self.height * 3) / 2 - 4, self.x + half_width, self.y - (self.height * 3) / 2

    def get_left_bb(self):
        # Random_box 왼쪽의 충돌 박스 (왼쪽 약간 확장)
        half_height = (self.height * 3) / 2
        return self.x - (self.width * 3) / 2 - 4, self.y - half_height, self.x - (self.width * 3) / 2, self.y + half_height

    def get_right_bb(self):
        # Random_box 오른쪽의 충돌 박스 (오른쪽 약간 확장)
        half_height = (self.height * 3) / 2
        return self.x + (self.width * 3) / 2, self.y - half_height, self.x + (self.width * 3) / 2 + 4, self.y + half_height


    def handle_collision(self, group, other, hit_position):
        if group == 'mario:random_box_bottom' and not self.changed:
            print("Random Box가 마리오에게 밑에서 맞았습니다. 스프라이트를 변경합니다.")
            self.sprite_x = 0
            self.sprite_y = 240
            self.changed = True  # 상태를 변경하여 이후에는 다시 변경되지 않도록 함

            coin = Coin(self.x, self.y + (self.height * self.scale))  # 박스 위에 생성
            game_world.add_object(coin, 1)  # 게임 월드에 코인 추가
        else:
            print("호출이 안 되고 있습니다.")