from game.game_phases.game_phases import GamePhases


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

        return True
