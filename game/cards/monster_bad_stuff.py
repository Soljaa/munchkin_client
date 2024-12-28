from abc import ABC, abstractmethod
from game.death import Death
from game.dice import Dice

class MonsterBadStuff(ABC):
    @abstractmethod
    def apply(self, player) -> None:
        pass

class DeathBadStuff(MonsterBadStuff):
    def apply(self, player):
        Death(player).apply()

class OrcsBadStuff(MonsterBadStuff):
    def apply(self, player) -> None:
        roll = Dice.roll()
        if roll <= 2:
            Death(player).apply()
        else:
            player.level_down(roll)

class LoseAllClassItemsBadStuff(MonsterBadStuff):
    def apply(self, player) -> None:
        player.lose_all_class_items()

# TODO: Continuar com os outros bad stuffs