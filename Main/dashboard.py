# dashboard.py

import pico2d
from font import Font  # font.py에 포함된 Font 클래스 임포트

class Dashboard:
    def __init__(self):
        self.font = Font("font.png", char_width=8, char_height=8)  # Font 객체 생성 (font.png 파일 사용)
        self.state = "menu"
        self.levelName = "WORLD 1-1"
        self.points = 0
        self.coins = 0
        self.ticks = 0
        self.time = 0

    def update(self):
        # 시간 업데이트
        self.ticks += 1
        if self.ticks == 60:
            self.ticks = 0
            self.time += 1

    def draw(self, camera):
        # 화면에 텍스트를 그리는 코드
        self.font.draw("MARIO", 50, 550, camera)
        self.font.draw(self.pointString(), 50, 530, camera)
        self.font.draw("@x{}".format(self.coinString()), 225, 530, camera)
        self.font.draw("WORLD", 380, 550, camera)
        self.font.draw(str(self.levelName), 395, 530, camera)
        self.font.draw("TIME", 520, 550, camera)
        if self.state != "menu":
            self.font.draw(self.timeString(), 535, 530, camera)

    def coinString(self):
        return "{:02d}".format(self.coins)

    def pointString(self):
        return "{:06d}".format(self.points)

    def timeString(self):
        return "{:03d}".format(self.time)
