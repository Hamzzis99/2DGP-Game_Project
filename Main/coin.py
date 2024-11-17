# coin.py

from pico2d import load_image, draw_rectangle
import game_framework
import game_world

class Coin:
    image = None  # 클래스 변수로 이미지 로드 공유

    def __init__(self, x, y):
        if Coin.image is None:
            Coin.image = load_image('Items.png')  # Items 이미지 로드
        self.x = x
        self.y = y
        self.sprite_x_positions = [0, 16, 32, 48]  # 코인의 애니메이션 프레임 x 좌표들
        self.sprite_y = 112     # 코인의 스프라이트 y 좌표
        self.width = 16         # 스프라이트 너비
        self.height = 16        # 스프라이트 높이
        self.scale = 1.5        # 이미지 확대 배율 변경 (3 -> 1.5)
        self.velocity_y = 100   # 코인의 상승 속도 (픽셀/초) - 스케일에 맞게 조정
        self.lifetime = 1.0     # 코인의 존재 시간 (초)
        self.timer = self.lifetime
        self.frame = 0          # 애니메이션 프레임 인덱스
        self.total_frames = len(self.sprite_x_positions)
        self.frame_time = 0.0   # 프레임 시간 누적

        # 애니메이션 속도 설정
        self.time_per_action = 0.25  # 한 사이클에 걸리는 시간 (초)
        self.action_per_time = 1.0 / self.time_per_action
        self.frames_per_action = self.total_frames

    def update(self):
        # 위로 상승
        self.y += self.velocity_y * game_framework.frame_time
        # 존재 시간 감소
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            # 게임 월드에서 제거
            game_world.remove_object(self)
            return

        # 애니메이션 프레임 업데이트
        self.frame_time += game_framework.frame_time
        frame_progress = self.frame_time / self.time_per_action
        self.frame = int(frame_progress * self.total_frames) % self.total_frames

    def draw(self):
        adjusted_sprite_y = Coin.image.h - self.sprite_y - self.height
        sprite_x = self.sprite_x_positions[self.frame]

        Coin.image.clip_draw(
            sprite_x, adjusted_sprite_y, self.width, self.height,
            self.x, self.y, self.width * self.scale, self.height * self.scale
        )
        # 충돌 박스 그리기 (디버깅용)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        half_width = (self.width * self.scale) / 2
        half_height = (self.height * self.scale) / 2
        return (self.x - half_width,
                self.y - half_height,
                self.x + half_width,
                self.y + half_height)

    def handle_collision(self, group, other, hit_position):
        pass  # 코인은 충돌 처리가 필요 없음
