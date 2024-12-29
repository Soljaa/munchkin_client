from enum import Enum, auto
from game.cards.monster_effect import MonsterEffect
from game.cards.monster_bad_stuff import MonsterBadStuff

class CardType(Enum):
    MONSTER = auto()
    CURSE = auto()
    RACE = auto()
    CLASS = auto()
    ITEM = auto()
    BUFF = auto()

class Card:
    def __init__(self, name, image, card_type):
        self.name = name
        self.image = image
        self.card_type = card_type
        self.equipped = False #TODO: Ver se o "equipado" entra na classe pai ou se entra nas classes filhas apropriadas. Pois, por exemplo, a classe Monstro não se equipa (eu acho), já a classe Item sim.

    def __str__(self):
        return f"{self.name} (Level: {self.level}, Bonus: {self.bonus})"

class Monster(Card):
    def __init__(self, name: str, image: str, level: int, treasure: int, 
                 effect: MonsterEffect = None, bad_stuff: MonsterBadStuff = None):
        super().__init__(name, image, CardType.MONSTER)
        self.base_level = level
        self.level = level
        self.base_treasure = treasure
        self.treasure = treasure
        self.effect = effect
        self.bad_stuff = bad_stuff
        self.pursue = True

    def reset_stats(self):
        self.level = self.base_level
        self.pursue = True

    def apply_effect(self, player):
        self.reset_stats()
        if self.effect:
            self.effect.apply(self, player)
    
    def apply_bad_stuff(self, player):
        if self.bad_stuff:
            self.bad_stuff.apply(player)

class Item(Card):
    def __init__(self, name, image, bonus, value, slot=None, size="Small"):
        super().__init__(name, image, CardType.ITEM)
        self.bonus = bonus  # Bônus concedido pelo item
        self.value = value  # Valor do item em ouro
        self.slot = slot    # Slot onde o item é usado (cabeça, pé, etc)
        self.size = size    # Size é o tamanho (grande, etc) Default é small porque o jogo diz que todo item que não é grande é pequeno
        self.class_required = None
        self.class_prohibited = None

class Race(Card):
    def __init__(self, name, image, special_ability):
        super().__init__(name, image, CardType.RACE)
        self.special_ability = special_ability

class Class(Card):
    def __init__(self, name, image, special_ability):
        super().__init__(name, image, CardType.CLASS)
        self.special_ability = special_ability

# Classe para cartas de maldição
class Curse(Card):
    def __init__(self, name, image, effect):
        super().__init__(name, image, CardType.CURSE)
        self.effect = effect  # Efeito da maldição ao ser aplicada

    def apply_effect(self, player):
        if self.effect:
            self.effect.apply(self, player)

# Classe para cartas de buff
class Buff(Card):
    def __init__(self, name, image, effect, target):
        super().__init__(name, image, card_type="Buff")
        self.effect = effect  # Efeito do buff
        self.target = target  # Alvo do buff (jogador, monstro, etc.)