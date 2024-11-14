from pico2d import load_image, draw_rectangle
import game_framework
from state_machine import StateMachine, right_down, left_down, right_up, left_up, s_down

# 전역 변수 선언
global_y = 90  # 캐릭터의 초기 Y 좌표

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
        global global_y
        self.x, self.y = 400, global_y
        self.face_dir = 1
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, s_down: Jump},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, s_down: Jump},
            Jump: {right_up: Idle, left_up: Idle}
        })

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y + 30, self.x + 25, self.y - 30

    def handle_collision(self, group, other):
        pass

class Idle:
    @staticmethod
    def enter(mario, e):
        mario.dir = 0
        mario.frame = 0
        if e is not None:
            if left_up(e) or right_down(e):
                mario.face_dir = -1
            elif right_up(e) or left_down(e) or s_down(e):
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
            mario.dir, mario.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            mario.dir, mario.face_dir = -1, -1
        mario.run_frame_x_positions = [290, 304, 321]

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(mario.run_frame_x_positions)
        mario.x += mario.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(mario):
        frame_width = 16
        frame_height = 16
        frame_y = 342
        frame_x = mario.run_frame_x_positions[int(mario.frame)]
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
    JUMP_VELOCITY = 200
    GRAVITY = -300

    @staticmethod
    def enter(mario, e):
        global global_y
        mario.jump_speed = Jump.JUMP_VELOCITY
        mario.jump_frame_x_positions = [336, 353, 321]
        mario.frame = 0
        mario.y = global_y

    @staticmethod
    def exit(mario, e):
        global global_y
        global_y = mario.y
        mario.jump_speed = 0
        mario.dir = 0

    @staticmethod
    def do(mario):
        global global_y
        mario.y += mario.jump_speed * game_framework.frame_time
        mario.jump_speed += Jump.GRAVITY * game_framework.frame_time
        global_y = mario.y

        if mario.y <= 90:
            mario.y = 90
            mario.state_machine.cur_state = Idle
            mario.state_machine.cur_state.enter(mario, None)

        if mario.dir != 0:
            mario.x += mario.dir * RUN_SPEED_PPS * game_framework.frame_time

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
