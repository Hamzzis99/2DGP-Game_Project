import pico2d

class Font:
    def __init__(self, font_image, char_width=8, char_height=8):
        self.font_image = pico2d.load_image(font_image)
        self.char_width = char_width
        self.char_height = char_height
        self.char_positions = self.calculate_positions()

    def calculate_positions(self):
        # 정확한 문자 순서 (수정된 chars 배열)
        chars = (
            " !\"#$%&'()*+,-./"
            "0123456789:;<=>?"
            "ABCDEFGHIJKLMNO"
            "PQRSTUVWXYZ[\\]^_"
            "`abcdefghijklmno"
            "pqrstuvwxyz{|}~"
        )
        positions = {}
        index = 0

        for row in range(6):  # 총 6행
            for col in range(16):  # 각 행에 16문자
                if index < len(chars):
                    char = chars[index]
                    x = col * self.char_width
                    y = (5 - row) * self.char_height  # y는 위에서 아래로 계산
                    positions[char] = (x, y, x + self.char_width, y + self.char_height)
                    print(f"Mapping '{char}' to: x={x}, y={y}, width={self.char_width}, height={self.char_height}")
                    index += 1
        return positions

    def draw(self, text, x, y):
        for char in text:
            if char in self.char_positions:
                x1, y1, x2, y2 = self.char_positions[char]
                self.font_image.clip_draw(x1, y1, x2 - x1, y2 - y1, x, y)
                x += self.char_width
            else:
                print(f"Character '{char}' is not supported and will be ignored.")

# 테스트 코드
def test_font():
    pico2d.open_canvas(400, 200)
    font = Font('font.png', char_width=8, char_height=8)

    # 문자열 출력 테스트
    font.draw("HELLO WORLD!", 20, 150)
    font.draw("ABCDEFGHIJKLMNO", 20, 130)  # 수정된 순서 반영
    font.draw("0123456789:;<=>?", 20, 110)

    pico2d.update_canvas()
    pico2d.delay(5)
    pico2d.close_canvas()

test_font()