from abc import ABC, abstractmethod
from game.card import CardType


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
            card.apply_bad_stuff(player)
            player.add_to_discard_pile(card)

    def __str__(self):
        return "Você recebe a bad stuff do último monstro!"

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

    def __str__(self):
        return "Você muda de classe!"

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

    def __str__(self):
        return "Você muda de raça!"

class LoseRaceCurseEffect(CurseEffect):
    def apply(self, player) -> None:
        player.remove_race()

    def __str__(self):
        return "Você perde sua raça!"

class LoseClassCurseEffect(CurseEffect):
    def apply(self, player) -> None:
        player.remove_class()

    def __str__(self):
        return "Você perde sua classe!"