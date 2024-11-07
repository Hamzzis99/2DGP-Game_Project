from pico2d import load_image

from state_machine import StateMachine, right_down, left_down, right_up, left_up, start_event


class Mario:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.face_dir = 1  # 1은 오른쪽, -1은 왼쪽
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)  # 마리오 객체의 상태 머신 생성
        self.state_machine.start(Idle)  # 초기 상태를 Idle로 설정
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # event: 입력 이벤트 (키보드 또는 마우스)
        # 상태 머신에 ('INPUT', event) 형태로 이벤트를 전달합니다.
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()


class Idle:
    @staticmethod
    def enter(mario, e):
        mario.dir = 0  # 정지 상태
        mario.frame = 0
        # 방향 설정
        if left_up(e) or right_down(e):
            mario.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            mario.face_dir = 1

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        # Idle 상태에서는 프레임을 증가시키지 않습니다.
        pass

    @staticmethod
    def draw(mario):
        frame_width = 16
        frame_height = 16
        frame_x = 276  # Idle 상태의 x 좌표
        frame_y = 342  # Idle 상태의 y 좌표

        # 캐릭터를 두 배로 키워서 그립니다.
        if mario.face_dir == -1:
            # 좌우 반전하여 그리기
            mario.image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height,
                0, 'h',  # 각도, 반전 옵션 ('h'는 좌우 반전)
                mario.x, mario.y,
                frame_width * 3, frame_height * 3
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
            mario.dir = 1
            mario.face_dir = 1
        elif left_down(e) or right_up(e):
            mario.dir = -1
            mario.face_dir = -1

        mario.frame = 0

        # Run 상태에서 사용할 프레임 x 좌표 리스트
        mario.run_frame_x_positions = [290, 304, 321]

    @staticmethod
    def exit(mario, e):
        pass

    @staticmethod
    def do(mario):
        mario.x += mario.dir * 5
        mario.frame = (mario.frame + 1) % 3  # 총 3개의 프레임 사용

    @staticmethod
    def draw(mario):
        frame_width = 16
        frame_height = 16
        frame_y = 342  # y 좌표는 동일

        # 현재 프레임의 x 좌표 선택
        frame_x = mario.run_frame_x_positions[mario.frame]

        # 캐릭터를 두 배로 키워서 그립니다.
        if mario.face_dir == -1:
            # 좌우 반전하여 그리기
            mario.image.clip_composite_draw(
                frame_x, frame_y, frame_width, frame_height,
                0, 'h',  # 각도, 반전 옵션 ('h'는 좌우 반전)
                mario.x, mario.y,
                frame_width * 3, frame_height * 3
            )
        else:
            mario.image.clip_draw(
                frame_x, frame_y, frame_width, frame_height, mario.x, mario.y,
                frame_width * 3, frame_height * 3
            )