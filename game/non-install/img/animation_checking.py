# character_runs.py 사용하지 않는 것. 캐릭터 좌표 노가다 전용 파일
from pico2d import *



def main():
    # 캔버스 열기 (기본 크기 800x600)
    open_canvas()

    # 이미지 로드
    grass = load_image('grass.png')
    character = load_image('gun_mario.png')
    # 스프라이트의 시작 좌표 거북이 좌표 : 1(293, 169), 2(312, 169)
    # 애니메이션 프레임 쓰러진 거북이 설정1(160,169), 2(141,169)
    frame_x_positions = [100, 125, 146]
    frame_y_position = 476
    frame_width = 20  # 소스 이미지의 프레임 너비 (고정)
    frame_height = 20  # 소스 이미지의 프레임 높이 (고정)

    # Gun_mario IDLE : 26, 276
    # Gun_mario Move1 68, 476 <- 이건뺀다.

    # Gun_mario1 Move1 100, 476
    # Gun_mario Move2 125, 476
    # Gun_mario Move3 146, 476

    # Gun_Mario Jump 173,476
    # width = 20, hieght = 20

    # 캐릭터의 크기 두 배로 설정
    scale = 4
    display_width = frame_width * scale
    display_height = frame_height * scale

    # 프레임 인덱스 초기화
    frame = 0

    # 캐릭터의 초기 x 좌표
    x = 0

    # 애니메이션 및 이동 루프
    while x <= 800:
        clear_canvas()
        grass.draw(400, 30)  # 배경 그리기

        # 현재 프레임의 소스 x 좌표
        sx = frame_x_positions[frame]

        # 캐릭터 그리기 (크기 두 배로)
        # clip_draw(sx, sy, sw, sh, dx, dy, w, h)
        character.clip_draw(sx, frame_y_position, frame_width, frame_height, x, 90, display_width, display_height)

        update_canvas()

        # 프레임 업데이트 (0, 1, 2 반복)
        frame = (frame + 1) % 2

        # 캐릭터 이동
        x += 10  # 이동 속도 조절 (10 픽셀씩 이동)

        delay(0.1)  # 애니메이션 속도 조절

    # 캔버스 닫기
    close_canvas()


if __name__ == '__main__':
    main()
