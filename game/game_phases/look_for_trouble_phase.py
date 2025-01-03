import pygame
from game.card import CardType, Monster
from game.combat import Combat
from game.game_phases.game_phases import GamePhases
from game.game_state import GamePhase
from constants import WHITE


class LookForTroublePhase(GamePhases):
    def __init__(self, game_state, renderer):
        super().__init__(game_state)
        self.current_player = game_state.current_player()
        self.renderer = renderer

    def get_monsters_from_hand(self):
        """Retorna lista de monstros na mão do jogador atual"""
        return [card for card in self.current_player.hand
                if isinstance(card, Monster)]

    def run(self):
        print("Entering LookForTroublePhase...")
        self.game_state.set_game_phase(GamePhase.LOOK_FOR_TROUBLE)

        available_monsters = self.get_monsters_from_hand()

        if not available_monsters:
            print("No monsters in hand. Player must loot the room instead.")
            self.game_state.set_game_phase(GamePhase.KICK_DOOR)
            return False

        selected_monster = self.show_monster_selection_modal(available_monsters)

        if selected_monster:
            self.current_player.hand.remove(selected_monster)
            combat = Combat(self.current_player, selected_monster)
            self.game_state.set_combat(combat)
            self.game_state.set_game_phase(GamePhase.COMBAT)
            self.renderer.set_message(f"Combat started with {selected_monster.name}")
            return True

        return False

    def show_monster_selection_modal(self, available_monsters):
        """Mostra modal para seleção de monstros"""
        MODAL_WIDTH = 800
        MODAL_HEIGHT = 600
        CARD_WIDTH = 120
        CARD_HEIGHT = 180
        SPACING = 20

        # Usar o screen do renderer existente
        screen = self.renderer.screen

        # Posicionamento central na tela
        modal_x = (screen.get_width() - MODAL_WIDTH) // 2
        modal_y = (screen.get_height() - MODAL_HEIGHT) // 2

        # Criar superfície do modal
        modal_surface = pygame.Surface((MODAL_WIDTH, MODAL_HEIGHT))
        modal_surface.set_alpha(230)
        modal_surface.fill(WHITE)

        # Título
        font = pygame.font.Font(None, 36)
        title = font.render("Select a Monster to Fight", True, (0, 0, 0))
        title_rect = title.get_rect(centerx=MODAL_WIDTH // 2, y=20)

        # Posições dos cards
        cards_start_x = (MODAL_WIDTH - (len(available_monsters) * (CARD_WIDTH + SPACING))) // 2
        cards_y = 100

        running = True
        while running:
            # Desenha o modal
            screen.blit(modal_surface, (modal_x, modal_y))
            screen.blit(title, (modal_x + title_rect.x, modal_y + title_rect.y))

            # Desenha os cards dos monstros
            for i, monster in enumerate(available_monsters):
                card_x = modal_x + cards_start_x + (i * (CARD_WIDTH + SPACING))
                card_rect = pygame.Rect(card_x, modal_y + cards_y, CARD_WIDTH, CARD_HEIGHT)

                # Usar o método de renderização de cards existente
                monster_sprite = pygame.image.load(monster.image)
                monster_sprite = pygame.transform.scale(monster_sprite, (CARD_WIDTH, CARD_HEIGHT))
                screen.blit(monster_sprite, card_rect)

                # Nome do monstro
                monster_name = font.render(monster.name, True, (0, 0, 0))
                name_rect = monster_name.get_rect(centerx=card_rect.centerx,
                                                  top=card_rect.bottom + 10)
                screen.blit(monster_name, name_rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, monster in enumerate(available_monsters):
                        card_x = modal_x + cards_start_x + (i * (CARD_WIDTH + SPACING))
                        card_rect = pygame.Rect(card_x, modal_y + cards_y, CARD_WIDTH, CARD_HEIGHT)
                        if card_rect.collidepoint(mouse_pos):
                            return monster

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break

                if event.type == pygame.QUIT:
                    running = False
                    break

            pygame.display.flip()

        return None