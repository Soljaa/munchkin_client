from abc import ABC, abstractmethod

from game.card import CardType

# OBS: As curses já são aplicadas para o player target, não precisa se preocupar com o alvo.

class CurseEffect(ABC):
    @abstractmethod
    def apply(self, player) -> None:
        pass

class ApplyDiscardCardBadStuffCurseEffect(CurseEffect):
    def apply(self, player) -> None:
        from game.game_state import GameState
        door_deck = GameState.get_instance().door_deck
        card = next((card for card in reversed(door_deck.discard_pile) if card.type == CardType.MONSTER), None)

        if card:
            player.discard_card(card)

class ChangeClassCurseEffect(CurseEffect):        
    def apply(self, player) -> None:
        if player.class_ == None:
            return

        from game.game_state import GameState
        door_deck = GameState.get_instance().door_deck
        card = next((card for card in reversed(door_deck.discard_pile) if card.type == CardType.CLASS), None)

        if not card:
            player.remove_class()
            return
        if card:
            player.replace_class(card)

class ChangeRaceCurseEffect(CurseEffect):        
    def apply(self, player) -> None:
        if player.race == None:
            return

        from game.game_state import GameState
        door_deck = GameState.get_instance().door_deck
        card = next((card for card in reversed(door_deck.discard_pile) if card.type == CardType.RACE), None)

        if not card:
            player.remove_race()
            return
        if card:
            player.replace_race(card)

class LoseRaceCurseEffect(CurseEffect):
    def apply(self, player) -> None:
        player.remove_race()

class LoseClassCurseEffect(CurseEffect):
    def apply(self, player) -> None:
        player.remove_class()