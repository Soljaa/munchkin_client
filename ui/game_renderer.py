import pygame
from PPlay.sprite import *
from constants import *
from game.card import Item
from ui.button import Button
from game.dice import Dice
from game.game_state import GamePhase


BUTTONS_BY_GAME_PHASE = {
    GamePhase.SETUP: ["kick_door"],
    GamePhase.KICK_DOOR: ["look_for_trouble", "loot"],
    GamePhase.LOOK_FOR_TROUBLE: [],
    GamePhase.LOOT_ROOM: [],
    GamePhase.COMBAT: ["run_away", "use_card", "ask_for_help", "finish_combat"],
    GamePhase.CHARITY: [],
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
            "kick_door": Button(420, button_y, 200, 50, "Kick Down Door", GREEN, (100, 255, 100)),
            "use_card": Button(420, button_y - 60, 200, 50, "Use item card", GREEN, (100, 255, 100)),
            "run_away": Button(640, button_y, 200, 50, "Run Away", RED, (255, 100, 100)),
            "look_for_trouble": Button(860, button_y, 200, 50, "Trouble", BLUE, (100, 100, 255)),
            "ask_for_help": Button(860, button_y - 60, 200, 50, "Ask for help", BLUE, (100, 100, 255)),
            "loot": Button(1080, button_y, 200, 50, "Loot", BLUE, (100, 100, 255)),
            "finish_combat": Button(1080, button_y, 200, 50, "Finish Combat", BLUE, (100, 100, 255))
        }

    def draw_gameboard(self):
        self.screen.blit(self.gameboard, (0, 0)) #Minimapa
        pygame.draw.rect(self.screen, BROWN, (402, 0, 5, 720))

    def draw_dungeon_background(self):
        self.screen.blit(self.dungeon_background, (402, 0))

    def draw_avatars(self, players):
        # Configuração de posição inicial e incrementos para cada nível dos avatares
        level_positions = {
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
        roll_time_seconds = 4  # Tempo total de animação do dado rolando em segundos
        elapsed_time = 0  # Variável para controlar o tempo de animação
        
        clock = pygame.time.Clock()
        
        while elapsed_time < roll_time_seconds:
            # Calcula o tempo entre quadros
            delta_time = clock.tick(60) / 1000.0  # 60 FPS

            elapsed_time += delta_time  # Atualiza o tempo decorrido
            dice.draw_rolling_dice(SCREEN_WIDTH/2-dice.sprite_rolling_dice.width/2, SCREEN_HEIGHT/2-dice.sprite_rolling_dice.height/2, self.draw_dungeon_background, self.draw_gameboard) # Animação do rolamento do dado

            self.draw_dungeon_background()
            self.draw_gameboard()

        dice.draw_value_dice(SCREEN_WIDTH/2-dice.sprite_value_dice.width/2, SCREEN_HEIGHT/2-dice.sprite_value_dice.height/2)
        time.sleep(1)

    def draw_game_state(self, game_state):
        # Draw current player info
        player = game_state.current_player()
        players = game_state.players
        self._draw_player_info(player, 420, 50)

        # Draw avatars
        self.draw_avatars(players)

        # Draw phase indicator at the top
        self._draw_phase_indicator(game_state.phase, SCREEN_WIDTH // 2 + 50, 20)
        
        # Draw hand
        self._draw_hand(player, 420, 200)
        
        # Draw current combat if any
        if game_state.current_combat:
            self._draw_combat(game_state.current_combat, 800, 300)
        
        # Draw buttons based on game phase
        self._draw_buttons(game_state.phase)
        
        # Draw message if any
        self._draw_message()

    def _draw_phase_indicator(self, phase, x, y):
        font = pygame.font.Font(None, 32)
        phase_text = f"Current Phase: {phase.name.replace('_', ' ')}"
        surface = font.render(phase_text, True, BLUE)
        pygame.draw.rect(self.screen, WHITE, (x - 5, y - 5, surface.get_width() + 10, surface.get_height() + 10))
        pygame.draw.rect(self.screen, GRAY, (x - 5, y - 5, surface.get_width() + 10, surface.get_height() + 10), 2)
        self.screen.blit(surface, (x, y))

    def _draw_player_info(self, player, x, y):
        font = pygame.font.Font(None, 36)
        texts = [
            f"Player: {player.name}",
            f"Level: {player.level}",
            f"Combat Strength: {player.calculate_combat_strength()}"
        ]
        
        for i, text in enumerate(texts):
            surface = font.render(text, True, BLACK)
            self.screen.blit(surface, (x, y + i * 30))

    def _draw_hand(self, player, x, y):
        font = pygame.font.Font(None, 24)
        # Draw hand title
        title = font.render("Your Hand:", True, BLACK)
        self.screen.blit(title, (x, y))
        
        # Draw cards in hand
        for i, card in enumerate(player.hand):
            card_text = f"{card.name}"
            if hasattr(card, 'bonus') and card.bonus:
                card_text += f" (+{card.bonus})"
            color = GREEN if isinstance(card, Item) and not card.equipped else BLACK
            surface = font.render(card_text, True, color)
            self.screen.blit(surface, (x + 10, y + 30 + i * 25))
            
        # Draw equipped items section
        equipped_y = y + 30 + len(player.hand) * 25 + 20
        equipped_title = font.render("Equipped Items:", True, BLACK)
        self.screen.blit(equipped_title, (x, equipped_y))
        
        for i, item in enumerate(player.equipped_items):
            item_text = f"{item.name} (+{item.bonus})"
            surface = font.render(item_text, True, BLUE)
            self.screen.blit(surface, (x + 10, equipped_y + 30 + i * 25))

    def _draw_combat(self, combat, x, y):
        font = pygame.font.Font(None, 36)
        monster = combat.monster
        
        # Draw combat box background with border
        pygame.draw.rect(self.screen, BLACK, (x - 15, y - 15, 410, 250))
        pygame.draw.rect(self.screen, RED, (x - 10, y - 10, 400, 240))
        
        # Combat title with monster level
        title = font.render(f"COMBAT: Level {monster.level} {monster.name}", True, WHITE)
        self.screen.blit(title, (x, y))
        
        # Combat stats
        player_strength = combat.get_player_strength()
        monster_strength = combat.get_monster_strength()
        
        # Draw VS graphic
        vs_font = pygame.font.Font(None, 48)
        vs_text = vs_font.render("VS", True, WHITE)
        vs_rect = vs_text.get_rect(center=(x + 200, y + 80))
        self.screen.blit(vs_text, vs_rect)
        
        # Draw player and monster strength in larger font
        large_font = pygame.font.Font(None, 60)
        player_text = large_font.render(str(player_strength), True, GREEN if player_strength > monster_strength else WHITE)
        monster_text = large_font.render(str(monster_strength), True, RED if player_strength > monster_strength else WHITE)
        
        self.screen.blit(player_text, (x + 150, y + 60))
        self.screen.blit(monster_text, (x + 250, y + 60))
        
        # Draw combat details
        details = [
            f"Helpers: {len(combat.helpers)}",
            f"Treasure Reward: {monster.treasure}",
            f"Bad Stuff: {monster.bad_stuff}"
        ]
        
        for i, text in enumerate(details):
            surface = font.render(text, True, WHITE)
            self.screen.blit(surface, (x, y + 120 + i * 30))
        
        # Draw helper info if any
        if combat.helpers:
            helper_text = font.render("Helper Combat Power:", True, WHITE)
            self.screen.blit(helper_text, (x, y + 180))
            for i, helper in enumerate(combat.helpers):
                power = helper.calculate_combat_strength()
                helper_power = font.render(f"{helper.name}: +{power}", True, GREEN)
                self.screen.blit(helper_power, (x + 20, y + 210 + i * 25))

    def _draw_buttons(self, game_phase):
        for button_name, button_rect in self.buttons.items():
            if button_name in BUTTONS_BY_GAME_PHASE[game_phase]:
                button_rect.activate()
                button_rect.draw(self.screen)
            else:
                button_rect.deactivate()

    def set_message(self, message):
        self.message = message
        self.message_timer = 120  # Show message for 2 seconds (60 FPS)
        
    def _draw_message(self):
        if self.message and self.message_timer > 0:
            font = pygame.font.Font(None, 32)
            text = font.render(self.message, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT-25))
            pygame.draw.rect(self.screen, WHITE, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))
            self.screen.blit(text, text_rect)
            self.message_timer -= 1

    def handle_event(self, event, game_state=None):
        # Handle button clicks
        for button_name, button in self.buttons.items():
            if button.handle_event(event):
                return button_name
        
        # Handle card clicks if game_state is provided
        if game_state and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            current_player = game_state.current_player()
            
            # Check for clicks in the hand area
            x, y = 420, 200  # Starting position of hand cards
            for i, card in enumerate(current_player.hand):
                card_rect = pygame.Rect(x + 10, y + 30 + i * 25, 200, 20)
                if card_rect.collidepoint(mouse_pos):
                    if isinstance(card, Item):
                        return ("equip_item", i)
            
            # Check for clicks in equipped items area
            equipped_y = y + 30 + len(current_player.hand) * 25 + 20
            for i, item in enumerate(current_player.equipped_items):
                card_rect = pygame.Rect(x + 10, equipped_y + 30 + i * 25, 200, 20)
                if card_rect.collidepoint(mouse_pos):
                    return ("unequip_item", i)
        
        return None
