import os
from PPlay.window import *
from PPlay.mouse import *
from PPlay.gameimage import *
import pygame
from widgets.button.hover_button import HoverButton
from widgets.button.click_button import ClickButton


class PlayerSelection:
    def __init__(self, window):
        self.window = window
        self.running = True
        self.input_text = ""
        self.reload_mouse = 0.2

        # Initialization
        self.initialize_window()
        self.initialize_avatars()
        self.initialize_buttons()
        self.initialize_animation()

    def initialize_window(self):
        """Inicializa o fundo da tela de seleção do jogador."""
        self.bg = GameImage("assets/menu/bg_menu3.jpg")
        self.bg.resize(self.window.width, self.window.height)
        self.mouse = Window.get_mouse()

    def initialize_avatars(self):
        """Carrega os avatares disponíveis na pasta específica."""
        self.avatars = [
            os.path.join("assets/selecao_player/avatares", file)
            for file in os.listdir("assets/selecao_player/avatares")
            if file.startswith("avatar") and file.endswith(".png")
        ]
        self.avatar_index = 0  # Índice do avatar atual

    def initialize_buttons(self):
        """Inicializa os botões usados na tela de seleção."""
        self.buttons = {
            "back": HoverButton(
                "assets/menu/back_button.png",
                0.05 * self.window.width,
                0.08 * self.window.height,
                self.back
            ),
            "continue": HoverButton(
                "assets/selecao_player/continue_button.png",
                self.window.width / 2,
                500,
                self.game
            ),
            "left_arrow": ClickButton(
                "assets/selecao_player/seta_esq.png",
                self.window.width / 2 - 135,
                270,
                lambda: self.update_avatar(1)
            ),
            "right_arrow": ClickButton(
                "assets/selecao_player/seta_dir.png",
                self.window.width / 2 + 135,
                270,
                lambda: self.update_avatar(-1)
            ),
        }

        # Espelha a imagem do botão "back"
        self.buttons["back"].sprite.image = pygame.transform.flip(
            self.buttons["back"].sprite.image, True, False
        )

    def initialize_animation(self):
        """Inicializa as variáveis para a animação de cores."""
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Cores para aviso
        self.color_index = 0
        self.last_color_change_time = 0  # Tempo da última mudança de cor
        self.color_change_interval = 500  # Intervalo de tempo para mudar a cor (em ms)
        self.clock = pygame.time.Clock() 

    def draw_avatar(self, avatar, input_box_y):
        """Posiciona e desenha o avatar na tela."""
        avatar.x = self.window.width / 2 - avatar.width / 2
        avatar.y = 195
        avatar.draw()

    def draw_text(self, surface, text, position, font_size, color):
        """Desenha um texto na superfície fornecida."""
        font = pygame.font.Font(None, font_size)  # Usar a fonte padrão do Pygame com o tamanho especificado
        text_surface = font.render(text, True, color)  # Renderiza o texto
        text_rect = text_surface.get_rect(topleft=position)  # Obtém o retângulo do texto para posicionamento
        surface.blit(text_surface, text_rect)  # Desenha o texto na superfície fornecida

    def handle_text_imput(self, event):
        """Gerencia a entrada de texto do jogador, lidando com validação e formatação."""
        if event.key == pygame.K_RETURN:  # Verifica se a tecla Enter foi pressionada
            nickname = self.input_text.strip()  # Obtém o nickname
            print("Nickname inserido:", nickname)
            if self.is_valid_nickname(nickname): # Se nickname válido 
                self.running = False  
            else: # Se o nickname inválido
                if len(nickname) == 0:
                    print("AVISO: Insira um nome.")
                elif " " in nickname:
                    print("AVISO: Não é permitido espaço.")

        elif event.key == pygame.K_BACKSPACE:  # Verifica se a tecla Backspace foi pressionada
            self.input_text = self.input_text[:-1]  # Remove o último caractere
        else:
            new_char = event.unicode  # Obtém o novo caractere digitado
            if new_char != " " and new_char:  # Ignora espaços e caracteres vazios
                self.input_text += new_char  # Adiciona o novo caractere ao texto

    def is_valid_nickname(self, nickname):
        """Verifica se o nickname é válido: não vazio, sem espaços e alfanumérico."""
        return len(nickname) > 0 and " " not in nickname and nickname.isalnum()
    
    def update_avatar(self, incremento):
        """Atualiza a navegação dos avatares."""
        self.avatar_index = (self.avatar_index + incremento) % len(self.avatars)

    def back(self):
        """Ação para o botão 'back'."""
        self.running = False

    def game(self):
        """Função chamada ao pressionar o botão de continuar."""
        raise StartGameException(self.input_text.strip())
        
    def run(self):
        """Loop principal da tela de seleção do jogador."""
        if pygame.key.get_pressed()[pygame.K_F11]:
                pygame.display.toggle_fullscreen()
                
        input_box_width = 400
        input_box_height = 40
        input_box_x = (self.window.width - input_box_width) // 2
        input_box_y = ((self.window.height - input_box_height) // 2) + 50

        while self.running:
            self.bg.draw()

            # Botões 
            for button in self.buttons.values():
                button.draw()
                if self.mouse.is_over_object(button.sprite) and self.mouse.is_button_pressed(1) and self.reload_mouse <= 0:
                    self.reload_mouse = 0.2
                    button.acao()

            # Imagem Avatar
            avatar = GameImage(self.avatars[self.avatar_index])
            self.draw_avatar(avatar, input_box_y)

            for event in pygame.event.get():  # Captura eventos da janela
                if event.type == pygame.QUIT:
                    self.running = False  # Sai do loop se a janela for fechada

                elif event.type == pygame.KEYDOWN:  # Verifica se uma tecla foi pressionada
                    self.handle_text_imput(event)
                    
            # Desenha o campo de entrada (box)
            input_box_width = 400
            input_box_height = 40
            input_box_x = (self.window.width - input_box_width) // 2
            input_box_y = ((self.window.height - input_box_height) // 2) + 50
            pygame.draw.rect(self.window.screen, (0,0,0), (input_box_x, input_box_y, input_box_width, input_box_height), 2)
            
            # Textos
            self.draw_text(self.window.screen, "Digite seu nickname:", (input_box_x, input_box_y - 30), 28, (0, 0, 0))  # Texto acima do campo
            self.draw_text(self.window.screen, self.input_text, (input_box_x + 10, input_box_y + 10), 28, (0, 0, 0))  # Texto digitado

            # Verifica se é hora de alternar a cor do aviso
            current_time = pygame.time.get_ticks()
            if current_time - self.last_color_change_time >= self.color_change_interval:
                self.last_color_change_time = current_time
                self.color_index = (self.color_index + 1) % len(self.colors)

            # Exibe mensagens de aviso, se necessário
            if len(self.input_text) == 0:
                self.draw_text(self.window.screen, "AVISO: Insira um nome.", (input_box_x, input_box_y + input_box_height + 10), 20, self.colors[self.color_index])
            elif " " in self.input_text:
                self.draw_text(self.window.screen, "AVISO: Não é permitido espaço.", (input_box_x, input_box_y + input_box_height + 10), 20, self.colors[self.color_index])

            if self.reload_mouse > 0:
                self.reload_mouse -= 0.02

            self.window.update()
            #pygame.display.flip()  # Atualiza a tela do Pygame
            self.clock.tick(60)  # Limita o loop a 60 FPS


class StartGameException(Exception):
    pass
