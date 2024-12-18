from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.gameimage import *

class Game:
    def __init__(self, janela):
        self.janela = janela
        self.janela.set_background_color((0, 255, 0))
        self.bg = GameImage("assets/game/main-gameboard.jpg")  # Carrega a imagem de fundo do menu
        # Redimensiona a imagem de fundo para preencher a tela
        self.running = True
    
    def run(self):
        while self.running:
            if pygame.key.get_pressed()[pygame.K_F11]:
                pygame.display.toggle_fullscreen()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.running = False
            self.bg.draw()
            self.janela.update()


