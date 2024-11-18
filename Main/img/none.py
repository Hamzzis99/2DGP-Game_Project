#none.py 미사용 파일 오로지 마리오 좌표값 구하는데만 사용하는중

from pico2d import *

open_canvas()

# 스프라이트 시트 로드
sprite_sheet = load_image('gun_mario.png')

# 초기 스프라이트 좌표와 크기 설정
#sprite_x, sprite_y = 0 ,224  # 스프라이트의 시작 좌표
#sprite_x, sprite_y = 0 ,208  # 스프라이트의 시작 좌표
sprite_x, sprite_y = 68 ,476  # 스프라이트의 시작 좌표 거북이 좌표 : 1(293, 169), 2(312, 169)
                                #쓰러진 거북이 패턴 -> 1(160,169), 2(141,169)

                                #Gun_mario IDLE : 26, 276
                                #Gun_mario Move1 68, 476

                                #Gun_mario1 Move1 100, 476
                                #Gun_mario Move2 125, 476
                                #Gun_mario Move 146, 476

                                #Gun_Mario Jump 173,476
                                #width = 20, hieght = 20

#점프 시작? 336
#점프 좌표 355

sprite_width, sprite_height = 20, 20  # 기존 크기
scale_factor = 10  # 크기를 키우는 배율

# 캐릭터의 고정된 화면 좌표
character_x, character_y = 400, 350

def draw():
    clear_canvas()
    # sprite_width와 sprite_height에 배율을 곱해 크기를 조정
    sprite_sheet.clip_draw(sprite_x, sprite_y, sprite_width, sprite_height, character_x, character_y, sprite_width * scale_factor, sprite_height * scale_factor)
    update_canvas()

while True:
    draw()
    delay(0.01)

close_canvas()
