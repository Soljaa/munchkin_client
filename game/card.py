from enum import Enum, auto

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
    def __init__(self, name, image, level, treasure, bad_stuff):
        super().__init__(name, image, CardType.MONSTER)
        self.level = level        
        self.treasure = treasure  
        self.bad_stuff = bad_stuff

class Item(Card):
    def __init__(self, name, image, bonus, value, slot=None, size="Small"):
        super().__init__(name, image, CardType.ITEM)
        self.bonus = bonus  # Bônus concedido pelo item
        self.value = value  # Valor do item em ouro
        self.slot = slot    # Slot onde o item é usado (cabeça, pé, etc)
        self.slot = size    # Size é o tamanho (grande, etc) Default é small porque o jogo diz que todo item que não é grande é pequeno

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

# Classe para cartas de buff
class Buff(Card):
    def __init__(self, name, image, effect, target):
        super().__init__(name, image, card_type="Buff")
        self.effect = effect  # Efeito do buff
        self.target = target  # Alvo do buff (jogador, monstro, etc.)