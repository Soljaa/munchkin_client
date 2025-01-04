from game.game_phases.game_phases import GamePhases
import pygame


class SetupPhase(GamePhases):
    def __init__(self, game_state, action, renderer):
        super().__init__(game_state)
        self.player = game_state.current_player()
        self.action_type = action[0]
        self.item = action[1]
        self.renderer = renderer

    def run(self):
        print(f"Changing items: {self.game_state.phase}")

        if self.action_type == "equip_item":
            card = self.item
            if card in self.player.hand:
                item_equipped = self.player.equip_item(card)
                if item_equipped:
                    self.renderer.set_message(f"Equipped {card.name}!")
                else:
                    self.renderer.set_message("Cannot equip this item!")

        elif self.action_type == "unequip_item":
            item = self.item
            if item in self.player.equipped_items:
                self.player.unequip_item(item)
                self.renderer.set_message(f"Unequipped {item.name}")

        elif self.action_type == "sell_items":
            self.show_sell_items_modal()

        return True

    def show_sell_items_modal(self):
        """Mostra modal para seleção de itens para venda"""
        MODAL_WIDTH = 800
        MODAL_HEIGHT = 600
        CARD_WIDTH = 120
        CARD_HEIGHT = 180
        SPACING = 20

        screen = self.renderer.screen
        modal_x = (screen.get_width() - MODAL_WIDTH) // 2
        modal_y = (screen.get_height() - MODAL_HEIGHT) // 2

        modal_surface = pygame.Surface((MODAL_WIDTH, MODAL_HEIGHT))
        modal_surface.set_alpha(230)
        modal_surface.fill((255, 255, 255))

        font = pygame.font.Font(None, 36)
        title = font.render("Select Items to Sell", True, (0, 0, 0))
        title_rect = title.get_rect(centerx=MODAL_WIDTH // 2, y=20)

        available_items = [card for card in self.player.hand if hasattr(card, 'value') and card.value is not None]
        selected_items = []

        cards_start_x = (MODAL_WIDTH - (len(available_items) * (CARD_WIDTH + SPACING))) // 2
        cards_y = 100

        sell_button = pygame.Rect(MODAL_WIDTH // 2 - 50, MODAL_HEIGHT - 60, 100, 40)

        running = True
        while running:
            screen.blit(modal_surface, (modal_x, modal_y))
            screen.blit(title, (modal_x + title_rect.x, modal_y + title_rect.y))

            # Desenha os cards dos itens
            for i, item in enumerate(available_items):
                card_x = modal_x + cards_start_x + (i * (CARD_WIDTH + SPACING))
                card_rect = pygame.Rect(card_x, modal_y + cards_y, CARD_WIDTH, CARD_HEIGHT)

                # Destacar itens selecionados
                if item in selected_items:
                    pygame.draw.rect(screen, (255, 255, 0), card_rect, 3)

                item_sprite = pygame.image.load(item.image)
                item_sprite = pygame.transform.scale(item_sprite, (CARD_WIDTH, CARD_HEIGHT))
                screen.blit(item_sprite, card_rect)

                item_name = font.render(item.name, True, (0, 0, 0))
                name_rect = item_name.get_rect(centerx=card_rect.centerx, top=card_rect.bottom + 10)
                screen.blit(item_name, name_rect)

                value_text = font.render(f"Value: {item.value}", True, (0, 0, 0))
                value_rect = value_text.get_rect(centerx=card_rect.centerx, top=name_rect.bottom + 5)
                screen.blit(value_text, value_rect)

            # Desenha botão de venda
            pygame.draw.rect(screen, (0, 255, 0),
                             (modal_x + sell_button.x, modal_y + sell_button.y, sell_button.width, sell_button.height))
            sell_text = font.render("Sell", True, (0, 0, 0))
            sell_rect = sell_text.get_rect(center=(
            modal_x + sell_button.x + sell_button.width // 2, modal_y + sell_button.y + sell_button.height // 2))
            screen.blit(sell_text, sell_rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Verifica clique nos cards
                    for i, item in enumerate(available_items):
                        card_x = modal_x + cards_start_x + (i * (CARD_WIDTH + SPACING))
                        card_rect = pygame.Rect(card_x, modal_y + cards_y, CARD_WIDTH, CARD_HEIGHT)
                        if card_rect.collidepoint(mouse_pos):
                            if item in selected_items:
                                selected_items.remove(item)
                            else:
                                selected_items.append(item)

                    # Verifica clique no botão de venda
                    if (modal_x + sell_button.x <= mouse_pos[0] <= modal_x + sell_button.x + sell_button.width and
                            modal_y + sell_button.y <= mouse_pos[1] <= modal_y + sell_button.y + sell_button.height):
                        self.process_sale(selected_items)
                        running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()

    def process_sale(self, selected_items):
        if not selected_items:
            return

        total_value = sum(item.value for item in selected_items)

        # Remove os itens vendidos da mão do jogador
        for item in selected_items:
            self.player.hand.remove(item)

        # Se o jogador está abaixo do nível 9, pode converter ouro em níveis
        if self.player.level < 9:
            levels_to_gain = total_value // 1000
            remaining_gold = total_value % 1000

            for _ in range(levels_to_gain):
                self.player.level_up()

            self.player.gold += remaining_gold  # Adiciona o ouro restante

            self.renderer.set_message(
                f"Sold items for {total_value} gold. Gained {levels_to_gain} levels and {remaining_gold} gold!")
        else:
            self.player.gold += total_value  # Adiciona todo o valor como ouro
            self.renderer.set_message(f"Sold items for {total_value} gold!")
