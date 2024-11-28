# title_mode.py

import game_framework
from pico2d import load_image, clear_canvas, update_canvas, get_events, get_time, get_canvas_width, get_canvas_height, \
    SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, draw_rectangle

from game_object import GameObject
from utils.bgm import BGMManager
from utils.font import Font
from mario import Mario
import game_world
import play_mode

class Grass(GameObject):
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.image = None

    def load_images(self):
        pass

    def update(self):
        pass

    def draw_with_camera(self, camera=None):
        if self.image:
            self.image.draw(self.x, self.y, self.width, self.height)
        else:
            draw_rectangle(
                self.x - self.width / 2, self.y - self.height / 2,
                self.x + self.width / 2, self.y + self.height / 2
            )

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2

font = None
background = None
title_overlay_image = None
control_image = None
bgm_manager = None
start_time = 0
mario = None
grass = None
press_space_font = None
show_control = False

def init():
    global background, title_overlay_image, control_image, bgm_manager, start_time, mario, grass, font, press_space_font, show_control

    try:
        background = load_image('map/title.png')
    except Exception as e:
        background = None

    try:
        title_overlay_image = load_image('map/mariotitle.png')
    except Exception as e:
        title_overlay_image = None

    try:
        control_image = load_image('map/control.png')
    except Exception as e:
        control_image = None

    start_time = get_time()

    bgm_manager = BGMManager()
    bgm_manager.load_music('title_theme', 'resources/title_theme.ogg')
    bgm_manager.play('title_theme', volume=32)

    mario = Mario(None)
    mario.x = get_canvas_width() // 2
    mario.y = 40
    mario.scale = 2
    game_world.add_object(mario, 1)

    grass_width = get_canvas_width()
    grass_height = 30
    grass_x = get_canvas_width() // 2
    grass_y = 15
    grass = Grass(grass_x, grass_y, grass_width, grass_height)
    grass.load_images()
    game_world.add_object(grass, 1)

    game_world.add_collision_pair('mario:grass', mario, grass)

    try:
        font = Font('img/font.png', char_width=8, char_height=8)
        press_space_font = Font('img/font.png', char_width=8, char_height=8)
    except Exception as e:
        font = None
        press_space_font = None

    show_control = False

def finish():
    global background, title_overlay_image, control_image, bgm_manager, mario, grass, font, press_space_font, show_control
    del background
    del title_overlay_image
    del control_image
    del font
    del press_space_font
    show_control = False
    if bgm_manager:
        bgm_manager.stop()
    game_world.remove_object(mario)
    game_world.remove_object(grass)

def update():
    global show_control
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    screen_width, screen_height = get_canvas_width(), get_canvas_height()

    if background:
        background.draw(screen_width // 2, screen_height // 2)

    if title_overlay_image:
        scaling_factor = 0.7
        original_width, original_height = 617, 306
        scaled_width = original_width * scaling_factor
        scaled_height = original_height * scaling_factor
        y_delta = 20
        new_y_position = screen_height - (scaled_height / 2) - y_delta
        title_overlay_image.draw(screen_width // 2, new_y_position, scaled_width, scaled_height)

    if show_control and control_image:
        scaling_factor = 0.5
        original_width, original_height = 1503, 838
        scaled_width = original_width * scaling_factor
        scaled_height = original_height * scaling_factor
        y_offset = 10
        control_image.draw(screen_width // 2, screen_height // 2 + y_offset, scaled_width, scaled_height)

    game_world.render()

    if press_space_font:
        text = "PRESS SPACE TO START"
        scaling_factor = 2
        text_width = len(text) * press_space_font.char_width * scaling_factor
        x_position = (screen_width - text_width) // 2
        y_position = 50
        press_space_font.draw(text, x_position, y_position, scaling_factor=scaling_factor)

    update_canvas()

def handle_events():
    global show_control
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_SPACE:
                if not show_control:
                    show_control = True
                else:
                    game_framework.change_mode(play_mode)
    for event in events:
        mario.handle_event(event)

def pause():
    pass

def resume():
    pass
