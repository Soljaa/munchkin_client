from abc import ABC, abstractmethod
from game.game_state import GameState

# OBS: As curses já são aplicadas para o player target, não precisa se preocupar com o alvo.

class CurseEffect(ABC):
    @abstractmethod
    def apply(self, player) -> None:
        pass

class ApplyDiscardCardBadStuffCurseEffect(CurseEffect):
    def apply(self, player) -> None:
        door_deck = GameState.get_instance().door_deck
        card = next((card for card in reversed(door_deck.discard_pile) if card.type == 'monster'), None)
        if card:
            card.apply_bad_stuff(player)
