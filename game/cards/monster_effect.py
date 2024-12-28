from abc import ABC, abstractmethod
from game.death import Death
from game.dice import Dice

class MonsterEffect(ABC):
    @abstractmethod
    def apply(self, monster, player) -> None:
        pass

class CompositeEffect(MonsterEffect):
    def __init__(self, *effects: MonsterEffect):
        self.effects = effects
    
    def apply(self, monster, player) -> None:
        for effect in self.effects:
            effect.apply(monster, player)

class IncreaseMonsterLevelEffect(MonsterEffect):
    def __init__(self, raceClass: str, bonus: int):
        self.raceClass = raceClass
        self.bonus = bonus
    
    def apply(self, monster, player) -> None:
        if player.race == self.raceClass or player.class_ == self.raceClass:
            monster.level += self.bonus

class NotPursueLevelEffect(MonsterEffect):
    def __init__(self, level_limit, exclude_race=None):
        self.level_limit = level_limit
        self.exclude_race = exclude_race

    def apply(self, monster, player) -> None:
        if self.exclude_race and player.race == self.exclude_race:
                return
        if player.level <= self.level_limit:
            monster.pursue = False

# TODO: Continuar com os outros efeitos de monstros
