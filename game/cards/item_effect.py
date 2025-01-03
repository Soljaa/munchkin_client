from abc import ABC, abstractmethod

# TODO implementar efeitos dos items
class ItemEffect(ABC):
    @abstractmethod
    def apply(self, player) -> None:
        pass


class IncreaseDiceRollEffect(ItemEffect):

    def __init__(self, value=1):
        self.increase_by = value

    def apply(self, player) -> None:
        pass


class BonusByRace(ItemEffect):

    def __init__(self, race, value=2):
        self.increase_by = value
        self.race_required = race

    def apply(self, player) -> None:
        pass


class EscapeCombat(ItemEffect):

    def __init__(self, monster_level=None):
        self.monster_level_limit = monster_level

    def apply(self, player) -> None:
        pass


class BlockCurses(ItemEffect):

    def apply(self, player) -> None:
        pass
