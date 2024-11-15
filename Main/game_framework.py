# game_framework.py
import time

def change_mode(mode):
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        stack.pop()

    # execute resume function of the previous mode
    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global running
    running = False


def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    global frame_time
    frame_time = 0.0
    current_time = time.time()
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        frame_time = time.time() - current_time
        # 프레임 타임 제한 (예: 0.05초)
        frame_time = min(frame_time, 0.05)
        frame_rate = 1.0 / frame_time if frame_time > 0 else 0
        current_time += frame_time
        # print(f'Frame Time: {frame_time:.5f}, Frame Rate: {frame_rate:.2f}')  # 주석 처리됨

    # 스택에 남아있는 모든 모드의 finish 함수 실행
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()