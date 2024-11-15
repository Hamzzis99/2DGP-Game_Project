# mario.py
from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_s
import game_framework
from state_machine import StateMachine, right_down, left_down, left_up, right_up, s_down
from states import Idle, Run, Jump

class Mario:
    def __init__(self):
        self.x, self.y = 400, 90  # 초기 위치 설정
        self.face_dir = 1
        self.dir = 0  # 이동 방향: -1 (왼쪽), 0 (정지), 1 (오른쪽)
        self.image = load_image('character.png')  # 캐릭터 이미지 로드
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {
                right_down: Run,
                left_down: Run,
                left_up: Run,
                right_up: Run,
                s_down: Jump
            },
            Run: {
                right_down: Idle,
                left_down: Idle,
                right_up: Idle,
                left_up: Idle,
                s_down: Jump
            },
            Jump: {
                right_down: Jump,  # Jump 상태에서 방향키 입력 시 Jump 상태로 유지
                left_down: Jump,
                right_up: Jump,
                left_up: Jump
            }
        })
        self.pressed_keys = set()  # 현재 눌려 있는 키 추적
        self.frame = 0  # 현재 애니메이션 프레임
        self.game_framework = game_framework  # 상태 클래스에서 frame_time 접근을 위해 할당

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 키 상태 추적
        if event.type == SDL_KEYDOWN:
            if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_s):
                self.pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_s):
                self.pressed_keys.discard(event.key)
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y + 30, self.x + 25, self.y - 30

    def handle_collision(self, group, other):
        pass
