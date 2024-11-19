# state_machine.py

from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_s

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
                    #print(f'Exit from {self.cur_state.__name__}')
                    self.cur_state.exit(self.o, e)
                    self.cur_state = next_state
                    #print(f'Enter into {self.cur_state.__name__}')
                    self.cur_state.enter(self.o, e)
                else:
                    # 같은 상태로의 전환인 경우, 현재 상태의 handle_event 호출
                    if hasattr(self.cur_state, 'handle_event'):
                        self.cur_state.handle_event(self.o, e)
                return

    def set_state(self, new_state):
        if new_state != self.cur_state:
            #print(f'Exit from {self.cur_state.__name__}')
            self.cur_state.exit(self.o, None)
            self.cur_state = new_state
            #print(f'Enter into {self.cur_state.__name__}')
            self.cur_state.enter(self.o, None)
