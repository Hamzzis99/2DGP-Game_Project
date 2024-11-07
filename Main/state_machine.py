# 이벤트 체크 함수를 정의
# 상태 이벤트 e = (종류, 실제값) 튜플로 정의
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT


def start_event(e):
    return e[0] == 'START'


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


class StateMachine:
    def __init__(self, obj):
        self.obj = obj  # 어떤 객체를 위한 상태 머신인지 알려줌
        # 상태 이벤트를 보관할 리스트
        self.event_q = []

    def start(self, state):
        self.cur_state = state  # 시작 상태를 받아서 현재 상태로 설정
        self.cur_state.enter(self.obj, ('START', 0))
        print(f'Enter into {state}')

    def update(self):
        self.cur_state.do(self.obj)  # 현재 상태의 do() 함수 실행
        # 이벤트가 있는지 확인
        if self.event_q:
            e = self.event_q.pop(0)
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    print(f'Exit From {self.cur_state}')
                    self.cur_state.exit(self.obj, e)
                    self.cur_state = next_state
                    print(f'Enter into {next_state}')
                    self.cur_state.enter(self.obj, e)  # 상태 변환의 이유를 명확히 알려줌
                    return  # 이벤트에 따른 상태 변환 완료
            # 이 시점으로 왔다는 것은 이벤트에 따른 전환 실패
            print(f'        WARNING: {e} not handled at state {self.cur_state}')

    def draw(self):
        self.cur_state.draw(self.obj)

    def add_event(self, e):
        print(f'    DEBUG: add event {e}')
        self.event_q.append(e)

    def set_transitions(self, transitions):
        self.transitions = transitions
