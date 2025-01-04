from abc import ABC, abstractmethod


class DoorBuffEffect(ABC):
    @abstractmethod
    def apply(self, target) -> None:
        pass

class IncreaseMonsterLevelBuff(DoorBuffEffect):
    def __init__(self, bonus: int):
        self.bonus = bonus

    def apply(self, target) -> None:
        target.level += self.bonus
        if target.level < 1:
            target.level = 1

class DrawExtraTreasure(DoorBuffEffect):
    def __init__(self, amount: int):
        self.amount = amount

    def apply(self, target) -> None:
        target.draw_extra_treasure(self.amount)