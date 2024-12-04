# enemy/fake_brick.py

from pico2d import load_image, draw_rectangle
from game_object import GameObject
from states import game_state
from utils.camera import Camera
import game_world
from items.coin import Coin
import game_framework
from utils.score_text import ScoreText  # ScoreText 클래스 임포트 추가


class Fake_brick(GameObject):
    image = None  # 클래스 변수로 이미지 로드 공유

    def __init__(self, x, y):
        if Fake_brick.image is None:
            Fake_brick.image = load_image('img/tiles.png')  # Items 이미지 로드
            # Fake_brick.image.set_color_key((255, 255, 255))  # 흰색을 투명하게 설정 (필요 시)
        self.x = x
        self.y = y
        self.sprite_y = 0  # 스프라이트 시트 내 y 좌표 (고정)
        self.width = 16      # 원본 스프라이트 너비
        self.height = 16     # 원본 스프라이트 높이
        self.scale = 1.5     # 이미지 확대 배율 변경 (1.5로 조정)
        self.changed = False # 상태 변화 여부

        # 애니메이션 관련 변수
        self.sprite_x_positions = [0]  # 애니메이션 프레임 x 좌표들
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
            #print(f"Fake_brick Frame: {self.frame}")  # 디버깅용 출력
        else:
            self.frame = 0  # 상태 변경 후에는 첫 번째 프레임 사용

    def draw(self):
        if self.changed:
            # 변경된 상태일 때는 아무 것도 그리지 않음
            return
        else:
            # 애니메이션 상태일 때 이미지 그리기
            adjusted_sprite_y = Fake_brick.image.h - self.sprite_y - self.height
            sprite_x = self.sprite_x_positions[self.frame]
            Fake_brick.image.clip_draw(
                sprite_x, adjusted_sprite_y, self.width, self.height,
                self.x, self.y, self.width * self.scale, self.height * self.scale
            )

        # 충돌 박스 그리기 (디버깅용, 항상 그려짐)
        #draw_rectangle(*self.get_bb())
        #draw_rectangle(*self.get_top_bb())
        #draw_rectangle(*self.get_bottom_bb())
        #draw_rectangle(*self.get_left_bb())
        #draw_rectangle(*self.get_right_bb())

    def draw_with_camera(self, camera: Camera):
        if self.changed:
            # 변경된 상태일 때는 아무 것도 그리지 않음
            return
        else:
            # 애니메이션 상태일 때 이미지 그리기
            adjusted_sprite_y = Fake_brick.image.h - self.sprite_y - self.height
            sprite_x = self.sprite_x_positions[self.frame]
            screen_x, screen_y = camera.apply(self.x, self.y)
            Fake_brick.image.clip_draw(
                sprite_x, adjusted_sprite_y, self.width, self.height,
                screen_x, screen_y, self.width * self.scale, self.height * self.scale
            )

        # 충돌 박스 그리기 (디버깅용, 항상 그려짐)
        #draw_rectangle(*self.get_bb_offset(camera))
        #draw_rectangle(*self.get_top_bb_offset(camera))
        #draw_rectangle(*self.get_bottom_bb_offset(camera))
        #draw_rectangle(*self.get_left_bb_offset(camera))
        #draw_rectangle(*self.get_right_bb_offset(camera))

    # 히트박스 메서드들 (변경 없음)
    def get_bb(self):
        # 전체 Fake_brick의 충돌 박스
        half_width = (self.width * self.scale) / 2
        half_height = (self.height * self.scale) / 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_top_bb(self):
        # Fake_brick 상단의 충돌 박스 (좌우로 1픽셀씩 줄이고 y 범위도 축소)
        half_width = (self.width * self.scale) / 2 - 1
        return self.x - half_width, self.y + (self.height * self.scale) / 2 - 2, \
               self.x + half_width, self.y + (self.height * self.scale) / 2 + 2

    def get_top_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_top_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_bottom_bb(self):
        # Fake_brick 하단의 충돌 박스 (좌우로 1픽셀씩 줄이고 y 범위도 축소)
        half_width = (self.width * self.scale) / 2 - 1
        return self.x - half_width, self.y - (self.height * self.scale) / 2 - 2, \
               self.x + half_width, self.y - (self.height * self.scale) / 2 + 2

    def get_bottom_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bottom_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_left_bb(self):
        # Fake_brick 왼쪽의 충돌 박스 (위아래로 1픽셀씩 줄임)
        half_width = (self.width * self.scale) / 2
        half_height = (self.height * self.scale) / 2 - 1  # 상하로 1픽셀씩 줄임
        return self.x - half_width - 1, self.y - half_height, self.x - half_width, self.y + half_height

    def get_left_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_left_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_right_bb(self):
        # Fake_brick 오른쪽의 충돌 박스 (위아래로 1픽셀씩 줄임)
        half_width = (self.width * self.scale) / 2
        half_height = (self.height * self.scale) / 2 - 1  # 상하로 1픽셀씩 줄임
        return self.x + half_width, self.y - half_height, self.x + half_width + 1, self.y + half_height

    def get_right_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_right_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def handle_collision(self, group, other, hit_position, hit_side=None):
        """
        hit_side: 문자열로 'top', 'bottom', 'left', 'right' 중 하나
        """
        if not self.changed and group.startswith('mario:fake_brick'):
            print(f"Collision detected with Mario at position: {hit_position}, side: {hit_side}")  # 디버깅용 출력
            self.changed = True  # 박스 상태 변경

            # 코인 생성
            coin = Coin(self.x, self.y + self.height * self.scale / 2 + 10)  # 박스 위에 생성
            game_world.add_object(coin, 1)  # 적절한 층에 추가

            game_state.score += 1000  # 점수는 필요에 따라 조정 가능
            print(f"Score increased by 1000. Total Score: {game_state.score}")

            # 점수 텍스트 생성
            score_text = ScoreText(self.x, self.y + self.height * self.scale / 2 + 20, "+1000")  # 문자열 전달
            game_world.add_object(score_text, 2)

            # 사운드 재생 (선택 사항)
            # coin_sound.play()
