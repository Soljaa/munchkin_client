from abc import ABC, abstractmethod


class BuffsRestriction(ABC):
    @abstractmethod
    def check(self, player) -> bool:
        pass

class OnlyInCombatRestriction(BuffsRestriction):
    def check(self, player):
        from game.game_state import GamePhase
        from game.game_state import GameState
        game_state = GameState.get_instance()

        if game_state.phase == GamePhase.COMBAT:
            return True
        return False
