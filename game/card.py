from enum import Enum, auto
from game.cards.monster_effect import MonsterEffect
from game.cards.monster_bad_stuff import MonsterBadStuff


class CardType(Enum):
    MONSTER = auto()
    CURSE = auto()
    RACE = auto()
    CLASS = auto()
    ITEM = auto()
    DOOR_BUFF = auto()
    TREASURE_BUFF = auto()


class RaceTypes(Enum):
    DWARF = "Anão"
    ELF = "Elfo"
    HALFlING = "Hobbit"
    HUMAN = "Humano"
    ORC = "Orc"


class ClassTypes(Enum):
    WARRIOR = auto()
    CLERIC = auto()
    THIEF = auto()
    WIZARD = auto()
    BARD = auto()

class ItemSlotTypes(Enum):
    HANDS = auto()
    HEAD = auto()
    ARMOR = auto()
    FEET = auto()


class Gender(Enum):
    MALE = "Masculino"
    FEMALE = "Feminino"


class Card:
    def __init__(self, name, image, type):
        self.name = name
        self.image = image
        self.type = type

    def __str__(self):
        return f"{self.name}"


class Monster(Card):
    def __init__(self, name: str, image: str, level: int, treasure: int, 
                 effect: MonsterEffect = None, bad_stuff: MonsterBadStuff = None, reward_two_levels: bool = False):
        super().__init__(name, image, CardType.MONSTER)
        self.base_level = level
        self.level = level
        self.base_treasure = treasure
        self.treasure = treasure
        self.effect = effect
        self.bad_stuff = bad_stuff
        self.reward_two_levels = reward_two_levels
        self.pursue = True

    def reset_stats(self):
        self.level = self.base_level
        self.treasure = self.base_treasure
        self.pursue = True

    def apply_effect(self, player):
        self.reset_stats()
        if self.effect:
            self.effect.apply(self, player)
    
    def apply_bad_stuff(self, player):
        if self.bad_stuff:
            self.bad_stuff.apply(player)


class Item(Card):
    def __init__(self, name, image, bonus, value, slot=None, big=False, two_hands=False, class_required=None,
                 classes_prohibited=None, race_required=None, races_prohibited=None, gender_required=None,
                 genders_prohibited=None, effect=None):
        super().__init__(name, image, CardType.ITEM)
        self.bonus = bonus  # Bônus concedido pelo item
        self.value = value  # Valor do item em ouro
        self.slot = slot    # Slot onde o item é usado (cabeça, pé, etc)
        self.big = big    # Size é o tamanho (grande, etc) Default é false
        self.class_required = class_required
        self.classes_prohibited = classes_prohibited
        self.race_required = race_required
        self.races_prohibited = races_prohibited
        self.gender_required = gender_required
        self.genders_prohibited = genders_prohibited
        # add gender
        self.two_hands = two_hands  # armas de duas mão, default False
        self.effect = effect  # tupla com tipo e valor

class Race(Card):
    def __init__(self, name, image, special_ability, race_type):
        super().__init__(name, image, CardType.RACE)
        self.special_ability = special_ability
        self.type = race_type

class Class(Card):
    def __init__(self, name, image, special_ability, class_type):
        super().__init__(name, image, CardType.CLASS)
        self.special_ability = special_ability
        self.type = class_type

class Curse(Card):
    def __init__(self, name, image, effect):
        super().__init__(name, image, CardType.CURSE)
        self.effect = effect

    def apply_effect(self, player):
        if self.effect:
            self.effect.apply(self, player)

class DoorBuff(Card):
    def __init__(self, name, image, effect):
        super().__init__(name, image, CardType.DOOR_BUFF)
        self.effect = effect

class TreasureBuff(Card):
    def __init__(self, name, image, effect, restriction=None):
        super().__init__(name, image, CardType.TREASURE_BUFF)
        self.effect = effect
    
    def can_use(self, player) -> bool:
        if self.restriction:
            return self.restriction.check(player)
        return True

    def apply_effect(self, player):
        self.effect.apply(self, player)
