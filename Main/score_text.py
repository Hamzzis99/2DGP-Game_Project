# score_text.py

from pico2d import *

import game_world
from game_object import GameObject  # GameObject 임포트 추가
from utils.camera import Camera      # Camera 클래스 임포트
from utils.font import Font          # Font 클래스 임포트

class ScoreText(GameObject):
    def __init__(self, x, y, text, duration=3.0):
        self.x = x
        self.y = y
        self.text = text
        self.duration = duration
        self.start_time = get_time()
        self.font = Font("img/font.png", char_width=8, char_height=8)
        self.active = True

    def update(self):
        current_time = get_time()
        if current_time - self.start_time >= self.duration:
            game_world.remove_object(self)

    def draw(self):
        self.font.draw(self.text, self.x, self.y, camera=None, scaling_factor=2)

    def draw_with_camera(self, camera: Camera):
        screen_x, screen_y = camera.apply(self.x, self.y)
        self.font.draw(self.text, screen_x, screen_y, camera=None, scaling_factor=2)

    def get_bb(self):
        return ()

    def handle_collision(self, group, other, hit_position):
        pass
