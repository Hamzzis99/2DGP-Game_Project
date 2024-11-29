# world_start_mode.py

import game_framework
from pico2d import load_image, clear_canvas, update_canvas, get_events, SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, get_canvas_width, get_canvas_height, get_time
from utils.font import Font
from utils.dashboard import Dashboard
import play_mode  # play_mode로 전환하기 위해 추가
from states import game_state  # game_state 임포트 추가

# 전역 변수 선언
font = None
background = None
mario_sprite = None
dashboard = None
start_time = None  # 시작 시간을 추적하기 위한 변수


def init():
    """초기화 함수"""
    global font, background, mario_sprite, dashboard, start_time

    # 검은 배경과 폰트, 대시보드 로드
    font = Font('img/font.png', char_width=8, char_height=8)
    background = load_image('img/black.jpg')
    mario_sprite = load_image('img/character.png')
    dashboard = Dashboard()  # Dashboard 인스턴스 생성

    start_time = get_time()  # 초기화 시 현재 시간을 기록


def finish():
    global font, background, mario_sprite, dashboard
    del font
    del background
    del mario_sprite
    del dashboard


def draw():
    clear_canvas()

    # 검은 배경 그리기
    background.draw(get_canvas_width() // 2, get_canvas_height() // 2)

    # HUD 그리기
    dashboard.draw(None)

    # "WORLD 1-1" 텍스트 중앙에 표시
    screen_width = get_canvas_width()
    screen_height = get_canvas_height()
    text = "WORLD 1-1"
    scaling_factor = 2
    text_width = len(text) * font.char_width * scaling_factor
    x_position = (screen_width - text_width) // 2
    y_position = screen_height // 2 + 50
    font.draw(text, x_position, y_position, scaling_factor=scaling_factor)

    # 마리오와 "x {lives}" 표시
    mario_x, mario_y = screen_width // 2 - 30, screen_height // 2 - 20
    mario_sprite.clip_draw(276, 342, 16, 16, mario_x, mario_y, 32, 32)  # 마리오 스프라이트 표시
    life_text = f"x {game_state.lives}"  # 동적으로 목숨 수 가져오기
    life_x_position = mario_x + 40
    life_y_position = mario_y
    font.draw(life_text, life_x_position, life_y_position, scaling_factor=scaling_factor)

    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()


def update():
    dashboard.update()  # Dashboard 업데이트

    # 일정 시간이 지나면 play_mode로 전환
    current_time = get_time()
    if current_time - start_time >= 1.0:  # 1초 후에 play_mode로 전환 (원하는 시간으로 수정 가능)
        game_framework.change_mode(play_mode)


def pause():
    pass


def resume():
    pass
