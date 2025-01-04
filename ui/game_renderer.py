import pygame
from PPlay.sprite import *
from PPlay.window import Window
from constants import *
from game.card import Item, CardType
from ui.hover_button import HoverButton
from game.game_state import GamePhase
from game.combat import CombatStates


BUTTONS_BY_GAME_PHASE = {
    GamePhase.SETUP: ["kick_door", "sell_items"],  # Adiciona sell_items,
    GamePhase.KICK_DOOR: ["look_for_trouble", "loot"],
    GamePhase.LOOK_FOR_TROUBLE: [],
    GamePhase.LOOT_ROOM: [],
    GamePhase.COMBAT: ["run_away", "use_card", "ask_for_help", "finish_combat"],
    GamePhase.CHARITY: [],
    GamePhase.FINAL_SETUP: ["end_turn", "sell_items"]
}

COMBAT_CONDITIONS = {
    CombatStates.WINNING: ["use_card", "finish_combat"],
    CombatStates.LOSING: ["run_away", "use_card", "ask_for_help"]
}


class GameRenderer:
    _instance = None

    def __init__(self, screen):
        if GameRenderer._instance is None:
            GameRenderer._instance = self
        self.screen = screen
        self.gameboard = pygame.image.load("assets/gameboard.png")
        self.dungeon_background = pygame.image.load("assets/dungeon_background.png")
        self.buttons = {}
        self.message = ""
        self.message_timer = 0
        self._init_buttons()
        self.zoomed_card: Sprite | None = None
        self.mouse = Window.get_mouse()
        self.equip_holder = pygame.transform.scale(pygame.image.load("assets/game/equip_holder.png"), (100, 150))
        self.hand_card_sprites = []  # [(card_sprite, card)]
        self.equipped_card_sprites = []  # [(card_sprite, card)]]

    @classmethod
    def get_instance(cls):
        return cls._instance

    def _init_buttons(self):
        button_y0 = SCREEN_HEIGHT - 270
        button_y1 = SCREEN_HEIGHT - 410
        button_y2 = SCREEN_HEIGHT - 490
        button_y3 = SCREEN_HEIGHT - 570
        button_y4 = SCREEN_HEIGHT - 330  # Nova posição para o botão vender
        buttons_x = SCREEN_WIDTH - 100
        buttons_x2 = SCREEN_WIDTH - 780

        self.buttons = {
            "kick_door": HoverButton("assets/game/kick_door_new.png", buttons_x, button_y0, 147, 142),
            "use_card": HoverButton("assets/game/use_card.png", buttons_x, button_y2, 160, 66),
            "run_away": HoverButton("assets/game/run_away.png", buttons_x, button_y1, 160, 66),
            "look_for_trouble": HoverButton("assets/game/look_for_trouble.png", buttons_x, button_y1, 160, 66),
            "ask_for_help": HoverButton("assets/game/ask_for_help.png", buttons_x, button_y3, 160, 66),
            "loot": HoverButton("assets/game/loot.png", buttons_x, button_y2, 160, 66),
            "finish_combat": HoverButton("assets/game/finish_combat.png", buttons_x, button_y1, 160, 66),
            "end_turn": HoverButton("assets/game/end_turn.png", buttons_x, button_y1, 160, 66),
            "sell_items": HoverButton("assets/game/sell_items.png", buttons_x2, button_y4, 160, 66)
        }

    def draw_gameboard(self):
        self.screen.blit(self.gameboard, (0, 0)) #Minimapa
        pygame.draw.rect(self.screen, BROWN, (402, 0, 5, 720))

    def draw_dungeon_background(self):
        self.screen.blit(self.dungeon_background, (402, 0))
        self.screen.blit(self.equip_holder, (428, 440))

    def draw_avatars(self, players):
        # Configuração de posição inicial e incrementos para cada nível dos avatares
        level_positions = {
            0: {"base_x": 150, "base_y": 620, "increment_x": 30, "increment_y": 30},
            1: {"base_x": 230, "base_y": 550, "increment_x": 35, "increment_y": 0},
            2: {"base_x": 305, "base_y": 430, "increment_x": 25, "increment_y": 35},
            3: {"base_x": 175, "base_y": 440, "increment_x": 40, "increment_y": 25},
            4: {"base_x": 150, "base_y": 335, "increment_x": 40, "increment_y": 30},
            5: {"base_x": 35, "base_y": 330, "increment_x": 20, "increment_y": 20},
            6: {"base_x": 40, "base_y": 220, "increment_x": 35, "increment_y": 25},
            7: {"base_x": 157, "base_y": 180, "increment_x": 37, "increment_y": 40},
            8: {"base_x": 310, "base_y": 141, "increment_x": 23, "increment_y": 20},
            9: {"base_x": 305, "base_y": 25, "increment_x": 30, "increment_y": 40},
            10: {"base_x": 182, "base_y": 45, "increment_x": 40, "increment_y": 40},
        }

        # Armazena contadores de deslocamento para cada nível (level_counters é como se fosse a quantidade de avatares/jogadores no nível)
        level_counters = {level: 0 for level in level_positions}

        for player in players:
            player_level = player.level  # Obtém o nível do jogador
            if player_level not in level_positions:
                continue  # Ignora jogadores com níveis não definidos

            # Recupera configuração para o nível atual
            level_config = level_positions[player_level]
            base_x = level_config["base_x"]
            base_y = level_config["base_y"]
            increment_x = level_config["increment_x"]
            increment_y = level_config["increment_y"]

            # Calcula posição com base no índice do jogador no nível
            index = level_counters[player_level]
            if increment_y > 0:  # "Listinha" para níveis com increment_y > 0
                col = index % 2  # Alterna entre coluna 0 e 1
                row = index // 2  # Define a linha com base no índice
                offset_x = col * increment_x
                offset_y = row * increment_y
            else:  # Padrão para outros níveis
                offset_x = index * increment_x
                offset_y = 0

            # Incrementa o contador para o nível atual
            level_counters[player_level] += 1

            # Cria e posiciona o sprite do jogador
            player_sprite = Sprite(player.avatar_img_dir)
            player_sprite.x = base_x + offset_x
            player_sprite.y = base_y + offset_y

            # Redimensionar a imagem para 50% do tamanho original
            new_width = int(player_sprite.image.get_width() * 0.25)
            new_height = int(player_sprite.image.get_height() * 0.25)
            resized_image = pygame.transform.scale(player_sprite.image, (new_width, new_height))

            # Atualiza a imagem do Sprite com a redimensionada
            player_sprite.image = resized_image

            # Desenha o Sprite
            player_sprite.draw()

    def draw_dice_animation(self, dice):
        roll_time_seconds = 1.5  # Tempo total de animação do dado rolando em segundos
        elapsed_time = 0  # Variável para controlar o tempo de animação
        
        clock = pygame.time.Clock()
        
        rolling_dice_sound = pygame.mixer.Sound("assets/sounds/rolling_dice.mp3")
        rolling_dice_sound.play()
        while elapsed_time < roll_time_seconds:
            # Calcula o tempo entre quadros
            delta_time = clock.tick(60) / 1000.0  # 60 FPS

            elapsed_time += delta_time  # Atualiza o tempo decorrido
            dice.draw_rolling_dice(SCREEN_WIDTH/2-dice.sprite_rolling_dice.width/2, SCREEN_HEIGHT/2-dice.sprite_rolling_dice.height/2) # Animação do rolamento do dado

            self.draw_dungeon_background()
            self.draw_gameboard()

        dice.draw_value_dice(SCREEN_WIDTH/2-dice.sprite_value_dice.width/2, SCREEN_HEIGHT/2-dice.sprite_value_dice.height/2)
        time.sleep(1)

    def draw_alert_player_die(self, player): #TODO Talvez colocar algo dentro de Death.draw()
        # Background
        self.screen.blit(pygame.image.load("assets/death_background.jpg"), (0, 0))

        # Cria o objeto de fonte para o texto
        font = pygame.font.SysFont("Comic Sans MS", 40, bold=True)

        # Texto dividido em duas linhas
        text_lines = [
            font.render(f"{player.name}", True, (255, 255, 255)),  # Primeira linha
            font.render("morreu!", True, (255, 255, 255))  # Segunda linha
        ]

        # Calcula a posição central da tela
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        # Avatar do referido jogador
        avatar_img = pygame.image.load(player.avatar_img_dir)
        self.screen.blit(avatar_img, (center_x - avatar_img.get_width()/2,60))

        # Desenha o texto, linha por linha
        pos_y = center_y-40
        for line in text_lines:
            text_rect = line.get_rect(center=(center_x + 5, pos_y))
            self.screen.blit(line, text_rect)
            pos_y += 70

        pygame.display.flip()
        time.sleep(2.5)

    def draw_transition(self, image_path, sound_path=None, duration=2.0, extra_element=None):
        """
        Desenha uma transição genérica na tela.

        Args:
            image_path (str): Caminho para a imagem a ser exibida.
            sound_path (str, optional): Caminho para o som a ser tocado. Default é None.
            duration (float): Duração da transição em segundos. Default é 2.0.
            extra_element (callable, optional): Função que desenha elementos extras na tela. Default é None.
        """
        # Carrega a imagem de transição
        transition_image = pygame.image.load(image_path)

        # Toca o som, se fornecido
        if sound_path:
            sound = pygame.mixer.Sound(sound_path)
            sound.play()

        # Controle do tempo de animação
        elapsed_time = 0
        clock = pygame.time.Clock()

        while elapsed_time < duration:
            delta_time = clock.tick(60) / 1000.0  # 60 FPS
            elapsed_time += delta_time

            # Desenha a imagem de transição
            self.screen.blit(transition_image, (0, 0))

            # Desenha o elemento extra, se fornecido
            if extra_element:
                extra_element()

            pygame.display.update()

    def draw_kick_door_transition(self):
        self.draw_transition(
            image_path="assets/game/kick_door_transition.jpg",
            sound_path="assets/sounds/kick_door.mp3",
            duration=2.0
        )

    def draw_loot_the_room_transition(self, loot_card):
        def draw_card():
            # Configuração da carta centralizada
            card_sprite = Sprite(loot_card.image)
            card_x = (self.screen.get_width() - card_sprite.width) // 2
            card_y = (self.screen.get_height() - card_sprite.height) // 2
            card_sprite.x = card_x
            card_sprite.y = card_y
            card_sprite.draw()

        self.draw_transition(
            image_path="assets/game/loot_the_room_transition.png",
            sound_path="assets/sounds/loot_the_room.mp3",
            duration=2.5,
            extra_element=draw_card
        )

    def draw_charity_fase_transition(self, donor, players, distribution):  # TODO: Polir
        """
        Exibe a distribuição de cartas para os jogadores na fase de caridade na tela do Pygame, com um botão para continuar.
        """
        transition_image = pygame.image.load("assets/game/charity_transition.jpg")

        # contraste
        contrast_width = max([max([len(cards) for cards in distribution.values()]) * 100, 200])
        rect_surface = pygame.Surface((contrast_width + 200, SCREEN_HEIGHT), pygame.SRCALPHA)
        rect_surface.fill((255, 255, 255, 200))

        font = pygame.font.Font(None, 36)
        y_position = 40  # Posição inicial no eixo Y

        # Título da seção
        title_text = font.render(f"Doador:", True, (0, 0, 0))
        player_name = font.render(f"{donor.name}", True, (0, 0, 0))

        continue_btn = HoverButton("assets/game/continue.png", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 50, 160, 66)

        waiting = True
        while waiting:

            # posições iniciais
            players_y_position = y_position + 60
            cards_x_position = 50

            # background
            self.screen.blit(transition_image, (0, 0))

            # contraste
            self.screen.blit(rect_surface, (0, 0))

            # Título da seção
            self.screen.blit(title_text, (50, y_position))
            self.screen.blit(player_name, (50, y_position + 25))

            # Itera sobre todos os jogadores, incluindo os que não receberam cartas
            for player in players:
                # Exibe o nome do jogador
                player_text = font.render(f"{player.name}:", True, (0, 0, 0))
                self.screen.blit(player_text, (50, players_y_position))
                players_y_position += 30

                # Verifica se o jogador recebeu cartas
                cards = distribution.get(player, [])
                if cards:
                    # Renderiza os sprites das cartas se o jogador recebeu cartas
                    for card in cards:
                        try:
                            card_sprite = pygame.image.load(card.image).convert_alpha()
                            card_sprite = pygame.transform.scale(card_sprite, (100, 150))
                            self.screen.blit(card_sprite, (cards_x_position, players_y_position))
                            cards_x_position += 110  # Move a posição X para o próximo sprite de carta
                        except Exception as e:
                            print(f"Erro ao carregar sprite da carta: {card.image}. Erro: {e}")
                    cards_x_position = 50
                else:
                    # Se o jogador não recebeu cartas, exibe uma mensagem simples
                    no_cards_text = font.render("Não recebeu nada...", True, (0, 0, 0))
                    self.screen.blit(no_cards_text, (50, players_y_position))

                players_y_position += 160  # Move a posição Y para o próximo jogador

            # continue btn
            continue_btn.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
                if continue_btn.handle_event():
                    waiting = False
            pygame.display.flip()

    def draw_run_away_success_transition(self):
        self.draw_transition(
            image_path="assets/game/run_away_success.jpg",
            duration=2.0
        )

    def draw_run_away_failed_transition(self):
        self.draw_transition(
            image_path="assets/game/run_away_failed.jpg",
            duration=2.0
        )

    def draw_game_state(self, game_state):
        # cuidado, a ordem dos draws importa

        # Draw current player info
        player = game_state.current_player()
        players = game_state.players
        self._draw_player_info(player, 430, 10)

        # Draw equipped items
        self._draw_player_equips(player)

        # Draw avatars
        self.draw_avatars(players)

        # deck info
        self._draw_decks_info(game_state)
        
        # Draw current combat if any
        if game_state.current_combat:
            self._draw_combat(game_state.current_combat, 620, 180)
        
        # Draw buttons based on game phase
        self._draw_buttons(game_state)

        # Draw hand
        self._draw_hand(player, 430, 190)
        
        # Draw message if any
        self._draw_message()

        # Draw phase indicator at the top
        self._draw_phase_indicator(game_state.phase, 570, 120)

    def _draw_phase_indicator(self, phase, x, y):
        font = pygame.font.Font(None, 32)
        phase_text = f"Fase: {phase.value}"
        surface = font.render(phase_text, True, WHITE)
        self.screen.blit(surface, (x, y))

    def _draw_player_info(self, player, x, y):
        # Carregar e configurar o avatar
        player_sprite = Sprite(player.avatar_img_dir)
        new_width = int(player_sprite.image.get_width() * 0.8)
        new_height = int(player_sprite.image.get_height() * 0.8)
        resized_image = pygame.transform.scale(player_sprite.image, (new_width, new_height))

        # Desenhar avatar
        player_sprite.image = resized_image
        player_sprite.x = x
        player_sprite.y = y
        player_sprite.draw()

        # Desenhar informações
        font = pygame.font.Font(None, 26)
        texts = [
            f"Jogador: {player.name} | {player.gender.value}",
            f"Nível: {player.level}",
            f"Força: {player.calculate_combat_strength()}",
            f"Raça: {player.get_player_race()}",
            f"Ouro: {player.gold}"  # Nova linha adicionada para mostrar o gold
        ]

        text_x = x + new_width + 20
        for i, text in enumerate(texts):
            surface = font.render(text, True, WHITE)
            self.screen.blit(surface, (text_x, y + 10 + i * 20))

    def _draw_player_equips(self, player):
        equipped_card_positions = {
            'head': (465, 440),
            'armor': (465, 490),
            'l_hand': (500, 490),
            'r_hand': (430, 490),
            'feet': (465, 540),
            'class': (440, 420),
            'no-slot': (550, 460),
        }
        r_hand_used = False

        self.equipped_card_sprites = []

        # revisar display para usar o super munchkin
        if player.class_:
            item_sprite = Sprite(player.class_[0].image)  # aqui
            item_sprite.resize(30, 45)
            item_sprite.draw()

            self.handle_card_hover(player.class_, item_sprite)

            self.equipped_card_sprites.append((item_sprite, player.class_))

        no_slot_x_offset = 0
        no_slot_y_offset = 0

        no_slot_items_sprite = []

        for item in player.equipped_items:
            item_sprite = Sprite(item.image)
            item_sprite.resize(30, 45)

            # Usar Enum
            pos_x = 0
            pos_y = 0

            if item.slot:
                if item.slot == 'head':
                    pos_x = equipped_card_positions['head'][0]
                    pos_y = equipped_card_positions['head'][1]

                if item.slot == 'feet':
                    pos_x = equipped_card_positions['feet'][0]
                    pos_y = equipped_card_positions['feet'][1]

                if item.slot == 'armor':
                    pos_x = equipped_card_positions['armor'][0]
                    pos_y = equipped_card_positions['armor'][1]

                if item.slot == 'hands':
                    if not r_hand_used:
                        pos_x = equipped_card_positions['r_hand'][0]
                        pos_y = equipped_card_positions['r_hand'][1]
                        r_hand_used = True
                    else:
                        pos_x = equipped_card_positions['l_hand'][0]
                        pos_y = equipped_card_positions['l_hand'][1]
            else:
                pos_x = equipped_card_positions['no-slot'][0] + no_slot_x_offset
                pos_y = equipped_card_positions['no-slot'][1] + no_slot_y_offset

                no_slot_items_sprite.append(item_sprite)
                no_slot_y_offset += 50
                if len(no_slot_items_sprite) % 2 == 0:
                    no_slot_x_offset += 40
                    no_slot_y_offset = 0

            item_sprite.x = pos_x
            item_sprite.y = pos_y
            item_sprite.draw()

            self.handle_card_hover(item, item_sprite)

            self.equipped_card_sprites.append((item_sprite, item))

    def _draw_hand(self, player, x, y):
        # Dimensões para cartas na mão do jogador atual
        HAND_CARD_WIDTH = 90
        HAND_CARD_HEIGHT = 135

        HAND_CARD_SPACING = HAND_CARD_WIDTH - 20

        self.hand_card_sprites = []

        hand_cards_y = 610
        for i, card in enumerate(player.hand):
            try:
                card_sprite = Sprite(card.image)
                card_sprite.resize(HAND_CARD_WIDTH, HAND_CARD_HEIGHT)

                card_x = x + (i * HAND_CARD_SPACING)
                card_y = hand_cards_y
                card_sprite.x = card_x
                card_sprite.y = card_y
                card_sprite.draw()

                self.handle_card_hover(card, card_sprite)

                self.hand_card_sprites.append((card_sprite, card))

            except Exception as e:
                print(f"Error drawing hand card: {e}")
                raise e

    def _draw_combat(self, combat, x, y):
        font = pygame.font.Font(None, 36)
        monster = combat.monster

        # Desenhar imagem do monstro
        MONSTER_WIDTH = 200
        MONSTER_HEIGHT = 300
        monster_sprite = Sprite(monster.image)
        resized_image = pygame.transform.scale(monster_sprite.image, (MONSTER_WIDTH, MONSTER_HEIGHT))
        monster_sprite.image = resized_image
        monster_sprite.x = x  # Centralizar na área de combate
        monster_sprite.y = y
        monster_sprite.draw()

        # Combat title
        title = font.render(f"{monster.name} | Level {monster.level}", True, WHITE)
        self.screen.blit(title, (x + MONSTER_WIDTH + 20, y + 20))

        # Estatísticas de combate
        player_strength = combat.get_player_strength()
        monster_strength = combat.get_monster_strength()

        # Desenhar VS e forças
        large_font = pygame.font.Font(None, 60)
        vs_text = large_font.render("VS", True, WHITE)
        player_text = large_font.render(str(player_strength), True,
                                        GREEN if player_strength > monster_strength else WHITE)
        monster_text = large_font.render(str(monster_strength), True,
                                         RED if player_strength > monster_strength else WHITE)

        # Posicionar textos
        self.screen.blit(vs_text, (x + MONSTER_WIDTH + 100, y + 100))
        self.screen.blit(player_text, (x + MONSTER_WIDTH + 30, y + 100))
        self.screen.blit(monster_text, (x + MONSTER_WIDTH + 210, y + 100))

        # Informações adicionais
        details = [
            f"Tesouro: {monster.treasure}",
            f"Ajudantes: {len(combat.helpers)}",
        ]

        bad_stuff_lines = str(monster.bad_stuff).split('\n')
        if bad_stuff_lines:
            details.append(f"Coisa Ruim: {bad_stuff_lines[0]}")
        for line in bad_stuff_lines[1:]:
            details.append(f"                  {line}")

        for i, text in enumerate(details):
            surface = font.render(text, True, WHITE)
            self.screen.blit(surface, (x + MONSTER_WIDTH + 20, 400 + i * 30))

    def _draw_buttons(self, game_state):
        current_phase_buttons = BUTTONS_BY_GAME_PHASE[game_state.phase]

        for button_name, button in self.buttons.items():
            # Verifica se o botão é relevante para a fase atual do jogo
            if button_name not in current_phase_buttons:
                button.deactivate()
                continue

            # Caso seja a fase de combate, verifica as condições específicas
            if game_state.phase == GamePhase.COMBAT:
                combat_state = game_state.current_combat.get_combat_state()
                combat_buttons = COMBAT_CONDITIONS.get(combat_state, [])

                if button_name in combat_buttons:
                    button.activate()
                    button.draw()
                else:
                    button.deactivate()
            else:
                # Para fases que não são de combate
                button.activate()
                button.draw()

    def set_message(self, message):
        self.message = message
        self.message_timer = 120  # Show message for 2 seconds (60 FPS)
        
    def _draw_message(self):
        if self.message and self.message_timer > 0:
            font = pygame.font.Font(None, 32)
            text = font.render(self.message, True, BLACK)
            text_rect = text.get_rect(center=(850, 585))
            pygame.draw.rect(self.screen, WHITE, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))
            self.screen.blit(text, text_rect)
            self.message_timer -= 1

    def handle_event(self, event, game_state=None):
        equipable_card_types = [CardType.CLASS, CardType.ITEM]
        # Handle button clicks
        for button_name, button in self.buttons.items():
            if button.handle_event():
                return button_name

        # Handle card clicks
        if game_state and event.type == pygame.MOUSEBUTTONDOWN:
            # Check for clicks on any cards
            for card_sprite, card in self.hand_card_sprites:
                if self.mouse.is_over_object(card_sprite) and card.type in equipable_card_types:
                    self._remove_item_sprite(self.hand_card_sprites, card_sprite)
                    return 'equip_item', card

            for card_sprite, card in self.equipped_card_sprites:
                if self.mouse.is_over_object(card_sprite):
                    self._remove_item_sprite(self.equipped_card_sprites, card_sprite)
                    return 'unequip_item', card
        return None

    def _draw_zoomed_card(self, card_size=None, zoomed_position=None):
        zoomed_card_width = card_size[0] if card_size else 270
        zoomed_card_height = card_size[1] if card_size else 395
        zoomed_card_x = zoomed_position[0] if zoomed_position else (SCREEN_WIDTH + 402)/2 - zoomed_card_width/2
        zoomed_card_y = zoomed_position[1] if zoomed_position else SCREEN_HEIGHT/2 - zoomed_card_height/2
        if self.zoomed_card:
            zoomed_sprite = Sprite(self.zoomed_card)
            zoomed_sprite.resize(zoomed_card_width, zoomed_card_height)
            zoomed_sprite.set_position(zoomed_card_x, zoomed_card_y)
            zoomed_sprite.draw()

    def _set_zoomed_card(self, card_sprite):
        self.zoomed_card = card_sprite

    def _hide_zoomed_card(self):
        self.zoomed_card = None

    def _draw_decks_info(self, game_state):
        font = pygame.font.Font(None, 50)

        # quantidades de cartas
        treasure_deck_amount = len(game_state.treasure_deck.cards)
        discard_treasure_deck_amount = len(game_state.treasure_deck.discard_pile)
        door_deck_amount = len(game_state.door_deck.cards)
        discard_door_deck_amount = len(game_state.door_deck.discard_pile)

        # posições
        treasure_deck_x = 50
        treasure_deck_y = 25
        treasure_discard_x = treasure_deck_x
        treasure_discard_y = treasure_deck_y + 120
        door_deck_x = 305
        door_deck_y = 240
        door_discard_x = door_deck_x
        door_discard_y = door_deck_y + 120

        # texto
        treasure_text = font.render(str(treasure_deck_amount), True, WHITE)
        treasure_discard_text = font.render(str(discard_treasure_deck_amount), True, WHITE)
        door_text = font.render(str(door_deck_amount), True, WHITE)
        door_discard_text = font.render(str(discard_door_deck_amount), True, WHITE)

        # draw text
        self.screen.blit(treasure_text, (treasure_deck_x, treasure_deck_y))
        self.screen.blit(treasure_discard_text, (treasure_discard_x, treasure_discard_y))
        self.screen.blit(door_text, (door_deck_x, door_deck_y))
        self.screen.blit(door_discard_text, (door_discard_x, door_discard_y))

    def handle_card_hover(self, card, card_sprite, card_size=None, zoomed_position=None):
        if self.mouse.is_over_object(card_sprite):
            self._set_zoomed_card(card.image)
            self._draw_zoomed_card(card_size=card_size, zoomed_position=zoomed_position)
        elif self.zoomed_card == card_sprite:
            self._hide_zoomed_card()

    def _remove_item_sprite(self, origin, sprite):
        for idx, sprite_tuple in enumerate(origin):
            if sprite_tuple[0] == sprite:
                origin.remove(sprite_tuple)

    def display_selection_modal(self, cards, title, background=None):
        """Mostra modal generalizado"""
        MODAL_WIDTH = 800
        MODAL_HEIGHT = 600
        CARD_WIDTH = 90
        CARD_HEIGHT = 135
        ZOOMED_CARD_SIZE = (216, 316)
        ZOOMED_CARD_POS = (535, 160)
        SPACING = - 20

        # Usar o screen do renderer existente
        screen = self.screen

        # Posicionamento central na tela
        modal_x = (screen.get_width() - MODAL_WIDTH) // 2
        modal_y = (screen.get_height() - MODAL_HEIGHT) // 2

        # Criar superfície do modal
        modal_surface = pygame.Surface((MODAL_WIDTH, MODAL_HEIGHT))
        modal_surface.set_alpha(230)
        if background:
            background_image = pygame.image.load(background)
            modal_surface.blit(background_image, (0, 0))
        else:
            modal_surface.fill((255, 255, 255))

        # Título
        big_font = pygame.font.Font(None, 36)
        title = big_font.render(title, True, (0, 0, 0))
        title_rect = title.get_rect(centerx=MODAL_WIDTH // 2, y=20)

        # Fechar
        lower_font = pygame.font.Font(None, 24)
        close = lower_font.render("(Pressione ESC para fechar)", True, (0, 0, 0))
        close_rect = close.get_rect(centerx=MODAL_WIDTH // 2, y=50)

        # Posições dos cards
        cards_start_x = (MODAL_WIDTH - (len(cards) * (CARD_WIDTH + SPACING))) // 2
        cards_y = 510

        card_sprites = []
        for i, card in enumerate(cards):
            card_sprite = Sprite(card.image)
            card_sprite.resize(CARD_WIDTH, CARD_HEIGHT)

            card_x = modal_x + cards_start_x + (i * (CARD_WIDTH + SPACING))
            card_y = cards_y
            card_sprite.x = card_x
            card_sprite.y = card_y

            card_sprites.append((card_sprite, card))

        running = True
        while running:
            # Desenha o modal
            screen.blit(modal_surface, (modal_x, modal_y))
            screen.blit(title, (modal_x + title_rect.x, modal_y + title_rect.y))
            screen.blit(close, (modal_x + close_rect.x, modal_y + close_rect.y))

            # Desenha os cards
            for card_sprite, card in card_sprites:
                card_sprite.draw()

                self.handle_card_hover(card, card_sprite, card_size=ZOOMED_CARD_SIZE,
                                       zoomed_position=ZOOMED_CARD_POS)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for card_sprite, card in card_sprites[::-1]:
                        if self.mouse.is_over_object(card_sprite):
                            return card

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break

                if event.type == pygame.QUIT:
                    running = False
                    break

            pygame.display.flip()

        return None

    def display_multi_selection_modal(self, cards, title, btn_image, background=None):
        """Mostra modal multi-select generalizado"""
        MODAL_WIDTH = 800
        MODAL_HEIGHT = 600
        CARD_WIDTH = 90
        CARD_HEIGHT = 135
        ZOOMED_CARD_SIZE = (216, 316)
        ZOOMED_CARD_POS = (535, 160)
        SPACING = - 20

        # Usar o screen do renderer existente
        screen = self.screen

        # Posicionamento central na tela
        modal_x = (screen.get_width() - MODAL_WIDTH) // 2
        modal_y = (screen.get_height() - MODAL_HEIGHT) // 2

        # Criar superfície do modal
        modal_surface = pygame.Surface((MODAL_WIDTH, MODAL_HEIGHT))
        modal_surface.set_alpha(230)
        if background:
            background_image = pygame.image.load(background)
            modal_surface.blit(background_image, (0, 0))
        else:
            modal_surface.fill((255, 255, 255))

        # Título
        big_font = pygame.font.Font(None, 36)
        title = big_font.render(title, True, (0, 0, 0))
        title_rect = title.get_rect(centerx=MODAL_WIDTH // 2, y=20)

        # Fechar
        lower_font = pygame.font.Font(None, 24)
        close = lower_font.render("(Pressione ESC para fechar)", True, (0, 0, 0))
        close_rect = close.get_rect(centerx=MODAL_WIDTH // 2, y=50)

        # Posições dos cards
        cards_start_x = (MODAL_WIDTH - (len(cards) * (CARD_WIDTH + SPACING))) // 2
        cards_y = 510

        card_sprites = []
        for i, card in enumerate(cards):
            card_sprite = Sprite(card.image)
            card_sprite.resize(CARD_WIDTH, CARD_HEIGHT)

            card_x = modal_x + cards_start_x + (i * (CARD_WIDTH + SPACING))
            card_y = cards_y
            card_sprite.x = card_x
            card_sprite.y = card_y

            card_sprites.append((card_sprite, card))

        selected_cards = []

        confirm_btn = HoverButton(btn_image, MODAL_WIDTH + 100, MODAL_HEIGHT - 200, 160, 66)

        running = True
        while running:
            # Desenha o modal
            screen.blit(modal_surface, (modal_x, modal_y))
            screen.blit(title, (modal_x + title_rect.x, modal_y + title_rect.y))
            screen.blit(close, (modal_x + close_rect.x, modal_y + close_rect.y))

            # Desenha os cards
            for card_sprite, card in card_sprites:
                card_sprite.draw()
                if card in selected_cards:
                    pygame.draw.rect(
                        self.screen,
                        (0, 255, 0),
                        (card_sprite.rect.x - 5, card_sprite.rect.y - 5,
                         card_sprite.rect.width + 10, card_sprite.rect.height + 10),
                        3
                    )
                self.handle_card_hover(card, card_sprite, card_size=ZOOMED_CARD_SIZE,
                                       zoomed_position=ZOOMED_CARD_POS)
                confirm_btn.draw()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for card_sprite, card in card_sprites[::-1]:
                        if self.mouse.is_over_object(card_sprite):
                            if card in selected_cards:
                                selected_cards.remove(card)
                            else:
                                selected_cards.append(card)
                            break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break

                if event.type == pygame.QUIT:
                    running = False
                    break

                if confirm_btn.handle_event():
                    return selected_cards

            pygame.display.flip()

        return None
