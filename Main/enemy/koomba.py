# enemy/koomba.py

from pico2d import load_image, draw_rectangle, clamp, load_wav
from game_object import GameObject
from utils.camera import Camera
import random
import game_framework
import game_world

# Koomba Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Koomba Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2.0  # 두 가지 프레임으로 애니메이션

class Koomba(GameObject):
    image = None  # 스프라이트 시트 이미지

    def load_images(self):
        if Koomba.image is None:
            Koomba.image = load_image('img/character.png')  # 스프라이트 시트 로드

        # 애니메이션 프레임 좌표 설정
        self.frame_x_positions = [296, 315]
        self.frame_y_position = 196
        self.frame_width = 16
        self.frame_height = 20

        # 납작해진 Koomba의 스프라이트 좌표
        self.stomped_frame_x = 276  # 납작해진 굼바의 스프라이트 x 좌표
        self.stomped_frame_y = 196  # 납작해진 굼바의 스프라이트 y 좌표
        self.stomped_frame_width = 16
        self.stomped_frame_height = 16  # 납작해진 Koomba의 높이

    def __init__(self, x, y, move_distance=100):
        """
        Koomba 초기화
        :param x: Koomba의 초기 x 좌표
        :param y: Koomba의 초기 y 좌표
        :param move_distance: Koomba의 이동 거리
        """
        self.start_x = x  # 이동 범위의 시작점
        self.move_distance = move_distance  # 이동 거리 설정
        self.x, self.y = x, y  # 초기 위치 설정
        self.load_images()
        self.frame = random.randint(0, 1)  # 초기 프레임 (0 또는 1)
        self.dir = 1  # 초기 이동 방향: 1(오른쪽)
        self.alive = True  # 살아있는 상태
        self.stomped = False  # 굼바가 밟혔는지 여부
        self.stomp_timer = 0.3  # 밟힌 후 0.3초 후 제거 (디버깅용)
        self.frame_time = 0  # 애니메이션 시간

        self.stomp_sound = load_wav('sound/koomba.ogg')  # 사운드 파일 로드
        self.stomp_sound.set_volume(20)  # 필요에 따라 볼륨 설정
        self.stomp_sound_played = False  # Stomp 사운드 재생 여부

    def update(self):
        frame_time = game_framework.frame_time  # 전역 frame_time 사용
        if self.stomped:
            if not self.stomp_sound_played:
                self.stomp_sound.play()  # Stomp 사운드 한 번만 재생
                self.stomp_sound_played = True
            self.stomp_timer -= frame_time
            if self.stomp_timer <= 0:
                self.alive = False
                game_world.remove_object(self)
            return

        if not self.alive:
            return

        # 애니메이션 프레임 업데이트
        self.frame_time += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.frame_time) % len(self.frame_x_positions)

        # 위치 업데이트
        self.x += RUN_SPEED_PPS * self.dir * frame_time

        # 이동 범위 제한 및 방향 전환
        if self.x > self.start_x + self.move_distance:
            self.x = self.start_x + self.move_distance
            self.dir = -1  # 왼쪽으로 방향 전환
        elif self.x < self.start_x:
            self.x = self.start_x
            self.dir = 1  # 오른쪽으로 방향 전환

    def draw_with_camera(self, camera: Camera):
        if not self.alive:
            return  # 살아있지 않으면 그리지 않음

        screen_x, screen_y = camera.apply(self.x, self.y)

        # 그릴 크기 설정 (스케일 적용)
        dest_width, dest_height = 32, 32  # 화면에 그릴 크기

        if self.stomped:
            # 납작해진 Koomba의 스프라이트 좌표 사용
            Koomba.image.clip_draw(
                self.stomped_frame_x, self.stomped_frame_y,
                self.stomped_frame_width, self.stomped_frame_height,
                screen_x, screen_y, dest_width, dest_height
            )
        else:
            # 현재 프레임 인덱스 (0 또는 1)
            frame_x = self.frame_x_positions[self.frame]
            frame_y = self.frame_y_position
            frame_width = self.frame_width
            frame_height = self.frame_height

            if self.dir < 0:
                # 왼쪽으로 이동 중이면 프레임을 수평 반전하여 그립니다.
                Koomba.image.clip_composite_draw(
                    frame_x, frame_y, frame_width, frame_height, 0, 'h',
                    screen_x, screen_y, dest_width, dest_height
                )
            else:
                # 오른쪽으로 이동 중이면 프레임을 그대로 그립니다.
                Koomba.image.clip_draw(
                    frame_x, frame_y, frame_width, frame_height,
                    screen_x, screen_y, dest_width, dest_height
                )

        # 히트박스 그리기 (디버깅용)
        #bb_offset = self.get_bb_offset(camera)
        #if bb_offset:
            #draw_rectangle(*bb_offset)
        top_bb_offset = self.get_top_bb_offset(camera)
        #if top_bb_offset:
            #draw_rectangle(*top_bb_offset)
        bottom_bb_offset = self.get_bottom_bb_offset(camera)
        #if bottom_bb_offset:
            #draw_rectangle(*bottom_bb_offset)

    def get_bb(self):
        if self.stomped:
            # stomped 상태일 때는 충돌 박스 비활성화
            return self.x, self.y, self.x, self.y
        width = 16 * 2  # 이미지의 폭 * 스케일 (16 * 2 = 32)
        height = 20 * 1.6  # 이미지의 높이 * 스케일 (20 * 1.6 = 32)
        half_width = width / 2
        half_height = height / 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_bb_offset(self, camera: Camera):
        bb = self.get_bb()
        if len(bb) != 4:
            return None  # 올바른 히트박스가 아니면 그리지 않음
        left, bottom, right, top = bb
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_top_bb(self):
        if self.stomped:
            # stomped 상태일 때는 Top 히트박스 비활성화
            return self.x, self.y, self.x, self.y
        # 기존 Top 히트박스 반환
        return self.x - 14, self.y + 10, self.x + 14, self.y + 25

    def get_top_bb_offset(self, camera: Camera):
        bb = self.get_top_bb()
        if len(bb) != 4:
            return None
        left, bottom, right, top = bb
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_bottom_bb(self):
        if self.stomped:
            # stomped 상태일 때는 Bottom 히트박스 비활성화
            return self.x, self.y, self.x, self.y
        # 기존 Bottom 히트박스 반환
        return self.x - 15, self.y - 15, self.x + 15, self.y + 20

    def get_bottom_bb_offset(self, camera: Camera):
        bb = self.get_bottom_bb()
        if len(bb) != 4:
            return None
        left, bottom, right, top = bb
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def get_normal_bb(self):
        if self.stomped:
            # stomped 상태일 때는 Normal 히트박스 비활성화
            return self.x, self.y, self.x, self.y
        # 전체 몸을 덮는 Normal 히트박스 정의
        width = 16 * 2  # 이미지의 폭 * 스케일 (32)
        height = 20 * 1.6  # 이미지의 높이 * 스케일 (32)
        half_width = width / 2
        half_height = height / 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_normal_bb_offset(self, camera: Camera):
        bb = self.get_normal_bb()
        if len(bb) != 4:
            return None
        left, bottom, right, top = bb
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def set_dir(self, dir):
        """
        적의 이동 방향을 설정합니다.
        :param dir: -1 (왼쪽), 1 (오른쪽)
        """
        self.dir = dir

    def handle_collision(self, group, other, hit_position):
        pass
