from PPlay.sprite import *
from ui.button import Button  # Importa a classe Button
from utils import resource_path

class ClickButton(Button):
    def __init__(self, image_path, x, y, width=None, height=None, acao=None):  # Inicializa o botão
        # Chama o construtor da classe base (Button) para inicializar o sprite e os parâmetros comuns
        super().__init__(image_path, x, y, width, height, acao)
        
        # Atribuindo as variáveis específicas do ClickButton (Tudo isso pra fazer o movimento do clique)
        self.original_x = x
        self.original_y = y

        self.original_width = self.sprite.width  # Guarda o tamanho original do botão
        self.original_height = self.sprite.height
        self.hovered_width = self.original_width * 0.9
        self.hovered_height = self.original_height * 0.9

        # Variável para rastrear se o botão está sendo segurado
        self.mouse_held = False

    def update(self):  # Atualiza o estado do botão (verifica clique)
        if self.mouse.is_over_object(self.sprite) and self.mouse.is_button_pressed(1):
            self.sprite.set_scale(self.hovered_width / self.original_width,
                                  self.hovered_height / self.original_height)  # Muda o tamanho
            self.sprite.x = self.original_x - self.sprite.width / 2  # Recentraliza o botão
            self.sprite.y = self.original_y - self.sprite.height / 2  # Recentraliza o botão
        else:
            self.sprite.set_scale(1, 1)  # Volta ao tamanho original
            self.sprite.x = self.original_x - self.sprite.width / 2  # Recentraliza o botão
            self.sprite.y = self.original_y - self.sprite.height / 2  # Recentraliza o botão

    def draw(self):  # Desenhar os Botões
        self.update()  # Atualiza o estado antes de desenhar
        self.sprite.draw()

    def handle(self):
        if not self.verify_hover():
            self.is_hovered = False
            self.mouse_held = False  # Reset ao sair do hover
        elif self.verify_hover():
            if not self.is_hovered:
                self.is_hovered = True

            if self.mouse.is_button_pressed(1):
                if not self.mouse_held:
                    self.mouse_held = True
                    self.play_sound()  # Som apenas no início do clique
                self.acao()  # Executa a ação enquanto o botão está pressionado
            else:
                self.mouse_held = False  # Reset quando o botão é solto

    def handle_event(self):
        if self.acao:
            self.handle()

        if not self.verify_hover():
            self.is_hovered = False
            self.mouse_held = False  # Reset ao sair do hover
        elif self.verify_hover() and self.is_active:
            if not self.is_hovered:
                self.is_hovered = True

            if self.mouse.is_button_pressed(1) and self.is_active:
                if not self.mouse_held:
                    self.mouse_held = True
                    self.play_sound()
                return True
            else:
                self.mouse_held = False  # Reset quando o botão é solto

        self.is_hovered = False
        return False

    def play_sound(self):
        hovered_button_sound = pygame.mixer.Sound(resource_path("assets/sounds/clicked_button.mp3"))
        hovered_button_sound.play()