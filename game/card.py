from enum import Enum, auto

class CardType(Enum):
    MONSTER = auto()
    CURSE = auto()
    RACE = auto()
    CLASS = auto()
    ITEM = auto()
    BUFF = auto()

class Card:
    def __init__(self, name, card_type, level=0, bonus=0, treasure=0, bad_stuff=""):
        self.name = name
        self.card_type = card_type
        self.level = level
        self.bonus = bonus
        self.treasure = treasure
        self.bad_stuff = bad_stuff
        self.equipped = False

    def __str__(self):
        return f"{self.name} (Level: {self.level}, Bonus: {self.bonus})"

class Monster(Card):
    def __init__(self, name, level, treasure, bad_stuff):
        super().__init__(name, CardType.MONSTER, level=level, treasure=treasure, bad_stuff=bad_stuff)

class Item(Card):
    def __init__(self, name, bonus, value):
        super().__init__(name, CardType.ITEM, bonus=bonus)
        self.value = value
        self.slot = None  # Equipment slot (hand, head, etc.)

class Race(Card):
    def __init__(self, name, special_ability):
        super().__init__(name, CardType.RACE)
        self.special_ability = special_ability

class Class(Card):
    def __init__(self, name, special_ability):
        super().__init__(name, CardType.CLASS)
        self.special_ability = special_ability
