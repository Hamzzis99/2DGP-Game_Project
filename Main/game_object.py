# game_object.py

from pico2d import draw_rectangle

class GameObject:
    def update(self):
        pass

    def draw(self):
        pass

    def draw_with_camera(self, camera):
        pass

    def get_bb(self):
        pass

    def get_bb_offset(self, camera):
        pass

    def get_top_bb(self):
        pass

    def get_top_bb_offset(self, camera):
        pass

    def get_bottom_bb(self):
        pass

    def get_bottom_bb_offset(self, camera):
        pass

    def get_left_bb(self):
        pass

    def get_left_bb_offset(self, camera):
        pass

    def get_right_bb(self):
        pass

    def get_right_bb_offset(self, camera):
        pass

    def handle_collision(self, group, other, hit_position):
        pass
