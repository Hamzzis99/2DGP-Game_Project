from pico2d import load_image, draw_rectangle
import game_framework
from state_machine import StateMachine, right_down, left_down, right_up, left_up, start_event

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
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle}
        })

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision(self, group, other):
        pass

class Idle:
    @staticmethod
    def enter(mario, e):
        mario.dir = 0
        mario.frame = 0
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
