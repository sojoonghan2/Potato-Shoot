from pico2d import load_image


class Water:
    def __init__(self, x = 140, y = 500):
        self.image = load_image('Resource\\Water\\Water.png')
        self.x, self.y = x, y

    def draw(self):
        self.image.draw_to_origin(self.x, self.y, 540, 1280)

    def update(self):
        pass
