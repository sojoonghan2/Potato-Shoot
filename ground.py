from pico2d import load_image, load_music
import random

class Ground:
    def __init__(self):
        stage = random.randint(0, 2)
        if stage == 0:
            self.image = load_image('Resource\\Ground\\Ground1.png')
        elif stage == 1:
            self.image = load_image('Resource\\Ground\\Ground2.png')
        else:
            self.image = load_image('Resource\\Ground\\Ground3.png')

    def draw(self):
        self.image.draw_to_origin(0, 0, 540, 960)

    def update(self):
        pass
