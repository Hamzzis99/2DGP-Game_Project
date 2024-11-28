# utils/config.py

class MarioConfig:
    WORLD_WIDTH = 4800
    WORLD_HEIGHT = 600
    START_X = 100
    START_Y = 100
    # 기타 설정 변수들...

    # 게임 시간 제한 (초 단위)
    GAME_TIME_LIMIT = 100  # 기본값: 300초 (5분)

    # 배경음악 설정
    GAME_MUSIC_VOLUME = 64  # 볼륨 조절 (0-128)


class TurtleConfig:
    TURTLE_TRANSFORM_INTERVAL = 10.0  # seconds (50초마다 변신)
    TURTLE_TRANSFORM_DURATION = 5.0    # seconds (5초간 변신 상태)