# utils/camera.py

class Camera:
    def __init__(self, screen_width, screen_height, world_width, world_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        self.camera_x = 0
        self.camera_y = 0

    def update(self, target):
        # 타겟(Mario)의 위치를 기반으로 카메라 위치를 업데이트
        self.camera_x = target.x - self.screen_width // 2
        self.camera_y = target.y - self.screen_height // 2

        # 카메라가 월드 밖으로 나가지 않도록 제한
        self.camera_x = max(0, min(self.camera_x, self.world_width - self.screen_width))
        self.camera_y = max(0, min(self.camera_y, self.world_height - self.screen_height))

    def apply(self, x, y):
        # 객체의 월드 좌표를 화면 좌표로 변환
        screen_x = x - self.camera_x
        screen_y = y - self.camera_y
        return screen_x, screen_y
