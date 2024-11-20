# state_machine.py

from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_s
from utils.camera import Camera  # Camera 클래스 임포트
import game_framework

# 이벤트 헬퍼 함수들
def start_event(e):
    return e[0] == 'START'

def right_down(e):
    return isinstance(e, tuple) and e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return isinstance(e, tuple) and e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return isinstance(e, tuple) and e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return isinstance(e, tuple) and e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def s_down(e):
    return isinstance(e, tuple) and e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def s_up(e):
    return isinstance(e, tuple) and e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s

class StateMachine:
    def __init__(self, o):
        self.o = o
        self.event_que = []
        self.cur_state = None
        self.transitions = {}

    def start(self, state):
        self.cur_state = state
        print(f'Enter into {state.__name__}')
        self.cur_state.enter(self.o, ('START', 0))

    def add_event(self, e):
        self.event_que.append(e)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        self.cur_state.do(self.o)
        while self.event_que:
            event = self.event_que.pop(0)
            self.handle_event(event)

    def draw(self):
        self.cur_state.draw(self.o)

    def draw_with_camera(self, camera):
        self.cur_state.draw_with_camera(self.o, camera)

    def handle_event(self, e):
        for event, next_state in self.transitions.get(self.cur_state, {}).items():
            if event(e):
                if next_state != self.cur_state:
                    self.cur_state.exit(self.o, e)
                    self.cur_state = next_state
                    self.cur_state.enter(self.o, e)
                else:
                    # 같은 상태로의 전환인 경우, 현재 상태의 handle_event 호출
                    if hasattr(self.cur_state, 'handle_event'):
                        self.cur_state.handle_event(self.o, e)
                return

    def set_state(self, new_state):
        if new_state != self.cur_state:
            self.cur_state.exit(self.o, None)
            self.cur_state = new_state
            self.cur_state.enter(self.o, None)

class Dead:
    def __init__(self):
        self.animation_duration = 0.5  # 올라가는 시간 (초)
        self.fall_speed = 350  # 내려가는 속도 (픽셀/초)
        self.elapsed_time = 0.0
        self.rising = True
        self.sound_played = False  # 사운드 재생 여부 플래그 추가

    def enter(self, mario, e):
        mario.dir = 0
        mario.velocity_y = 0
        mario.frame = 0  # 프레임 강제 초기화
        self.elapsed_time = 0.0
        self.rising = True
        self.sound_played = False  # 초기화
        print("Dead 상태: 진입 - 사망 애니메이션 시작")  # 디버깅용

    def exit(self, mario, e):
        print("Dead 상태: 종료")  # 디버깅용

    def do(self, mario):
        frame_time = game_framework.frame_time

        # 사운드 재생 (한 번만 재생)
        if not self.sound_played:
            mario.dead_sound.play()
            self.sound_played = True

        if self.rising:
            # y를 올라가게 함
            rise_amount = 50 * (frame_time / self.animation_duration)
            mario.y += rise_amount
            self.elapsed_time += frame_time
            if self.elapsed_time >= self.animation_duration:
                self.rising = False
                self.elapsed_time = 0.0
        else:
            # y를 떨어지게 함
            mario.y -= self.fall_speed * frame_time
            # y 좌표를 0으로 고정하지 않고 계속 떨어지도록 합니다.
            # 게임 오버는 play_mode.py에서 처리

    def draw(self, mario):
        print("Dead 상태에서 draw 호출")  # 디버깅용
        frame_width = 16
        frame_height = 16
        frame_x = 12  # Dead 상태의 스프라이트 x 좌표 (스프라이트 시트에 맞게 조정)
        frame_y = 342  # Dead 상태의 스프라이트 y 좌표 (스프라이트 시트에 맞게 조정)
        mario.image.clip_draw(
            frame_x, frame_y, frame_width, frame_height,
            mario.x, mario.y,
            frame_width * 3, frame_height * 3  # 스케일 적용
        )

    def draw_with_camera(self, mario, camera: Camera):
        print("Dead 상태에서 draw_with_camera 호출")  # 디버깅용
        frame_width = 16
        frame_height = 16
        frame_x = 12  # Dead 상태의 스프라이트 x 좌표 (스프라이트 시트에 맞게 조정)
        frame_y = 342  # Dead 상태의 스프라이트 y 좌표 (스프라이트 시트에 맞게 조정)
        screen_x, screen_y = camera.apply(mario.x, mario.y)
        mario.image.clip_draw(
            frame_x, frame_y, frame_width, frame_height,
            screen_x, screen_y,
            frame_width * 3, frame_height * 3  # 스케일 적용
        )
