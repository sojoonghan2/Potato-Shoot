from pico2d import load_image


class Ground:
    def __init__(self):
        self.image = load_image('Resource\\Ground\\Ground1.png')
        # self.image = load_image('Resource\\Ground\\Ground2.png')
        # self.image = load_image('Resource\\Ground\\Ground3.png')

    def draw(self):
        self.image.draw_to_origin(0, 0, 540, 960)

    def update(self):
        pass
