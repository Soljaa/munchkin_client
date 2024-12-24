import pygame
from constants import *
from game.card import Item
from ui.button import Button

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
            "kick_door": Button(500, button_y, 200, 50, "Kick Down Door", GREEN, (100, 255, 100)),
            "run_away": Button(750, button_y, 200, 50, "Run Away", RED, (255, 100, 100)),
            "end_turn": Button(1000, button_y, 200, 50, "End Turn", BLUE, (100, 100, 255))
        }

    def draw_gameboard(self):
        self.screen.blit(self.gameboard, (0, 0))

    def draw_dungeon_background(self):
        self.screen.blit(self.dungeon_background, (402, 0))


    def draw_game_state(self, game_state):
        # Draw current player info
        player = game_state.current_player()
        self._draw_player_info(player, 420, 50)
        
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
        for button in self.buttons.values():
            button.draw(self.screen)

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
