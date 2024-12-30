from game.game_phases.game_phases import GamePhases


class SetupPhase(GamePhases):
    def __init__(self, game_state, action, renderer):
        super().__init__(game_state)
        self.player = game_state.current_player()
        self.action_type = action[0]
        self.item_index = action[1]
        self.renderer = renderer

    def run(self):
        print(f"Changing items: {self.game_state.phase}")

        if self.action_type == "equip_item":
            card = self.player.hand[self.item_index]
            if self.player.equip_item(card):
                self.renderer.set_message(f"Equipped {card.name}!")
            else:
                self.renderer.set_message("Cannot equip this item!")

        elif self.action_type == "unequip_item":
            item = self.player.equipped_items[self.item_index]
            self.player.unequip_item(item)
            self.renderer.set_message(f"Unequipped {item.name}")

        return True
