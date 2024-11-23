# game_over.py

import game_framework
from pico2d import load_image, load_wav, clear_canvas, update_canvas, get_events, get_time, get_canvas_width, get_canvas_height, SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE
import logo_mode
from states import reset_game
from utils.font import Font

def init():
    global font, sound, background, running, logo_start_time
    font = Font('img/font.png', char_width=8, char_height=8)
    sound = load_wav('resources/game_over-yoshi-island2.mp3')  # 사운드 파일 로드
    sound.set_volume(32)  # 필요 시 볼륨 조정
    sound.play()  # 사운드 재생
    background = load_image('img/black.jpg')  # 검은 배경 이미지 로드

    running = True
    logo_start_time = get_time()
    reset_game()  # 게임 상태 초기화 (lives=3, score=0)

def finish():
    global font, sound, background
    del font
    del sound
    del background

def update():
    global logo_start_time
    if get_time() - logo_start_time >= 1.0:  # 원래는 10초였음
        game_framework.change_mode(logo_mode)

def draw():
    clear_canvas()
    background.draw(400, 300)  # 검은 배경을 (400, 300)에 그리기

    # "GAME OVER" 텍스트를 중앙에 표시하기
    screen_width = get_canvas_width()
    screen_height = get_canvas_height()
    text = "GAME OVER"
    scaling_factor = 3  # 크기를 키우기 위해 확대 배율 설정
    text_width = len(text) * font.char_width * scaling_factor
    x_position = (screen_width - text_width) // 2  # 중앙 정렬을 위한 x 좌표 계산
    y_position = screen_height // 2  # y 좌표는 화면 중앙

    font.draw(text, x_position, y_position, scaling_factor=scaling_factor)

    # 아래에 텍스트 추가 (살짝 오른쪽으로 이동)
    sub_text = "2DGP-PROJECT T_T"
    sub_text_width = len(sub_text) * font.char_width * scaling_factor
    sub_x_position = (screen_width - sub_text_width) // 2
    sub_y_position = y_position - (font.char_height * scaling_factor * 2)  # "GAME OVER" 아래에 위치하도록 설정
    font.draw(sub_text, sub_x_position, sub_y_position, scaling_factor=scaling_factor)

    update_canvas()  # 캔버스 업데이트 (화면에 출력)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:  # ESC 키를 누르면 게임 종료
                game_framework.quit()
