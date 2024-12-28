from abc import ABC, abstractmethod
from game.death import Death
from game.dice import Dice

class MonsterBadStuff(ABC):
    @abstractmethod
    def apply(self, player) -> None:
        pass

class DeathBadStuff(MonsterBadStuff):
    def __init__(self, exclude_race=None):
        self.exclude_race = exclude_race

    def apply(self, player):
        if self.exclude_race and player.race == self.exclude_race:
            return
        
        Death(player).apply()

class OrcsBadStuff(MonsterBadStuff):
    def apply(self, player) -> None:
        roll = Dice.roll()
        if roll <= 2:
            Death(player).apply()
        else:
            player.level_down(roll)

class LoseItemsBadStuff(MonsterBadStuff):
    def __init__(self, qty: int):
        self.qty = qty
    def apply(self, player) -> None:
        player.lose_items(self.qty)

class LoseAllClassItemsBadStuff(MonsterBadStuff):
    def apply(self, player) -> None:
        player.lose_all_class_items()

class LoseLevelBadStuff(MonsterBadStuff):
    def __init__(self, level_loss: int):
        self.level_loss = level_loss

    def apply(self, player) -> None:
            player.level_down(self.level_loss)

class LoseAllItemsStuff(MonsterBadStuff):
    def apply(self, player) -> None:
            player.lose_all_items()
    

# TODO: Continuar com os outros bad stuffs