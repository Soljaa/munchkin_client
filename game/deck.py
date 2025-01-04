import random
from game.card import Item, RaceTypes, ClassTypes, ItemSlotTypes, Gender
from game.cards.curses import CURSES
from game.cards.items import ITEMS
from game.cards.monsters import MONSTERS
from game.cards.item_effect import IncreaseDiceRollEffect, BonusByRace, EscapeCombat, BlockCurses
from game.cards.treasure_buffs import TREASURE_BUFFS

class Deck:
    def __init__(self):
        self.cards = []
        self.discard_pile = []

    def add_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        card = None
        if not self.cards and self.discard_pile:
            self.cards = self.discard_pile
            self.discard_pile = []
            self.shuffle()
        if self.cards:
            card = self.cards.pop()
        return card

    def discard(self, card):
        self.discard_pile.append(card)


class DoorDeck(Deck):
    def __init__(self):
        super().__init__()
        self._initialize_deck()

    def _initialize_deck(self):
        print("Initializing Door Deck...")

        print(f"Adding {len(MONSTERS)} monsters to deck")
        for monster in MONSTERS:
            self.add_card(monster)

        print(f"Adding {len(CURSES)} curses to deck")
        for curse in CURSES:
            self.add_card(curse)

        races = [
            # TODO: Faltam cartas de raça (com imagem das raças)
            #Race("Elf", "image", "Can sell items for levels"),
            #Race("Dwarf", "image", "Can carry extra items"),
            #Race("Halfling", "image", "Can sell one item per turn"),
            #Race("Human", "image", "Get bonus on running away"),
        ]

        print(f"Adding {len(races)} races to deck")
        for race in races:
            self.add_card(race)

        classes = [
            # TODO: Faltam cartas de classe (com imagem das classes)
        ]

        print(f"Adding {len(classes)} classes to deck")
        for class_ in classes:
            self.add_card(class_)

        door_buffs = [
            # TODO: Buffs
        ]

        print(f"Adding {len(door_buffs)} door buffs to deck")
        for buff in door_buffs:
            self.add_card(buff)

        print(f"Door deck initialized with {len(self.cards)} cards")
        self.shuffle()
        print("Door deck shuffled")


class TreasureDeck(Deck):
    def __init__(self):
        super().__init__()
        self._initialize_deck()

    def _initialize_deck(self):
        print("Initializing Treasure Deck...")

        print(f"Adding {len(ITEMS)} items to deck")
        for item in ITEMS:
            self.add_card(item)

        print(f"Adding {len(TREASURE_BUFFS)} treasure buffs to deck")
        for buff in TREASURE_BUFFS:
            self.add_card(buff)

        print(f"Treasure deck initialized with {len(self.cards)} cards")
        self.shuffle()
        print("Treasure deck shuffled")
