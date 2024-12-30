from abc import ABC, abstractmethod

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

class PlayerLoseLevelsIfLevelIsBiggerThanMonsterEffect(MonsterEffect):
    def __init__(self, level_loss: int):
        self.level_loss = level_loss

    def apply(self, monster, player) -> None:
        if player.level > monster.level:
            player.level_down(self.level_loss)

class MoreTreasureEffect(MonsterEffect):
    def __init__(self, qty_plus_treasure, include_race=None):
        self.qty_plus_treasure = qty_plus_treasure
        self.include_race = include_race

    def apply(self, monster, player) -> None:
        if not self.include_race:
            monster.treasure += 1
        elif self.include_race and player.race==self.include_race:
            monster.treasure += 1
            


# TODO: Continuar com os outros efeitos de monstros
