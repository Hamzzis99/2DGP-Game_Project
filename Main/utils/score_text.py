# utils/score_text.py

from pico2d import *

import game_framework
import game_world
from game_object import GameObject
from utils.camera import Camera
from utils.font import Font

class ScoreText(GameObject):
    def __init__(self, x, y, text, duration=3.0, velocity_y=50):
        self.x = x
        self.y = y
        self.text = text
        self.duration = duration
        self.start_time = get_time()
        self.font = Font("img/font.png", char_width=8, char_height=8)
        self.active = True
        self.velocity_y = velocity_y  # 텍스트가 위로 이동하는 속도

    def update(self):
        current_time = get_time()
        elapsed_time = current_time - self.start_time
        if elapsed_time >= self.duration:
            game_world.remove_object(self)
            return

        # 텍스트가 위로 이동하도록 y 위치 업데이트
        self.y += self.velocity_y * game_framework.frame_time

    def draw(self):
        # 카메라가 없다면 화면 좌표 그대로 그리기
        self.font.draw(self.text, self.x, self.y, camera=None, scaling_factor=1.5)

    def draw_with_camera(self, camera: Camera):
        screen_x, screen_y = camera.apply(self.x, self.y)
        self.font.draw(self.text, screen_x, screen_y, camera=None, scaling_factor=1.5)

    def get_bb(self):
        return ()

    def handle_collision(self, group, other, hit_position):
        pass
