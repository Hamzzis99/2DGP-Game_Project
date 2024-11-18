import pico2d
import game_framework
from pico2d import load_wav
from font import Font

def main():
    pico2d.open_canvas(800, 600)  # 캔버스를 800x600 사이즈로 열기

    # 검은색 배경 이미지 로드 (black.jpg 사용)
    background = pico2d.load_image('img/black.jpg')  # 이미지 경로가 올바른지 확인하세요
    background.draw(400, 300)  # 800x600 화면 중심에 그리기

    # Font 객체 생성 (파일 이름은 필요에 따라 조정)
    font = Font('img/font.png', char_width=8, char_height=8)

    # "GAME OVER" 텍스트를 중앙에 표시하기
    screen_width = pico2d.get_canvas_width()
    screen_height = pico2d.get_canvas_height()
    text = "GAME OVER"
    scaling_factor = 3  # 크기를 키우기 위해 확대 배율 설정
    text_width = len(text) * font.char_width * scaling_factor
    x_position = (screen_width - text_width) // 2  # 중앙 정렬을 위한 x 좌표 계산
    y_position = screen_height // 2  # y 좌표는 화면 중앙

    font.draw(text, x_position, y_position, scaling_factor=scaling_factor)

    # 아래에 텍스트 추가 (살짝 오른쪽으로 이동)
    sub_text = "2DGP-PROJECT K.G.H"
    sub_text_width = len(sub_text) * font.char_width * scaling_factor
    sub_x_position = (screen_width - sub_text_width) // 2  # 약간 오른쪽으로 이동 (+20)
    sub_y_position = y_position - (font.char_height * scaling_factor * 2)  # "GAME OVER" 아래에 위치하도록 설정
    font.draw(sub_text, sub_x_position, sub_y_position, scaling_factor=scaling_factor)

    pico2d.update_canvas()  # 캔버스 업데이트 (화면에 출력)

    # Game over 사운드 재생
    game_over_sound = load_wav('resources/game_over-yoshi-island2.mp3')  # 사운드 파일 로드
    game_over_sound.set_volume(22)
    game_over_sound.play()

    pico2d.delay(10)  # 10초 동안 유지
    pico2d.close_canvas()  # 캔버스 닫기

if __name__ == "__main__":
    main()
