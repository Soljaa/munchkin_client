from game.combat import Combat
from game.game_phases.game_phases import GamePhases
from game.game_state import GamePhase


class CombatPhase(GamePhases):
    def __init__(self, game_state, card, renderer):
        super().__init__(game_state)
        self.player = game_state.current_player()
        self.card = card
        self.renderer = renderer

    def run(self):
        self.game_state.set_game_phase(GamePhase.COMBAT)
        print("Monster encountered! Initializing combat...")

        self.game_state.set_combat(Combat(self.player, self.card))
        print(f"Combat initialized with monster: {self.card.name}")
        self.renderer.set_message(f"Combat initialized with monster: {self.card.name}")

        return True
