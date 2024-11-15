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
    def __init__(self, owner):
        self.owner = owner
        self.event_queue = []
        self.current_state = None
        self.transitions = {}

    def start(self, state):
        self.current_state = state
        print(f'Enter into {state.__name__}')
        self.current_state.enter(self.owner, ('START', 0))

    def add_event(self, event):
        self.event_queue.append(event)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        if self.current_state:
            self.current_state.do(self.owner)
        if self.event_queue:
            event = self.event_queue.pop(0)
            self.handle_event(event)

    def draw(self):
        if self.current_state:
            self.current_state.draw(self.owner)

    def handle_event(self, event):
        for trigger_event, next_state in self.transitions.get(self.current_state, {}).items():
            if trigger_event(event):
                if next_state != self.current_state:
                    print(f'Exit from {self.current_state.__name__}')
                    self.current_state.exit(self.owner, event)
                    self.current_state = next_state
                    print(f'Enter into {self.current_state.__name__}')
                    self.current_state.enter(self.owner, event)
                else:
                    if hasattr(self.current_state, 'handle_event'):
                        self.current_state.handle_event(self.owner, event)
                return

    def set_state(self, new_state):
        if new_state != self.current_state:
            if self.current_state:
                print(f'Exit from {self.current_state.__name__}')
                self.current_state.exit(self.owner, None)
            self.current_state = new_state
            print(f'Enter into {self.current_state.__name__}')
            self.current_state.enter(self.owner, None)
