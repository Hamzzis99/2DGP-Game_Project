# enemy/boss_turtle.py
from pico2d import load_image, clamp, draw_rectangle
from game_object import GameObject
from states import game_state
from utils.camera import Camera
import random
import game_framework
import game_world

# Boss_turtle Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boss_turtle Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2.0  # 두 가지 프레임으로 애니메이션

class Boss_turtle(GameObject):
    image = None  # 스프라이트 시트 이미지

    def load_images(self):
        if Boss_turtle.image is None:
            Boss_turtle.image = load_image('img/character.png')  # 스프라이트 시트 로드

        # 애니메이션 프레임 좌표 설정
        self.normal_frame_x_positions = [293, 312]
        self.normal_frame_y_position = 169
        self.frame_width = 20
        self.frame_height = 29

    def __init__(self, scale=1.0, initial_y=300):
        """
        Boss_turtle 초기화
        :param scale: 캐릭터의 스케일 (기본값: 1.0)
        :param initial_y: Boss_turtle의 초기 y 좌표 (기본값: 300)
        """
        self.x, self.y = random.randint(1000, 1400), initial_y  # 초기 위치 설정
        self.load_images()
        self.frame = random.randint(0, 1)  # 초기 프레임 (0 또는 1)
        self.dir = random.choice([-1, 1])  # 초기 이동 방향: -1(왼쪽), 1(오른쪽)
        self.alive = True  # 살아있는 상태
        self.state = 'normal'  # 현재 상태: 항상 'normal' 상태
        self.frame_time = 0.0  # 애니메이션 시간
        self.scale = scale  # 스케일 설정

        self.hp = 2  # Boss_turtle의 HP 설정

    def update(self):
        frame_time = game_framework.frame_time  # 전역 frame_time 사용

        if not self.alive:
            return

        # 애니메이션 프레임 업데이트
        self.frame_time += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.frame_time) % len(self.normal_frame_x_positions)

        # 위치 업데이트
        self.x += RUN_SPEED_PPS * self.dir * frame_time

        # 위치 클램프 (방향 전환은 play_mode.py에서 관리)
        self.x = clamp(1000, self.x, 1400)

    def draw_with_camera(self, camera: Camera):
        if not self.alive:
            return  # 살아있지 않으면 그리지 않음

        screen_x, screen_y = camera.apply(self.x, self.y)

        # 현재 프레임 인덱스 (0 또는 1)
        frame_x = self.normal_frame_x_positions[self.frame]
        frame_y = self.normal_frame_y_position

        # 그릴 크기 설정 (스케일 적용)
        dest_width, dest_height = self.frame_width * self.scale, self.frame_height * self.scale  # 화면에 그릴 크기

        if self.dir < 0:
            # 왼쪽으로 이동 중이면 프레임을 수평 반전하여 그립니다.
            Boss_turtle.image.clip_composite_draw(
                frame_x, frame_y, self.frame_width, self.frame_height, 0, 'h',
                screen_x, screen_y, dest_width, dest_height
            )
        else:
            # 오른쪽으로 이동 중이면 프레임을 그대로 그립니다.
            Boss_turtle.image.clip_draw(
                frame_x, frame_y, self.frame_width, self.frame_height,
                screen_x, screen_y, dest_width, dest_height
            )

        # 히트박스 그리기 (디버깅용)
        draw_rectangle(*self.get_bb_offset(camera))
        draw_rectangle(*self.get_top_bb_offset(camera))
        draw_rectangle(*self.get_bottom_bb_offset(camera))

    def get_bb(self):
        """
        히트박스 계산 (스케일 적용)
        :return: (left, bottom, right, top)
        """
        width = self.frame_width * self.scale  # 이미지의 폭 * 스케일
        height = self.frame_height * self.scale  # 이미지의 높이 * 스케일
        half_width = width / 2
        half_height = height / 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_top_bb(self):
        """
        Top 히트박스: Boss_turtle의 머리 부분 (스케일 적용)
        :return: (left, bottom, right, top)
        """
        return (self.x - 13 * self.scale, self.y + 10 * self.scale,
                self.x + 13 * self.scale, self.y + 25 * self.scale)  # (left, bottom, right, top)

    def get_top_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_top_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_bottom_bb(self):
        """
        Bottom 히트박스: Boss_turtle의 몸통 부분 (스케일 적용)
        :return: (left, bottom, right, top)
        """
        return (self.x - 15 * self.scale, self.y - 15 * self.scale,
                self.x + 15 * self.scale, self.y + 20 * self.scale)  # (left, bottom, right, top)

    def get_bottom_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bottom_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def set_dir(self, dir):
        """
        적의 이동 방향을 설정합니다.
        :param dir: -1 (왼쪽), 1 (오른쪽)
        """
        self.dir = dir

    def handle_collision(self, group, other, hit_position):
        if not self.alive:
            return

        if group == 'fire_ball:boss_turtle':
            print(f"Boss_turtle이 Ball에 맞았습니다. 현재 HP: {self.hp}")
            self.hp -= 1  # HP 감소

            # Ball 제거는 ball.py에서 처리
            # 여기서는 HP만 관리

            if self.hp <= 0:
                self.alive = False
                game_world.remove_object(self)
                print("Boss_turtle이 파괴되었습니다.")

        else:
            pass  # 다른 충돌 그룹에 대한 처리는 필요 없으므로 pass
