import random

from pico2d import get_time


class Camera:
    def __init__(self, screen_width, screen_height, world_width, world_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        self.camera_x = 0
        self.camera_y = 0

        # 흔들기 관련 속성 추가
        self.is_shaking = False
        self.shake_duration = 0.0
        self.shake_start_time = 0.0
        self.shake_magnitude = 5  # 흔들림의 세기 (픽셀 단위)

    def update(self, target):
        # 타겟(Mario)의 위치를 기반으로 카메라 위치를 업데이트
        self.camera_x = target.x - self.screen_width // 2
        self.camera_y = target.y - self.screen_height // 2

        # 카메라가 월드 밖으로 나가지 않도록 제한
        self.camera_x = max(0, min(self.camera_x, self.world_width - self.screen_width))
        self.camera_y = max(0, min(self.camera_y, self.world_height - self.screen_height))

        # 흔들기 효과 업데이트
        if self.is_shaking:
            current_time = get_time()
            elapsed_time = current_time - self.shake_start_time
            if elapsed_time < self.shake_duration:
                # 흔들림을 적용 (무작위로 x, y 오프셋을 추가)
                offset_x = random.randint(-self.shake_magnitude, self.shake_magnitude)
                offset_y = random.randint(-self.shake_magnitude, self.shake_magnitude)
                self.camera_x += offset_x
                self.camera_y += offset_y

                # 카메라가 월드 밖으로 나가지 않도록 다시 제한
                self.camera_x = max(0, min(self.camera_x, self.world_width - self.screen_width))
                self.camera_y = max(0, min(self.camera_y, self.world_height - self.screen_height))
            else:
                # 흔들기 종료
                self.is_shaking = False

    def apply(self, x, y):
        # 객체의 월드 좌표를 화면 좌표로 변환
        screen_x = x - self.camera_x
        screen_y = y - self.camera_y
        return screen_x, screen_y

    def start_shake(self, duration, magnitude=5):
        """카메라 흔들기 시작"""
        self.is_shaking = True
        self.shake_duration = duration
        self.shake_start_time = get_time()
        self.shake_magnitude = magnitude
        print(f"Camera shaking started for {duration} seconds with magnitude {magnitude}.")