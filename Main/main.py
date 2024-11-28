#s main.py

from pico2d import *
import game_framework
import play_mode
import game_over
import logo_mode
import title_mode

open_canvas(800, 600)


game_framework.run(title_mode)

close_canvas()