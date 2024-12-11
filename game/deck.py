import random
from game.card import Card, Monster, Item, Race, Class, CardType

class Deck:
    def __init__(self):
        self.cards = []
        self.discard_pile = []

    def add_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards and self.discard_pile:
            self.cards = self.discard_pile
            self.discard_pile = []
            self.shuffle()
        return self.cards.pop() if self.cards else None

    def discard(self, card):
        self.discard_pile.append(card)

class DoorDeck(Deck):
    def __init__(self):
        super().__init__()
        self._initialize_deck()

    def _initialize_deck(self):
        print("Initializing Door Deck...")
        # Add monsters with varying levels
        monsters = [
            Monster("Dragon", 20, 5, "Lose 2 levels"),
            Monster("Goblin", 1, 1, "Lose 1 level"),
            Monster("Orc", 4, 2, "Lose a race card"),
            Monster("Troll", 10, 3, "Lose your equipped items"),
            Monster("Skeleton", 2, 1, "Lose your headgear"),
            Monster("Vampire", 8, 2, "Lose 2 levels"),
            Monster("Zombie", 3, 1, "Lose your footgear"),
            Monster("Werewolf", 6, 2, "Lose your armor"),
            Monster("Ghost", 5, 1, "Run away or lose a level"),
            Monster("Giant Rat", 1, 1, "Lose your food items"),
        ]
        print(f"Adding {len(monsters)} monsters to deck")
        for monster in monsters:
            self.add_card(monster)

        # Add races with special abilities
        races = [
            Race("Elf", "Can sell items for levels"),
            Race("Dwarf", "Can carry extra items"),
            Race("Halfling", "Can sell one item per turn"),
            Race("Human", "Get bonus on running away"),
        ]
        print(f"Adding {len(races)} races to deck")
        for race in races:
            self.add_card(race)

        print(f"Door deck initialized with {len(self.cards)} cards")
        self.shuffle()
        print("Door deck shuffled")

class TreasureDeck(Deck):
    def __init__(self):
        super().__init__()
        self._initialize_deck()

    def _initialize_deck(self):
        print("Initializing Treasure Deck...")
        # Add various items with different bonuses and values
        items = [
            Item("Sword of Slashing", 3, 400),
            Item("Shield of Protection", 2, 300),
            Item("Boots of Running", 1, 200),
            Item("Helmet of Courage", 2, 250),
            Item("Armor of Defense", 3, 450),
            Item("Ring of Power", 1, 300),
            Item("Cloak of Stealth", 2, 350),
            Item("Amulet of Protection", 1, 200),
            Item("Staff of Magic", 2, 400),
            Item("Dagger of Speed", 1, 150),
        ]
        print(f"Adding {len(items)} items to deck")
        for item in items:
            self.add_card(item)

        print(f"Treasure deck initialized with {len(self.cards)} cards")
        self.shuffle()
        print("Treasure deck shuffled")
