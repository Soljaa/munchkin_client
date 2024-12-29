import pygame
from PPlay.sprite import *
from PPlay.window import Window

class Button:
    def __init__(self, image_path, x, y, width=None, height=None, acao=None):
        self.sprite = Sprite(image_path)
        self.sprite.x = x - self.sprite.width/2
        self.sprite.y = y - self.sprite.height/2
        self.acao = acao

        if width and height:
            resized_image = pygame.transform.scale(self.sprite.image, (width, height))
            self.sprite.image = resized_image

        self.is_hovered = False
        self.is_active = True

        self.mouse = Window.get_mouse()


    def draw(self):
        # Desenha o sprite
        self.sprite.draw()

    def handle(self):
        if self.mouse.is_over_object(self.sprite) and self.mouse.is_button_pressed(1):
            self.acao()

    def handle_event(self):
        if self.acao:
            self.handle()

        if self.mouse.is_over_object(self.sprite) and self.mouse.is_button_pressed(1) and self.is_active:
            #self.acao()
            return True
        return False

    """
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and self.is_active:
                return True
        return False
    """

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
