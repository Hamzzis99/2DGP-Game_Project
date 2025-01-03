# utils/font.py

import pico2d

class Spritesheet:
    def __init__(self, filename):
        try:
            self.sheet = pico2d.load_image(filename)
        except Exception as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise e

    def image_at(self, x, y, scalingfactor, xTileSize=8, yTileSize=8):
        # flip을 빈 문자열로 설정 (수평/수직 반전 없음)
        flip = ''  # 반전하지 않도록 빈 문자열로 설정
        self.sheet.clip_composite_draw(x, y, xTileSize, yTileSize, 0, 0, xTileSize * scalingfactor, yTileSize * scalingfactor, flip)

class Font:
    def __init__(self, filePath, char_width=8, char_height=8):
        self.spritesheet = Spritesheet(filePath)  # Spritesheet 로드
        self.char_width = char_width
        self.char_height = char_height
        self.chars = (
            " !\"#$%&'()*+,-./"
            "0123456789:;<=>?"
            " ABCDEFGHIJKLMNO"
            "PQRSTUVWXYZ[\\]^_"
            "`abcdefghijklmno"
            "pqrstuvwxyz{|}~"
        )
        self.char_positions = self.calculate_positions()

    def calculate_positions(self):
        positions = {}
        index = 0

        for row in range(6):  # 총 6행
            for col in range(16):  # 각 행에 16문자
                if index < len(self.chars):
                    char = self.chars[index]
                    x = col * self.char_width
                    y = (5 - row) * self.char_height  # y는 위에서 아래로 계산
                    positions[char] = (x, y, x + self.char_width, y + self.char_height)
                    index += 1
        return positions

    def draw(self, text, x, y, camera=None, scaling_factor=2):
        # HUD 요소일 경우 카메라 오프셋을 적용하지 않음
        if camera:
            screen_x = x - camera.camera_x
            screen_y = y - camera.camera_y
        else:
            screen_x = x
            screen_y = y

        for char in text:
            if char in self.char_positions:
                x1, y1, x2, y2 = self.char_positions[char]
                width = x2 - x1
                height = y2 - y1
                # 스프라이트 크기를 scaling_factor를 사용하여 확대
                self.spritesheet.sheet.clip_composite_draw(
                    x1, y1, width, height,  # 원본 좌표와 크기
                    0, '',  # 회전 각도와 반전 설정 (여기서 flip 인자는 빈 문자열로 설정됨)
                    screen_x, screen_y,  # 출력 위치
                    width * scaling_factor, height * scaling_factor  # 가로 및 세로 크기 조정 비율
                )
                # 문자 간격 조정
                screen_x += (self.char_width * scaling_factor)  # 문자 간격을 조정하여 글자가 더 잘 맞도록 설정


