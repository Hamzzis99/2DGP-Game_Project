# dashboard.py

import pico2d
from font import Font  # font.py에 포함된 Font 클래스 임포트

class Dashboard:
    def __init__(self):
        self.font = Font("font.png", char_width=8, char_height=8)  # Font 객체 생성 (font.png 파일 사용)
        self.state = "menu"
        self.levelName = "1-1"
        self.points = 0
        self.coins = 0
        self.ticks = 0
        self.time = 0

    def update(self):
        # 현재 구현에서는 별도의 업데이트 로직이 필요 없으므로 pass
        pass

    def draw(self, camera):
        print(f"Dashboard.draw(): Time={self.time}, Points={self.points}, Coins={self.coins}")
        # 화면에 텍스트를 그리는 코드
        self.font.draw("MARIO", 50, 550, None)  # HUD는 camera 없이 그리기
        self.font.draw(self.pointString(), 50, 530, None)
        self.font.draw("@x{}".format(self.coinString()), 225, 530, None)
        self.font.draw("WORLD", 380, 550, None)
        self.font.draw(str(self.levelName), 395, 530, None)
        self.font.draw("TIME", 520, 550, None)
        self.font.draw(self.timeString(), 535, 530, None)

    def set_time(self, time):
        self.time = time

    def coinString(self):
        return "{:02d}".format(self.coins)

    def pointString(self):
        return "{:06d}".format(self.points)

    def timeString(self):
        return "{:03d}".format(self.time)
