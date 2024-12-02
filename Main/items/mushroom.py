# items/mushroom.py

from pico2d import load_image, load_wav, draw_rectangle
import game_world
from game_object import GameObject
from utils.camera import Camera
import game_framework

class Mushroom(GameObject):
    image = None
    collect_sound = None
    create_sound = None

    def __init__(self, x, y):
        # 이미지 로드
        if Mushroom.image is None:
            Mushroom.image = load_image('img/Items.png')  # Items 이미지 로드

        # 생성 시 소리 재생
        if Mushroom.create_sound is None:
            Mushroom.create_sound = load_wav('sound/upgradebox.ogg')
            Mushroom.create_sound.set_volume(20)
        Mushroom.create_sound.play()

        # 수집 시 소리 로드
        if Mushroom.collect_sound is None:
            Mushroom.collect_sound = load_wav('sound/powerup.ogg')
            Mushroom.collect_sound.set_volume(20)

        # 위치 및 속성 설정
        self.x = x
        self.y = y
        self.sprite_x = 0
        self.sprite_y = 16
        self.width = 16
        self.height = 16
        self.scale = 1.5
        self.changed = False  # 상태 변화 여부

        # 애니메이션 변수
        self.frame = 0
        self.frame_time = 0.0
        self.animation_speed = 0.1  # 초당 프레임 변화 속도
        self.total_frames = 3  # 애니메이션 프레임 수

        # 이동 상태 변수
        self.state = 'idle'  # 'idle', 'moving_right', 'falling'
        self.move_timer = 0.0  # 상태 전환 타이머
        self.velocity_x = 100  # 오른쪽 이동 속도 (픽셀/초)
        self.velocity_y = 0  # 수직 속도
        self.gravity = -700  # 중력 가속도 (픽셀/초^2)
        self.is_on_ground = False  # 바닥에 서 있는지 여부

    def update(self):
        frame_time = game_framework.frame_time

        # Ground 상태 초기화
        self.is_on_ground = False

        # 애니메이션 업데이트
        self.frame_time += frame_time
        if self.frame_time >= self.animation_speed:
            self.frame = (self.frame + 1) % self.total_frames
            self.frame_time -= self.animation_speed

        # 상태별 동작 처리
        if self.state == 'idle':
            self.move_timer += frame_time
            if self.move_timer >= 0.5:
                self.state = 'moving_right'
                self.move_timer = 0.0
                print("Mushroom 상태가 'moving_right'로 변경되었습니다.")
        elif self.state == 'moving_right':
            # 오른쪽으로 이동
            self.x += self.velocity_x * frame_time
            # 중력 적용
            self.velocity_y += self.gravity * frame_time
            self.y += self.velocity_y * frame_time
        elif self.state == 'falling':
            # 중력 적용 및 이동
            self.velocity_y += self.gravity * frame_time
            self.y += self.velocity_y * frame_time
            self.x += self.velocity_x * frame_time  # 계속 오른쪽으로 이동

            # 화면 아래로 떨어지면 제거
            if self.y < 0:
                game_world.remove_object(self)
                print("Mushroom이 화면 아래로 떨어져 제거되었습니다.")

        # 바닥에 서 있지 않다면 'falling' 상태로 전환
        if not self.is_on_ground and self.state != 'falling':
            self.state = 'falling'
            print("Mushroom이 바닥을 벗어나 'falling' 상태로 변경되었습니다.")

    def draw(self):
        # 애니메이션 프레임 계산
        frame_width = self.width
        frame_height = self.height
        frame_x = self.sprite_x + self.frame * frame_width
        adjusted_sprite_y = Mushroom.image.h - self.sprite_y - self.height
        Mushroom.image.clip_draw(
            frame_x, adjusted_sprite_y, frame_width, frame_height,
            self.x, self.y, self.width * self.scale, self.height * self.scale
        )
        # 디버깅용 충돌 박스 그리기
        draw_rectangle(*self.get_bb())

    def draw_with_camera(self, camera: Camera):
        screen_x, screen_y = camera.apply(self.x, self.y)
        frame_width = self.width
        frame_height = self.height
        frame_x = self.sprite_x + self.frame * frame_width
        adjusted_sprite_y = Mushroom.image.h - self.sprite_y - self.height
        Mushroom.image.clip_draw(
            frame_x, adjusted_sprite_y, frame_width, frame_height,
            screen_x, screen_y, self.width * self.scale, self.height * self.scale
        )
        # 디버깅용 충돌 박스 그리기
        draw_rectangle(*self.get_bb_offset(camera))

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
        if self.state == 'moving_right':
            if group.endswith('top'):
                # 바닥(Brick, Mushroom_box, Grass) 위에 서 있음
                self.velocity_y = 0
                self.state = 'moving_right'
                self.is_on_ground = True
                print(f"Mushroom이 {group} 위에 서 있습니다.")
            elif group.endswith('left') or group.endswith('right') or group.endswith('bottom'):
                # 벽이나 장애물과 충돌하여 떨어지기 시작
                self.state = 'falling'
                self.velocity_x = 0  # 충돌 시 수평 속도 정지
                self.velocity_y = 0
                print(f"Mushroom이 {group}과 충돌하여 'falling' 상태로 변경되었습니다.")
        elif self.state == 'falling':
            if group.endswith('top'):
                # 바닥(Brick, Mushroom_box, Grass) 위에 착지
                self.y = other.y + (other.height * other.scale) / 2 + (self.height * self.scale) / 2
                self.velocity_y = 0
                self.state = 'moving_right'
                self.is_on_ground = True
                print(f"Mushroom이 {group} 위에 착지하여 'moving_right' 상태로 변경되었습니다.")
