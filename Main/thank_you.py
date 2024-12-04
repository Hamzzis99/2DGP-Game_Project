# thank_you.py

import game_framework
from pico2d import (
    load_image, load_wav, clear_canvas, update_canvas,
    get_events, get_time, get_canvas_width, get_canvas_height,
    SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE
)
import logo_mode
import title_mode
from states import game_over_reset  # 변경: reset_game 대신 game_over_reset 임포트
from utils.font import Font

def init():
    global font, sound, background, credit_image, logo_start_time, credit_show_time
    font = Font('img/font.png', char_width=8, char_height=8)
    sound = load_wav('resources/super-mario-bros_win.mp3')
    sound.set_volume(32)  # 필요 시 볼륨 조정
    sound.play()  # 사운드 재생
    background = load_image('img/black.jpg')  # 검은 배경 이미지 로드
    credit_image = load_image('img/tuk_credit.png')  # 크레딧 이미지 로드

    logo_start_time = get_time()  # "Thank You" 화면 시작 시간 기록
    credit_show_time = None  # 크레딧 화면이 표시될 시간을 추적
    game_over_reset()  # 게임 상태 완전 초기화

def finish():
    global font, sound, background, credit_image
    del font
    del sound
    del background
    del credit_image

def update():
    global logo_start_time, credit_show_time
    current_time = get_time()
    elapsed_time = current_time - logo_start_time

    if elapsed_time >= 3.8 and credit_show_time is None:
        credit_show_time = current_time  # 크레딧 화면 표시 시작 시간 기록

    if credit_show_time and (current_time - credit_show_time) >= 3.0:
        game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    current_time = get_time()
    elapsed_time = current_time - logo_start_time

    if elapsed_time < 3.8:
        # "Thank You" 텍스트와 배경 그리기
        background.draw(400, 300)  # 검은 배경을 (400, 300)에 그리기

        # "Thank You" 텍스트를 중앙에 표시하기
        screen_width = get_canvas_width()
        screen_height = get_canvas_height()
        text = "Thank You"
        scaling_factor = 3  # 크기를 키우기 위해 확대 배율 설정
        text_width = len(text) * font.char_width * scaling_factor
        x_position = (screen_width - text_width) // 2  # 중앙 정렬을 위한 x 좌표 계산
        y_position = screen_height // 2  # y 좌표는 화면 중앙

        font.draw(text, x_position, y_position, scaling_factor=scaling_factor)

        # 아래에 텍스트 추가 (살짝 아래로 이동)
        sub_text = "2DGP-PROJECT"
        sub_text_width = len(sub_text) * font.char_width * scaling_factor
        sub_x_position = (screen_width - sub_text_width) // 2
        sub_y_position = y_position - (font.char_height * scaling_factor * 2)  # "Thank You" 아래에 위치
        font.draw(sub_text, sub_x_position, sub_y_position, scaling_factor=scaling_factor)

    elif 3.8 <= elapsed_time < 8.0:
        # 크레딧 이미지 표시
        credit_image.draw(400, 300)  # img/tuk_credit.png 이미지를 화면 중앙에 출력

    update_canvas()  # 캔버스 업데이트 (화면에 출력)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:  # ESC 키를 누르면 게임 종료
                game_framework.quit()
