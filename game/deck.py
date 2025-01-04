import random
from game.cards.classes import CLASSES
from game.cards.curses import CURSES
from game.cards.door_buffs import DOOR_BUFFS
from game.cards.items import ITEMS
from game.cards.monsters import MONSTERS
from game.cards.races import RACES
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

        print(f"Adding {len(RACES)} races to deck")
        for race in RACES:
            self.add_card(race)

        # print(f"Adding {len(CLASSES)} classes to deck")
        # for class_ in CLASSES:
        #     self.add_card(class_)

        print(f"Adding {len(DOOR_BUFFS)} door buffs to deck")
        for buff in DOOR_BUFFS:
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
