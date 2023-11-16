from pico2d import open_canvas, close_canvas
import game_framework
import title_mode

import play_mode as start_mode

open_canvas(540, 960)
game_framework.run(title_mode)
close_canvas()