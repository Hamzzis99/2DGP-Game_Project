# main.py

from pico2d import *
import game_framework
import play_mode

open_canvas(800, 600)

game_framework.run(play_mode)

close_canvas()