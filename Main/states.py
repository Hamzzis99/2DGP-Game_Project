# states.py

class GameState:
    def __init__(self):
        self.lives = 3  # Mario의 시작 목숨 개수
        self.score = 0  # Mario의 점수

    def reset(self):
        self.lives = 3
        self.score = 0

game_state = GameState()

def reset_game():
    """게임 상태를 초기화합니다."""
    game_state.reset()
    print("GameState has been reset. Lives: {}, Score: {}".format(game_state.lives, game_state.score))
