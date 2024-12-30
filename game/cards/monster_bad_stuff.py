from abc import ABC, abstractmethod
from game.death import Death
from game.dice import Dice

class MonsterBadStuff(ABC):
    @abstractmethod
    def apply(self, player) -> None:
        pass

class CompositeBadStuff(MonsterBadStuff):
    def __init__(self, *bad_stuffs: MonsterBadStuff):
        self.bad_stuffs = bad_stuffs
    
    def apply(self, monster, player) -> None:
        for bad_stuff in self.bad_stuffs:
            bad_stuff.apply(monster, player)

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
    def __init__(self, qty=None): # Se qty = None, remove todos
        self.qty = qty

    def apply(self, player) -> None:
        player.remove_equipped_items(self.qty)

class LoseHandCardsBadStuff(MonsterBadStuff):
    def __init__(self, qty=None): # Se qty = None, remove todos
        self.qty = qty

    def apply(self, player) -> None:
        player.remove_hand_cards(self.qty)

class LoseLevelBadStuff(MonsterBadStuff):
    def __init__(self, level_loss: int):
        self.level_loss = level_loss

    def apply(self, player) -> None:
        player.level_down(self.level_loss)

class LoseEquippedItemBadStuff(MonsterBadStuff):
    def __init__(self, item_type: str):
        self.item_type = item_type

    def apply(self, player) -> None:
        player.remove_equipped_item_type(self.item_type) 
    
class LoseAllClassItemsBadStuff(MonsterBadStuff):
    def apply(self, player) -> None:
        player.lose_all_equipped_class_items()

# TODO: Continuar com os outros bad stuffs