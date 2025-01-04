from abc import ABC, abstractmethod

from game.game_state import GamePhase


class BuffsRestriction(ABC):
    @abstractmethod
    def check(self) -> bool:
        pass

class OnlyInCombatRestriction(BuffsRestriction):
    def check(self):
        from game.game_state import GameState
        game_state = GameState.get_instance()

        if game_state.phase == GamePhase.COMBAT:
            return True
        return False
