# items/mushroom.py

from pico2d import load_image, load_wav
import game_world
from game_object import GameObject  # GameObject 베이스 클래스 임포트
from utils.camera import Camera      # Camera 클래스 임포트

class Mushroom(GameObject):
    image = None              # 클래스 변수로 이미지 공유
    collect_sound = None      # 클래스 변수로 수집 시 소리 로드 공유
    create_sound = None       # 클래스 변수로 생성 시 소리 로드 공유

    def __init__(self, x, y):
        # 이미지 로드
        if Mushroom.image is None:
            Mushroom.image = load_image('img/Items.png')  # Items 이미지 로드

        # 머쉬룸 생성 시 소리 로드 및 재생 (upgradebox.ogg)
        if Mushroom.create_sound is None:
            Mushroom.create_sound = load_wav('sound/upgradebox.ogg')  # Mushroom 생성 시 소리 로드
            Mushroom.create_sound.set_volume(20)  # 필요에 따라 볼륨 설정
        Mushroom.create_sound.play()  # Mushroom 생성 시 소리 재생

        # 머쉬룸 수집 시 소리 로드 (powerup.ogg)
        if Mushroom.collect_sound is None:
            Mushroom.collect_sound = load_wav('sound/powerup.ogg')  # Mushroom 수집 사운드 로드
            Mushroom.collect_sound.set_volume(20)  # 필요에 따라 볼륨 설정

        # 머쉬룸의 위치 및 속성 설정
        self.x = x
        self.y = y
        self.sprite_x = 0        # 머쉬룸의 고정 스프라이트 x 좌표 (Items.png 내 위치에 맞게 조정)
        self.sprite_y = 16       # 머쉬룸의 스프라이트 y 좌표 (Items.png 내 위치에 맞게 조정)
        self.width = 16          # 스프라이트 너비
        self.height = 16         # 스프라이트 높이
        self.scale = 1.5         # 이미지 확대 배율

    def update(self):
        pass  # 머쉬룸이 움직이지 않으므로 아무 동작도 하지 않음

    def draw(self):
        adjusted_sprite_y = Mushroom.image.h - self.sprite_y - self.height
        Mushroom.image.clip_draw(
            self.sprite_x, adjusted_sprite_y, self.width, self.height,
            self.x, self.y, self.width * self.scale, self.height * self.scale
        )
        # 충돌 박스 그리기 (디버깅용)
        # draw_rectangle(*self.get_bb())

    def draw_with_camera(self, camera: Camera):
        screen_x, screen_y = camera.apply(self.x, self.y)  # 카메라 적용 위치 계산
        adjusted_sprite_y = Mushroom.image.h - self.sprite_y - self.height
        Mushroom.image.clip_draw(
            self.sprite_x, adjusted_sprite_y, self.width, self.height,
            screen_x, screen_y, self.width * self.scale, self.height * self.scale
        )
        # 충돌 박스 그리기 (디버깅용)
        # draw_rectangle(*self.get_bb_offset(camera))

    def get_bb(self):
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

    def handle_collision(self, group, other, hit_position):
        # 충돌 처리 로직이 이제 mario.py로 통합되었으므로, 여기는 pass로 설정
        pass
