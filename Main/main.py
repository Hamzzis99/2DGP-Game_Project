#main.py

from pico2d import *
import game_framework
import play_mode
import game_over
import logo_mode
import thank_you
import title_mode
import world_start_mode

open_canvas(800, 600)


game_framework.run(logo_mode)

close_canvas()