# coin.py

from pico2d import load_image, draw_rectangle, load_wav
import game_framework
import game_world
from game_object import GameObject  # GameObject 베이스 클래스 임포트
from utils.camera import Camera      # Camera 클래스 임포트

class Coin(GameObject):
    image = None  # 클래스 변수로 이미지 로드 공유
    coin_sound = None  # 사운드 공유를 위해 클래스 변수로 초기화

    def __init__(self, x, y):
        if Coin.image is None:
            Coin.image = load_image('img/Items.png')  # Items 이미지 로드
        if Coin.coin_sound is None:
            Coin.coin_sound = load_wav('sound/coin.ogg')  # 코인 사운드 로드
            Coin.coin_sound.set_volume(20)  # 필요에 따라 볼륨 설정

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

        # 코인 사운드 재생
        Coin.coin_sound.play()

    def update(self):
        frame_time = game_framework.frame_time  # 전역 frame_time 사용

        # 위로 상승
        self.y += self.velocity_y * frame_time

        # 존재 시간 감소
        self.timer -= frame_time
        if self.timer <= 0:
            # 게임 월드에서 제거
            game_world.remove_object(self)
            return

        # 애니메이션 프레임 업데이트
        self.frame_time += frame_time
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

    def draw_with_camera(self, camera: Camera):
        screen_x, screen_y = camera.apply(self.x, self.y)  # 카메라 적용 위치 계산

        adjusted_sprite_y = Coin.image.h - self.sprite_y - self.height
        sprite_x = self.sprite_x_positions[self.frame]

        Coin.image.clip_draw(
            sprite_x, adjusted_sprite_y, self.width, self.height,
            screen_x, screen_y, self.width * self.scale, self.height * self.scale
        )
        # 충돌 박스 그리기 (디버깅용)
        draw_rectangle(*self.get_bb_offset(camera))

    def get_bb(self):
        half_width = (self.width * self.scale) / 2
        half_height = (self.height * self.scale) / 2
        return (self.x - half_width,
                self.y - half_height,
                self.x + half_width,
                self.y + half_height)

    def get_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def handle_collision(self, group, other, hit_position):
        pass  # 코인은 충돌 처리가 필요 없음
