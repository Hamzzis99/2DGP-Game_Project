#random_Box.py
from pico2d import load_image
import game_world
from coin import Coin
import game_framework

class Random_box:
    image = None  # 클래스 변수로 이미지 로드 공유

    def __init__(self, x, y):
        if Random_box.image is None:
            Random_box.image = load_image('Items.png')  # Items 이미지 로드
        self.x = x
        self.y = y
        self.sprite_y = 80  # 스프라이트 시트 내 y 좌표 (고정)
        self.width = 16      # 원본 스프라이트 너비
        self.height = 16     # 원본 스프라이트 높이
        self.scale = 3       # 이미지 확대 배율
        self.changed = False # 상태 변화 여부

        # 애니메이션 관련 변수
        self.sprite_x_positions = [0, 16, 32, 48]  # 애니메이션 프레임 x 좌표들
        self.frame = 0
        self.total_frames = len(self.sprite_x_positions)
        self.frame_time = 0.0

        # 애니메이션 속도 설정
        self.time_per_action = 0.5  # 한 사이클에 걸리는 시간 (초)
        self.action_per_time = 1.0 / self.time_per_action
        self.frames_per_action = self.total_frames

    def update(self):
        if not self.changed:
            # 애니메이션 프레임 업데이트
            self.frame_time += game_framework.frame_time
            frame_progress = self.frame_time / self.time_per_action
            self.frame = int(frame_progress * self.total_frames) % self.total_frames
        else:
            self.frame = 0  # 상태 변경 후에는 첫 번째 프레임 사용

    def draw(self):
        # 스프라이트 시트에서 (sprite_x, sprite_y) 위치의 (width, height) 크기 영역을 잘라서 그립니다.
        # 화면에 그릴 크기는 필요에 따라 조정 (예: 3배 확장)
        adjusted_sprite_y = Random_box.image.h - self.sprite_y - self.height
        if not self.changed:
            sprite_x = self.sprite_x_positions[self.frame]
        else:
            sprite_x = 0  # 상태 변경 후에는 첫 번째 프레임 고정
        Random_box.image.clip_draw(
            sprite_x, adjusted_sprite_y, self.width, self.height,
            self.x, self.y, self.width * 3, self.height * 3
        )

    # 히트박스 메서드들
    def get_bb(self):
        # 전체 Random_box의 충돌 박스
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
            print("Random Box가 마리오에게 밑에서 맞았습니다. 스프라이트를 변경하고 코인을 생성합니다.")
            self.changed = True

            # 코인 생성
            coin = Coin(self.x, self.y + (self.height * 3))  # 박스 위에 생성
            game_world.add_object(coin, 1)
