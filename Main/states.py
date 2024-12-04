# states.py

class GameState:
    def __init__(self):
        self.lives = 3  # Mario의 시작 목숨 개수
        self.score = 0  # Mario의 점수
        self.game_time = 300.0  # 게임 시간 (초) - 예: 3분으로 설정

    def reset(self):
        self.score = 0
        self.game_time = 300.0  # 게임 시간 초기화 (예: 3분)

    def game_over_reset(self):
        self.lives = 3  # Mario의 시작 목숨 개수 초기화
        self.score = 0  # Mario의 점수 초기화
        self.game_time = 300.0  # 게임 시간 초기화 (예: 3분)
        #print("GameState has been completely reset for Game Over. Lives: {}, Score: {}, Game Time: {}".format(
            #self.lives, self.score, self.game_time))

# 전역 GameState 인스턴스 생성
game_state = GameState()

def reset_game():
    game_state.reset()
    #print("GameState has been reset. Lives: {}, Score: {}, Game Time: {}".format(
        #game_state.lives, game_state.score, game_state.game_time))

def game_over_reset():
    game_state.game_over_reset()

debug_mode = False  # 디버그 모드 초기값은 False로 설정