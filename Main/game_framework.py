# game_framework.py
import time

running = False
stack = []
frame_time = 0.0  # 전역 변수로 frame_time 선언

def change_mode(mode):
    global stack
    if len(stack) > 0:
        stack[-1].finish()
        stack.pop()
    stack.append(mode)
    mode.init()

def push_mode(mode):
    global stack
    if len(stack) > 0:
        stack[-1].pause()
    stack.append(mode)
    mode.init()

def pop_mode():
    global stack
    if len(stack) > 0:
        stack[-1].finish()
        stack.pop()

    if len(stack) > 0:
        stack[-1].resume()

def quit():
    global running
    running = False

def run(start_mode):
    global running, stack, frame_time
    running = True
    stack = [start_mode]
    start_mode.init()

    current_time = time.time()
    while running:
        stack[-1].handle_events()
        stack[-1].update()  # 인자 없이 호출
        stack[-1].draw()
        frame_time = time.time() - current_time
        frame_time = min(frame_time, 0.05)  # 프레임 타임 제한
        frame_rate = 1.0 / frame_time if frame_time > 0 else 0
        current_time += frame_time

    while len(stack) > 0:
        stack[-1].finish()
        stack.pop()
