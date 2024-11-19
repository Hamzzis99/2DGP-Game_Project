from pico2d import get_time, load_image, clear_canvas, update_canvas, get_events, SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, \
    load_wav
import game_framework
import play_mode  # play_mode로 전환하기 위해 import

def init():
    global image, running, logo_start_time
    image = load_image('img/tuk_credit.png')
    sound = load_wav('resources/game_over-yoshi-island2.mp3')
    sound.set_volume(20)  # 필요 시 볼륨 조정
    sound.play()  # 사운드 재생
    running = True
    logo_start_time = get_time()

def finish():
    global image
    del image

def update():
    global logo_start_time
    if get_time() - logo_start_time >= 5.0:  # 5초 후에 play_mode로 전환
        game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    image.draw(400, 300)  # 이미지를 (400, 300)에 그리기
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:  # ESC 키를 누르면 게임 종료
                game_framework.quit()
