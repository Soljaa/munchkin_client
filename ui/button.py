import pygame
from PPlay.sprite import *
from PPlay.window import Window


class Button:
    def __init__(self, image_path, x, y, width=None, height=None, acao=None):
        self.sprite = Sprite(image_path)
        self.sprite.x = x - self.sprite.width / 2
        self.sprite.y = y - self.sprite.height / 2
        self.acao = acao

        if width and height:
            self.sprite.resize(width, height)

        self.is_hovered = False
        self.is_active = True
        self.mouse = Window.get_mouse()

        # Variável para rastrear o estado do botão do mouse
        self.mouse_held = False

    def draw(self):
        # Desenha o sprite
        self.sprite.draw()

    def verify_hover(self):
        if self.mouse.is_over_object(self.sprite):
            return True
        else:
            return False

    # TODO: Unificar os handles! (há essa diferença pois foram codadas em momentos distintos, com isso, há um handle para cada, na tentativa de se adequar a cada cenário)
    def handle(self): # Para botões do menu e play_selection
        if not self.verify_hover():
            self.is_hovered = False
            self.mouse_held = False  # Reset ao sair do hover
        elif self.verify_hover():
            if not self.is_hovered:
                self.is_hovered = True
                self.play_sound()

            # Verifica se o botão está sendo segurado
            if self.mouse.is_button_pressed(1):
                if not self.mouse_held:
                    self.mouse_held = True
                    self.play_sound()  # Som apenas no início do clique
                return self.acao()  # Executa a ação enquanto o botão está pressionado
            else:
                self.mouse_held = False  # Reset quando o botão é solto

    def handle_event(self): # # Para botões do jogo
        if not self.verify_hover():
            self.is_hovered = False
            self.mouse_held = False  # Reset ao sair do hover
        elif self.verify_hover() and self.is_active:
            if not self.is_hovered:
                self.is_hovered = True
                self.play_sound()

            # Verifica se o botão está sendo segurado
            if self.mouse.is_button_pressed(1) and self.is_active:
                if not self.mouse_held:
                    self.mouse_held = True
                    self.play_sound()
                return True
            else:
                self.mouse_held = False  # Reset quando o botão é solto

        return False

    def play_sound(self):
        pass

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
