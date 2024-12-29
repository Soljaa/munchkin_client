import pygame
from PPlay.sprite import *
from constants import *
from game.card import Item
from ui.hover_button import HoverButton
from game.dice import Dice
from game.game_state import GamePhase
from game.combat import CombatStates


BUTTONS_BY_GAME_PHASE = {
    GamePhase.SETUP: ["kick_door"],
    GamePhase.KICK_DOOR: ["look_for_trouble", "loot"],
    GamePhase.LOOK_FOR_TROUBLE: [],
    GamePhase.LOOT_ROOM: [],
    GamePhase.COMBAT: ["run_away", "use_card", "ask_for_help", "finish_combat"],
    GamePhase.CHARITY: [],
}

COMBAT_CONDITIONS = {
    CombatStates.WINNING: ["use_card", "finish_combat"],
    CombatStates.LOSING: ["run_away", "use_card", "ask_for_help"]
}


class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.gameboard = pygame.image.load("assets/gameboard.png")
        self.dungeon_background = pygame.image.load("assets/dungeon_background.png")
        self.buttons = {}
        self.message = ""
        self.message_timer = 0
        self._init_buttons()

    def _init_buttons(self):
        # Create buttons with consistent positioning
        button_y = SCREEN_HEIGHT - 100
        self.buttons = {
            "kick_door": HoverButton("assets/game/kick_door_new.png", 1010, 10, 250, 200),
            "use_card": HoverButton("assets/game/use_card.png", 1060, 10, 210, 60),
            "run_away": HoverButton("assets/game/run_away.png", 840, 80, 210, 60),
            "look_for_trouble": HoverButton("assets/game/look_for_trouble.png", 840, button_y, 210, 60),
            "ask_for_help": HoverButton("assets/game/ask_for_help.png", 840, 10, 210, 60),
            "loot": HoverButton("assets/game/loot.png", 1060, button_y, 210, 60),
            "finish_combat": HoverButton("assets/game/finish_combat.png", 1060, 80, 210, 60),
        }

    def draw_gameboard(self):
        self.screen.blit(self.gameboard, (0, 0)) #Minimapa
        pygame.draw.rect(self.screen, BROWN, (402, 0, 5, 720))

    def draw_dungeon_background(self):
        self.screen.blit(self.dungeon_background, (402, 0))

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
        
    def draw_game_state(self, game_state):
        # Draw current player info
        player = game_state.current_player()
        players = game_state.players
        self._draw_player_info(player, 430, 10)

        # Draw avatars
        self.draw_avatars(players)

        # Draw phase indicator at the top
        self._draw_phase_indicator(game_state.phase, 570, 105)
        
        # Draw hand
        self._draw_hand(player, 430, 230)
        
        # Draw current combat if any
        if game_state.current_combat:
            self._draw_combat(game_state.current_combat, 750, 200)
        
        # Draw buttons based on game phase
        self._draw_buttons(game_state)
        
        # Draw message if any
        self._draw_message()

    def _draw_phase_indicator(self, phase, x, y):
        font = pygame.font.Font(None, 32)
        phase_text = f"Phase: {phase.name.replace('_', ' ')}"
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
        font = pygame.font.Font(None, 36)
        texts = [
            f"Player: {player.name}",
            f"Level: {player.level}",
            f"Strength: {player.calculate_combat_strength()}"
        ]

        text_x = x + new_width + 20
        for i, text in enumerate(texts):
            surface = font.render(text, True, WHITE)
            self.screen.blit(surface, (text_x, y + i * 30))

    def _draw_hand(self, player, x, y):
        font = pygame.font.Font(None, 24)
        CARD_WIDTH = 120  # Increased for better clickability
        CARD_HEIGHT = 36
        CARD_SPACING = 140  # Increased to prevent overlapping

        # Store card positions for click detection
        self.card_positions = []  # Add this as instance variable in __init__

        # Equipped Items Section
        slots = {
            "head": {"title": "Head:", "items": [], "y_offset": 0},
            "armor": {"title": "Armor:", "items": [], "y_offset": CARD_HEIGHT + 60},
            "hands": {"title": "Hands:", "items": [], "y_offset": 2 * (CARD_HEIGHT + 60)},
            "feet": {"title": "Feet:", "items": [], "y_offset": 3 * (CARD_HEIGHT + 60)},
        }

        # Organize items by slots
        for item in player.equipped_items:
            if item.slot in slots:
                slots[item.slot]["items"].append(item)

        # Draw items by slot and store equipped item positions
        for slot_info in slots.values():
            slot_title = font.render(slot_info["title"], True, WHITE)
            slot_y = y + slot_info["y_offset"]
            self.screen.blit(slot_title, (x, slot_y - 25))

            for i, item in enumerate(slot_info["items"]):
                item_sprite = Sprite(item.image)
                resized_image = pygame.transform.scale(item_sprite.image, (CARD_WIDTH, CARD_HEIGHT))
                item_sprite.image = resized_image

                item_x = x + (i * CARD_SPACING)
                item_y = slot_y
                item_sprite.x = item_x
                item_sprite.y = item_y
                item_sprite.draw()

                # Store equipped item position and data
                self.card_positions.append({
                    'rect': pygame.Rect(item_x, item_y, CARD_WIDTH, CARD_HEIGHT),
                    'type': 'equipped',
                    'index': len(self.card_positions),
                    'item': item
                })

                bonus_text = font.render(f"+{item.bonus}", True, WHITE)
                self.screen.blit(bonus_text, (item_x + 5, item_y + CARD_HEIGHT + 5))

        # Draw hand cards
        hand_y = y + 4 * (CARD_HEIGHT + 60)
        hand_title = font.render("Your Hand:", True, WHITE)
        self.screen.blit(hand_title, (x, hand_y))

        hand_cards_y = hand_y + 30
        for i, card in enumerate(player.hand):
            card_sprite = Sprite(card.image)
            resized_image = pygame.transform.scale(card_sprite.image, (CARD_WIDTH, CARD_HEIGHT))
            card_sprite.image = resized_image

            card_x = x + (i * CARD_SPACING)
            card_y = hand_cards_y
            card_sprite.x = card_x
            card_sprite.y = card_y
            card_sprite.draw()

            # Store hand card position and data
            if isinstance(card, Item):
                self.card_positions.append({
                    'rect': pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT),
                    'type': 'hand',
                    'index': i,
                    'item': card
                })

            if hasattr(card, 'bonus') and card.bonus:
                bonus_text = font.render(f"+{card.bonus}", True,
                                         GREEN if isinstance(card, Item) and not card.equipped else WHITE)
                self.screen.blit(bonus_text, (card_x + 5, card_y + CARD_HEIGHT + 5))

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
            f"Treasure: {monster.treasure}",
            f"Bad Stuff: {monster.bad_stuff}",
            f"Helpers: {len(combat.helpers)}"
        ]

        for i, text in enumerate(details):
            surface = font.render(text, True, WHITE)
            self.screen.blit(surface, (x + MONSTER_WIDTH + 20, 400 + i * 30))

    def _draw_buttons(self, game_state):
        current_phase_buttons = BUTTONS_BY_GAME_PHASE[game_state.phase]

        for button_name, button_rect in self.buttons.items():
            # Verifica se o botão é relevante para a fase atual do jogo
            if button_name not in current_phase_buttons:
                button_rect.deactivate()
                continue

            # Caso seja a fase de combate, verifica as condições específicas
            if game_state.phase == GamePhase.COMBAT:
                combat_state = game_state.current_combat.get_combat_state()
                combat_buttons = COMBAT_CONDITIONS.get(combat_state, [])

                if button_name in combat_buttons:
                    button_rect.activate()
                    button_rect.draw(self.screen)
                else:
                    button_rect.deactivate()
            else:
                # Para fases que não são de combate
                button_rect.activate()
                button_rect.draw(self.screen)

    def set_message(self, message):
        self.message = message
        self.message_timer = 120  # Show message for 2 seconds (60 FPS)
        
    def _draw_message(self):
        if self.message and self.message_timer > 0:
            font = pygame.font.Font(None, 32)
            text = font.render(self.message, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 200))
            pygame.draw.rect(self.screen, WHITE, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))
            self.screen.blit(text, text_rect)
            self.message_timer -= 1

    def handle_event(self, event, game_state=None):
        # Handle button clicks
        for button_name, button in self.buttons.items():
            if button.handle_event(event):
                return button_name

        # Handle card clicks
        if game_state and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Check for clicks on any stored card positions
            for card_data in self.card_positions:
                if card_data['rect'].collidepoint(mouse_pos):
                    if card_data['type'] == 'hand' and isinstance(card_data['item'], Item):
                        return ('equip_item', card_data['index'])
                    elif card_data['type'] == 'equipped':
                        return ('unequip_item', card_data['index'])

        return None
