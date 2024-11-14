from pico2d import load_image, draw_rectangle
import time
import game_framework
from state_machine import StateMachine, right_down, left_down, right_up, left_up, start_event, s_up, s_down

x_coords = [290, 304, 321]
y_coord = 342
width, height = 16, 16
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

class Mario:
    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, s_down: Jump},  # s_down 추가
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, s_down: Jump},
            Jump: {right_up: Idle, left_up: Idle}  # 필요에 따라 다른 상태로의 전환 추가 가능
        })


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        # fill here
        # 네개의 값, x1, y1, x2, y2
        #return self.x - 20, self.y - 50, self.x + 20, self.y + 50  # 4개의 값으로 구성된 한개의 튜플
        return self.x - 25, self.y + 30, self.x + 25, self.y -30 # 4개의 값으로 구성된 한개의 튜플
        pass

    def handle_collision(self, group, other):
        pass

class Idle:
    @staticmethod
    def enter(mario, e):
        mario.dir = 0
        mario.frame = 0
        if e is not None:  # e가 None이 아닌 경우에만 조건 체크
            if left_up(e) or right_down(e):
                mario.face_dir = -1
            elif right_up(e) or left_down(e) or start_event(e):
                mario.face_dir = 1

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        pass

    @staticmethod
    def draw(mario):
        frame_width = 16
        frame_height = 16
        frame_x = 276
        frame_y = 342
        if mario.face_dir == -1:
            mario.image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                mario.x, mario.y, frame_width * 3, frame_height * 3
            )
        else:
            mario.image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, mario.x, mario.y,
                frame_width * 3, frame_height * 3
            )

class Run:
    @staticmethod
    def enter(mario, e):
        if right_down(e) or left_up(e):
            mario.dir, mario.face_dir, mario.action = 1, 1, 1
        elif left_down(e) or right_up(e):
            mario.dir, mario.face_dir, mario.action = -1, -1, 0
        mario.run_frame_x_positions = [290, 304, 321]  # x 좌표 배열

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        # 애니메이션 프레임 업데이트 (모듈러 연산을 통해 반복)
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(mario.run_frame_x_positions)
        mario.x += mario.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(mario):
        frame_width = 16
        frame_height = 16
        frame_y = 342  # y 좌표는 고정
        frame_x = mario.run_frame_x_positions[int(mario.frame)]  # 정수 변환 후 x 좌표 선택
        if mario.face_dir == -1:
            mario.image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                mario.x, mario.y, frame_width * 3, frame_height * 3
            )
        else:
            mario.image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, mario.x, mario.y,
                frame_width * 3, frame_height * 3
            )



class Jump:
    @staticmethod
    def enter(mario, e):
        mario.start_jump_time = time.time()  # 애니메이션 시작 시간 기록
        mario.jump_frame_x_positions = [336, 353, 321]  # 애니메이션 프레임 위치 설정
        mario.frame = 0  # 애니메이션 초기화

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        # 1초 동안 애니메이션 실행
        if time.time() - mario.start_jump_time > 1:
            mario.state_machine.cur_state = Idle  # 1초 후 원래 상태로 복귀
            mario.state_machine.cur_state.enter(mario, None)
        else:
            # 애니메이션 프레임 업데이트
            mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

    @staticmethod
    def draw(mario):
        frame_width = 16
        frame_height = 16
        frame_y = 342
        frame_x = mario.jump_frame_x_positions[int(mario.frame)]
        if mario.face_dir == -1:
            mario.image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height, 0, 'h',
                mario.x, mario.y, frame_width * 3, frame_height * 3
            )
        else:
            mario.image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, mario.x, mario.y,
                frame_width * 3, frame_height * 3
            )
