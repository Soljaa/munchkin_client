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

        selected_monster = self.renderer.display_selection_modal(available_monsters,
                                                                 "Selecione um monstro para lutar",
                                                                 "assets/game/monster_modal.png")

        if selected_monster:
            self.current_player.hand.remove(selected_monster)
            combat = Combat(self.current_player, selected_monster)
            self.game_state.set_combat(combat)
            self.game_state.set_game_phase(GamePhase.COMBAT)
            self.renderer.set_message(f"Combate iniciado com: {selected_monster.name}")
            return True

        return False
