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
                    self.renderer.set_message(f"Equipado {card.name}!")
                else:
                    self.renderer.set_message("Não pode equipar esse item!")

        elif self.action_type == "unequip_item":
            item = self.item
            if item in self.player.equipped_items:
                self.player.unequip_item(item)
                self.renderer.set_message(f"Desequipado {item.name}")

        elif self.action_type == "sell_items":
            self.show_sell_items_modal()

        return True

    def show_sell_items_modal(self):

        available_items = [card for card in self.player.hand if hasattr(card, 'value') and card.value is not None]

        cards_to_sell = self.renderer.display_multi_selection_modal(available_items, "Selecione items para vender",
                                                                    "assets/game/sell_items.png", "assets/game/sell_modal.jpeg")
        self.process_sale(cards_to_sell)

    def process_sale(self, selected_items):
        if not selected_items:
            return

        total_value = sum(item.value for item in selected_items)

        # Remove os itens vendidos da mão do jogador
        for item in selected_items:
            self.player.hand.remove(item)
            self.player.add_to_discard_pile(item)

        self.player.gold += total_value

        # Se o jogador está abaixo do nível 9, pode converter ouro em níveis
        if self.player.level < 9:
            levels_to_gain = self.player.gold // 1000
            remaining_gold = total_value % 1000

            for _ in range(levels_to_gain):
                self.player.level_up()

            self.player.gold = remaining_gold  # Adiciona o ouro restante

            level_plural = "nível" if levels_to_gain == 1 else "niveis"
            self.renderer.set_message(
                f"Total vendido {total_value} ouro. Ganhou {levels_to_gain} {level_plural} e {remaining_gold} ouro!")
        else:
            self.renderer.set_message(f"Total vendido {total_value} ouro!")
