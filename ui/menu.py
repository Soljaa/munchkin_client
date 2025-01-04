
import sys
from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.gameimage import *
from game.game_manager import main
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

    def play_music(self):
        music_path = "assets/sounds/medieval_music.mp3"
        self.medieval_music_sound = pygame.mixer.Sound(music_path)
        self.medieval_music_sound.play()
        
    def stop_music(self):
        self.medieval_music_sound.fadeout(800)

    def play_transition_fade_sound(self):
        sound_path = "assets/sounds/transition_fade.mp3"
        self.transition_fade_sound = pygame.mixer.Sound(sound_path)
        self.transition_fade_sound.set_volume(0.3)
        self.transition_fade_sound.play()


    def play(self):
        """Função chamada ao pressionar o botão de jogar."""
        selecao_player = PlayerSelection(self.window)
        result = selecao_player.run()  # Retorna o nickname e avatar_img_dir
        if result:
            nickname, avatar_img_dir, gender = result
            self.stop_music()
            self.play_transition_fade_sound()
            main(nickname, avatar_img_dir, gender)  # Passa os valores para o main()
            self.quit()
        
    def quit(self):
        sys.exit()

    def options(self):
        return

    def run(self):
        self.play_music()
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
