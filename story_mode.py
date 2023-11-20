from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE
import game_framework
from pico2d import get_events, load_image, clear_canvas, update_canvas, load_music
import play_mode
from ground import Ground


def init():
    global image
    global ground
    image = load_image('Resource\\Ground\\story.png')
    ground = Ground()


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(270, 480)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)


def pause():
    pass


def resume():
    pass
