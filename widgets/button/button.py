from PPlay.sprite import *
from PPlay.window import Window

class Button:
    def __init__(self, image_path, x, y, acao=None):  
        self.sprite = Sprite(image_path)
        self.sprite.x = x - self.sprite.width/2
        self.sprite.y = y - self.sprite.height/2
        self.acao = acao
        self.mouse = Window.get_mouse()

    def draw(self):  
        self.sprite.draw()