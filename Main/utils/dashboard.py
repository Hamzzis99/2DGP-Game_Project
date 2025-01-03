# utils/dashboard.py

from pico2d import *
from utils.font import Font  # font.py에 포함된 Font 클래스 임포트
from states import game_state  # game_state 임포트

class Dashboard:
    def __init__(self):
        self.font = Font("img/font.png", char_width=8, char_height=8)  # Font 객체 생성 (font.png 파일 사용)
        self.state = "menu"
        self.levelName = "1-1"
        self.ticks = 0
        self.time = 0

    def update(self):
        # 현재 구현에서는 별도의 업데이트 로직이 필요 없으므로 pass
        pass

    def draw(self, camera):
        scaling_factor = 2  # 글자 크기를 키우고 싶다면 이 값을 변경 (예: 3배로 확대)
        self.font.draw("MARIO", 60, 550, None, scaling_factor)  # HUD는 카메라 없이 그리기
        self.font.draw(self.pointString(), 50, 530, None, scaling_factor)  # 점수 표시 위치 조정
        self.font.draw("LIFE", 220, 550, None, scaling_factor)
        self.font.draw("x{}".format(self.mariolife()), 225, 530, None, scaling_factor)
        self.font.draw("WORLD", 380, 550, None, scaling_factor)
        self.font.draw(str(self.levelName), 395, 530, None, scaling_factor)
        self.font.draw("TIME", 710, 550, None, scaling_factor)
        self.font.draw(self.timeString(), 720, 530, None, scaling_factor)

    def set_time(self, time):
        self.time = time

    def mariolife(self):
        return "{:02d}".format(game_state.lives)  # game_state.lives 참조

    def pointString(self):
        return "{:06d}".format(game_state.score)  # game_state.score 참조

    def timeString(self):
        return "{:03d}".format(self.time)

    def increment_score(self, amount):
        game_state.score += amount  # game_state.score 증가
        print(f"Score increased by {amount}. Total Score: {game_state.score}")  # 디버깅 출력

    def decrement_life(self, amount=1):
        game_state.lives = max(game_state.lives - amount, 0)  # game_state.lives 감소
        print(f"Lives decreased by {amount}. Total Lives: {game_state.lives}")  # 디버깅 출력
