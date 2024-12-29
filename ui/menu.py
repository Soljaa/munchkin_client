
import sys
from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.gameimage import *
from ui.hover_button import HoverButton
from ui.player_selection import PlayerSelection


class Menu:
    def __init__(self, width, height):  # Inicialização do MENU
        self.initialize_window(width, height)
        self.initialize_buttons()
        self.running = True
        self.fullscreen = False

    def initialize_window(self, width, height):
        """Inicializa a window e a imagem de fundo."""
        self.window = Window(width, height)
        self.window.set_background_color((246, 255, 238))
        self.window.set_title("MUNCHKIN")
        self.bg = GameImage("assets/menu/bg.png")
        self.bg.resize(width, height)
        self.mouse = Window.get_mouse()

    def initialize_buttons(self):
        """Inicializa os botões do menu."""
        self.buttons = {
            "play": HoverButton(
                "assets/menu/jogar_button.png",
                self.window.width/2, 
                0.36*self.window.height,
                acao=self.play,
            ),
            "options": HoverButton(
                "assets/menu/opcoes_button.png",
                self.window.width/2, 
                0.49*self.window.height,
                acao=self.options
            ),
            "exit": HoverButton(
                "assets/menu/sair_button.png",
                self.window.width/2, 
                0.62*self.window.height,
                acao= self.quit
            )
        }


    def play(self):
        """Função chamada ao pressionar o botão de jogar."""
        selecao_player = PlayerSelection(self.window)
        selecao_player.run()
        self.quit()
        
    def quit(self):
        sys.exit()

    def options(self):
        return

    def run(self):
        """Executa o loop principal do menu."""
        while self.running:
            # if pygame.key.get_pressed()[pygame.K_F11]:
            #     pygame.display.toggle_fullscreen() fazer para todas as telas

            self.bg.draw()  
            for button in self.buttons.values():
                button.draw()
                button.handle()

            self.window.update()


if __name__ == "__main__":
    menu = Menu(1280, 720)
    menu.run()
