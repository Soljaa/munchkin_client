import os
import time
from PPlay.window import *
from PPlay.mouse import *
from PPlay.gameimage import *
import pygame
from ui.hover_button import HoverButton
from ui.click_button import ClickButton
from game.card import Gender
from utils import resource_path


class PlayerSelection:
    def __init__(self, window):
        self.avatar = None
        self.clock = None
        self.color_change_interval = None
        self.last_color_change_time = None
        self.color_index = None
        self.colors = None
        self.buttons = None
        self.avatar_index = None
        self.avatars = None
        self.mouse = None
        self.bg = None
        self.window = window
        self.running = True
        self.input_text = ""
        self.reload_mouse = 0.2
        self.cursor_visible = True
        self.last_blink_time = time.time()
        self.gender = None
        self.use_ai = False

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
        avatars_dir = resource_path("assets/selecao_player/avatares")
        self.avatars = [
            os.path.join(avatars_dir, file)
            for file in os.listdir(avatars_dir)
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
                acao=self.back
            ),
            "continue": HoverButton(
                "assets/selecao_player/continue_button.png",
                self.window.width / 2,
                580,
                acao=self.game
            ),
            "left_arrow": ClickButton(
                "assets/selecao_player/seta_esq.png",
                self.window.width / 2 - 135,
                270,
                acao=lambda: self.update_avatar(1)
            ),
            "right_arrow": ClickButton(
                "assets/selecao_player/seta_dir.png",
                self.window.width / 2 + 135,
                270,
                acao=lambda: self.update_avatar(-1)
            ),
            "male": ClickButton(
                "assets/selecao_player/male.png",
                self.window.width / 2 + 20,
                510,
                acao= lambda: self.set_player_gender(Gender.MALE)
            ),
            "female": ClickButton(
                "assets/selecao_player/female.png",
                self.window.width / 2 + 70,
                510,
                acao=lambda: self.set_player_gender(Gender.FEMALE)
            ),
            "pvp": ClickButton(
                "assets/selecao_player/pvp.png",
                self.window.width / 2 + 20,
                160,
                acao=lambda: self.set_use_ai(False)
            ),
            "pvcom": ClickButton(
                "assets/selecao_player/ia.png",
                self.window.width / 2 + 70,
                160,
                acao=lambda: self.set_use_ai(True)
            ),
        }

        # Espelha a imagem do botão "back"
        self.buttons["back"].sprite.image = pygame.transform.flip(
            self.buttons["back"].sprite.image, True, False
        )

    def set_use_ai(self, value):
        self.use_ai = value
        print(self.use_ai)

    def initialize_animation(self):
        """Inicializa as variáveis para a animação de cores."""
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Cores para aviso
        self.color_index = 0
        self.last_color_change_time = 0  # Tempo da última mudança de cor
        self.color_change_interval = 500  # Intervalo de tempo para mudar a cor (em ms)
        self.clock = pygame.time.Clock() 

    def draw_avatar(self, avatar):
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

    def handle_text_input(self, event):
        """Gerencia a entrada de texto do jogador, lidando com validação e formatação."""
        if event.key == pygame.K_BACKSPACE:  # Verifica se a tecla Backspace foi pressionada
            self.input_text = self.input_text[:-1]  # Remove o último caractere
        else:
            new_char = event.unicode  # Obtém o novo caractere digitado
            if new_char.isalnum():  # Verifica se o caractere é alfanumérico
                self.input_text += new_char  # Adiciona o novo caractere ao texto

    def update_cursor(self):
        """Alterna a visibilidade do cursor em intervalos regulares."""
        current_time = time.time()
        if current_time - self.last_blink_time >= 0.5:  # Alterna a cada 0.5 segundos
            self.cursor_visible = not self.cursor_visible
            self.last_blink_time = current_time

    def get_display_text(self):
        """Retorna o texto formatado com o cursor."""
        if self.cursor_visible:
            return self.input_text + "|"
        else:
            return self.input_text

    def set_player_gender(self, gender):
        self.gender = gender

    def is_valid_nickname(self, nickname):
        """Verifica se o nickname é válido: não vazio, sem espaços e alfanumérico."""
        nick_len = len(nickname)
        return 0 < nick_len <= 16 and " " not in nickname and nickname.isalnum()
    
    def update_avatar(self, incremento):
        """Atualiza a navegação dos avatares."""
        if self.reload_mouse <= 0:
            self.avatar_index = (self.avatar_index + incremento) % len(self.avatars)
            self.reload_mouse = 0.8

    def back(self):
        """Ação para o botão 'back'."""
        self.running = False

    def game(self):
        """Função chamada ao pressionar o botão de continuar."""
        nickname = self.input_text.strip()
        avatar_img_dir = self.avatars[self.avatar_index]
        player_gender = self.gender
        use_ai = self.use_ai
        if self.is_valid_nickname(nickname) and player_gender:
            # Ao invés de chamar main() diretamente, vamos retornar os dados
            return nickname, avatar_img_dir, player_gender, use_ai

    def quit(self):
        self.running = False
        
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
            for name, button in self.buttons.items():
                button.draw()
                if name == "male" and self.gender == Gender.MALE:
                    pygame.draw.circle(
                        self.window.screen,
                        (0, 255, 0),
                        (button.original_x, button.original_y),
                        max(button.original_width, button.original_height) // 2 + 5,
                        3
                    )
                if name == "female" and self.gender == Gender.FEMALE:
                    pygame.draw.circle(
                        self.window.screen,
                        (0, 255, 0),
                        (button.original_x, button.original_y),
                        max(button.original_width, button.original_height) // 2 + 5,
                        3
                    )
                if name == "pvcom" and self.use_ai:
                    pygame.draw.circle(
                        self.window.screen,
                        (0, 0, 0),
                        (button.original_x, button.original_y),
                        max(button.original_width, button.original_height) // 2 + 5,
                        3
                    )
                if name == "pvp" and not self.use_ai:
                    pygame.draw.circle(
                        self.window.screen,
                        (0, 0, 0),
                        (button.original_x, button.original_y),
                        max(button.original_width, button.original_height) // 2 + 5,
                        3
                    )
                if button.handle():
                    return button.handle()
                else:
                    button.handle()

            # Imagem Avatar
            self.avatar = GameImage(self.avatars[self.avatar_index])
            self.draw_avatar(self.avatar)

            for event in pygame.event.get():  # Captura eventos da janela
                if event.type == pygame.QUIT:
                    self.running = False  # Sai do loop se a janela for fechada

                elif event.type == pygame.KEYDOWN:  # Verifica se uma tecla foi pressionada
                    self.handle_text_input(event)

            self.update_cursor()
                    
            # Desenha o campo de entrada (box)
            pygame.draw.rect(self.window.screen, (0,0,0), (input_box_x, input_box_y, input_box_width,
                                                           input_box_height), 2)
            
            # Textos
            self.draw_text(self.window.screen, "Digite seu nickname:", (input_box_x, input_box_y - 30), 28, (0, 0, 0))  # Texto acima do campo
            self.draw_text(self.window.screen, self.get_display_text(), (input_box_x + 10, input_box_y + 10), 28, (0, 0, 0))  # Texto digitado
            self.draw_text(self.window.screen, "Escolha um gênero:", (input_box_x, input_box_y + 110), 28, (0, 0, 0))  # Texto digitado
            self.draw_text(self.window.screen, "Modo de jogo:", (input_box_x + 50, input_box_y - 240), 28, (0, 0, 0))  # Texto digitado

            # Verifica se é hora de alternar a cor do aviso
            current_time = pygame.time.get_ticks()
            if current_time - self.last_color_change_time >= self.color_change_interval:
                self.last_color_change_time = current_time
                self.color_index = (self.color_index + 1) % len(self.colors)

            erro_msg = ""
            # Exibe mensagens de aviso, se necessário
            if len(self.input_text) == 0:
                erro_msg = "AVISO: Insira um nome."
            elif len(self.input_text) > 16:
                erro_msg = "AVISO: Máximo de 16 caracteres."
            self.draw_text(self.window.screen, erro_msg, (input_box_x, input_box_y + input_box_height + 10),
                           20, self.colors[self.color_index])

            if self.reload_mouse > 0:
                self.reload_mouse -= 0.02

            self.window.update()
            self.clock.tick(60)  # Limita o loop a 60 FPS

            """
            # Se o jogador pressionou "continuar", retorna os valores
            if self.buttons["continue"].mouse.is_button_pressed(1) and self.input_text.strip() and self.input_text.isalnum():
                nickname, avatar_img_dir = self.game()
                if nickname and avatar_img_dir:
                    return nickname, avatar_img_dir  # Retorna o nickname e o caminho do avatar"""
