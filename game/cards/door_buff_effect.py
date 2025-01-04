from abc import ABC, abstractmethod


class DoorBuffEffect(ABC):
    @abstractmethod
    def apply(self, target) -> None:
        pass

class IncreaseMonsterLevelBuff(DoorBuffEffect):
    def __init__(self, bonus: int):
        self.bonus = bonus

    def apply(self, monster) -> None:
        monster.level += self.bonus
        if monster.level < 1:
            monster.level = 1

class DrawExtraTreasureBuff(DoorBuffEffect):
    def __init__(self, amount: int):
        self.amount = amount

    def apply(self, monster) -> None:
        monster.treasure += (self.amount)
        if monster.treasure < 1:
            monster.treasure = 1
