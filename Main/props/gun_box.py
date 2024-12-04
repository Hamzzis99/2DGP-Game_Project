# props/gun_box.py

from pico2d import load_image, draw_rectangle
from game_object import GameObject
from utils.camera import Camera
import game_framework

# play_mode의 objects_to_add 리스트를 import

class Gun_box(GameObject):
    image = None  # 클래스 변수로 이미지 로드 공유

    def __init__(self, x, y):
        if Gun_box.image is None:
            Gun_box.image = load_image('img/tiles.png')  # Items 이미지 로드
        self.x = x
        self.y = y
        self.sprite_y = 0  # 스프라이트 시트 내 y 좌표 (고정)
        self.width = 16      # 원본 스프라이트 너비
        self.height = 16     # 원본 스프라이트 높이
        self.scale = 1.5     # 이미지 확대 배율 변경 (1.5로 조정)
        self.changed = False # 상태 변화 여부

        # 애니메이션 관련 변수
        self.sprite_x_positions = [384, 400, 416]  # 애니메이션 프레임 x 좌표들
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
        adjusted_sprite_y = Gun_box.image.h - self.sprite_y - self.height
        if not self.changed:
            sprite_x = self.sprite_x_positions[self.frame]
        else:
            sprite_x = 0  # 상태 변경 후에는 동일한 스프라이트 사용
        Gun_box.image.clip_draw(
            sprite_x, adjusted_sprite_y, self.width, self.height,
            self.x, self.y, self.width * self.scale, self.height * self.scale
        )
        # 충돌 박스 그리기 (디버깅용)
        #draw_rectangle(*self.get_bb())
        #draw_rectangle(*self.get_top_bb())
        #draw_rectangle(*self.get_bottom_bb())
        #draw_rectangle(*self.get_left_bb())
        #draw_rectangle(*self.get_right_bb())

    def draw_with_camera(self, camera: Camera):
        adjusted_sprite_y = Gun_box.image.h - self.sprite_y - self.height
        if not self.changed:
            sprite_x = self.sprite_x_positions[self.frame]
        else:
            sprite_x = 432  # 상태 변경 후에는 동일한 스프라이트 사용
        screen_x, screen_y = camera.apply(self.x, self.y)
        Gun_box.image.clip_draw(
            sprite_x, adjusted_sprite_y, self.width, self.height,
            screen_x, screen_y, self.width * self.scale, self.height * self.scale
        )
        # 충돌 박스 그리기 (디버깅용)
        #draw_rectangle(*self.get_bb_offset(camera))
        #draw_rectangle(*self.get_top_bb_offset(camera))
        #draw_rectangle(*self.get_bottom_bb_offset(camera))
        #draw_rectangle(*self.get_left_bb_offset(camera))
        #draw_rectangle(*self.get_right_bb_offset(camera))

    # 히트박스 메서드들
    def get_bb(self):
        # 전체 Gun_box의 충돌 박스
        half_width = (self.width * self.scale) / 2
        half_height = (self.height * self.scale) / 2
        return (
            self.x - half_width,
            self.y - half_height,
            self.x + half_width,
            self.y + half_height
        )

    def get_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bb()
        return (
            left - camera.camera_x,
            bottom - camera.camera_y,
            right - camera.camera_x,
            top - camera.camera_y
        )

    def get_top_bb(self):
        # Gun_box 상단의 충돌 박스 (좌우로 1픽셀씩 줄이고 y 범위도 축소)
        half_width = (self.width * self.scale) / 2 - 1
        return (
            self.x - half_width,
            self.y + (self.height * self.scale) / 2 - 2,
            self.x + half_width,
            self.y + (self.height * self.scale) / 2 + 2
        )

    def get_top_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_top_bb()
        return (
            left - camera.camera_x,
            bottom - camera.camera_y,
            right - camera.camera_x,
            top - camera.camera_y
        )

    def get_bottom_bb(self):
        # Gun_box 하단의 충돌 박스 (좌우로 1픽셀씩 줄이고 y 범위도 축소)
        half_width = (self.width * self.scale) / 2 - 1
        return (
            self.x - half_width,
            self.y - (self.height * self.scale) / 2 - 2,
            self.x + half_width,
            self.y - (self.height * self.scale) / 2 + 2
        )

    def get_bottom_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bottom_bb()
        return (
            left - camera.camera_x,
            bottom - camera.camera_y,
            right - camera.camera_x,
            top - camera.camera_y
        )

    def get_left_bb(self):
        # Gun_box 왼쪽의 충돌 박스 (위아래로 1픽셀씩 줄임)
        half_width = (self.width * self.scale) / 2
        half_height = (self.height * self.scale) / 2 - 1  # 상하로 1픽셀씩 줄임
        return (
            self.x - half_width - 1,
            self.y - half_height,
            self.x - half_width,
            self.y + half_height
        )

    def get_left_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_left_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_right_bb(self):
        # Gun_box 오른쪽의 충돌 박스 (위아래로 1픽셀씩 줄임)
        half_width = (self.width * self.scale) / 2
        half_height = (self.height * self.scale) / 2 - 1  # 상하로 1픽셀씩 줄임
        return (
            self.x + half_width,
            self.y - half_height,
            self.x + half_width + 1,
            self.y + half_height
        )

    def get_right_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_right_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def handle_collision(self, group, other, hit_position):
        # 충돌 처리 로직이 이제 mario.py로 통합되었으므로, 여기는 pass로 설정
        pass
