import random
from game.card import Item, RaceTypes, ClassTypes, ItemSlotTypes, Gender
from game.cards.curses import CURSES
from game.cards.monsters import MONSTERS
from game.cards.item_effect import IncreaseDiceRollEffect, BonusByRace, EscapeCombat, BlockCurses


class Dice:
    @staticmethod
    def roll():
        value = random.randint(1, 6)
        return value


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
        # Add various items with different bonuses and values
        items = [
            Item("Bad-Ass Bandana", "assets/treasure_cards/BadAssBandana.png", 3, 400,
                 "head", race_required=RaceTypes.HUMAN),
            Item("Boots of Butt-Kicking", "assets/treasure_cards/BootOfButtKicking.png", 2,
                 400, "feet"),
            Item("Boots of Running Really Fast", "assets/treasure_cards/BootOfButtKicking.png", 0,
                 400, "feet", effect=IncreaseDiceRollEffect(value=2)),
            Item("Bow with Ribbons", "assets/treasure_cards/BowWithRibbons.png", 4, 800,
                 "hands", two_hands=True, race_required=RaceTypes.ELF),
            Item("Broad Sword", "assets/treasure_cards/BroadSword.png", 3, 400, "hands", gender_required=Gender.FEMALE),
            Item("Buckler of Swashing", "assets/treasure_cards/BucklerOfSwashing.png", 2, 400,
                 "hands"),
            Item("Chainsaw of Bloody Dismemberment",
                 "assets/treasure_cards/ChainsawOfBloodyDismemberment.png", 3, 600, "hands",
                 True, True),
            Item("Cheese Grater of Peace", "assets/treasure_cards/CheeseGraterOfPeace.png", 3,
                 400, "hands", class_required=ClassTypes.CLERIC),
            Item("Cloak of Obscurity", "assets/treasure_cards/CloakOfObscurity.png", 4, 600,
                 "armor", class_required=ClassTypes.THIEF),
            Item("Dagger of Treachery", "assets/treasure_cards/DaggerOfTreachery.png", 3, 400,
                 "hands", class_required=ClassTypes.THIEF),
            Item("Eleven-Foot Pole", "assets/treasure_cards/ElevenFootPole.png", 1, 200,
                 "hands", two_hands=True),
            Item("Flaming Armor", "assets/treasure_cards/FlamingArmor.png", 2, 400,
                 "armor"),
            Item("Gentlemen´s Club", "assets/treasure_cards/GentlemensClub.png", 3, 400,
                 "hands", gender_required=Gender.MALE),
            Item("Hammer of Kneecapping", "assets/treasure_cards/HammerOfKneecapping.png", 4,
                 600, "hands", race_required=RaceTypes.DWARF),
            Item("Helm of Courage", "assets/treasure_cards/HelmOfCourage.png", 1, 200,
                 "head"),
            Item("Horny Helmet", "assets/treasure_cards/HornyHelmet.png", 1, 600, "head",
                 effect=BonusByRace(RaceTypes.ELF, 2)),
            Item("Huge Rock", "assets/treasure_cards/HugeRock.png", 3, None, "hands",
                 True, True),
            Item("Leather Armor", "assets/treasure_cards/LeatherArmor.png", 1, 200,
                 "armor"),
            Item("Limburger and Anchovy Sandwich", "assets/treasure_cards/LimburgerAndAnchovySandwich.png",
                 3, 400, "hands", race_required=RaceTypes.HALFlING),
            Item("Mace of Sharpness", "assets/treasure_cards/MaceOfSharpness.png", 4, 600,
                 "hands", class_required=ClassTypes.CLERIC),
            Item("Mithril Armor", "assets/treasure_cards/MithrilArmor.png", 3, 600,
                 "armor", True, classes_prohibited=[ClassTypes.WIZARD]),
            Item("Pantyhose of Giant Strength", "assets/treasure_cards/PantyhoseOfGiantStrength.png",
                 3, 600, "feet", classes_prohibited=[ClassTypes.WARRIOR]),
            Item("Pointy Hat of Power", "assets/treasure_cards/PointyHatofPower.png", 3, 400,
                 "head", class_required=ClassTypes.WIZARD),
            Item("Rapier of Unfairness", "assets/treasure_cards/RapierOfUnfairness.png", 3,
                 600, "hands", race_required=RaceTypes.ELF),
            Item("Rat on a Stick", "assets/treasure_cards/RatOnAStick.png", 1, None,
                 "hands", effect=EscapeCombat(8)),
            # Item("Sandal of Protection", "assets/treasure_cards/SandalsOfProtection.png", 0,
            #      700, "feet", effect=BlockCurses()), rever items sem slot
            Item("Short Wide Armor", "assets/treasure_cards/ShortWideArmor.png", 3, 400,
                 "armor", race_required=RaceTypes.DWARF),
            Item("Singing & Dancing Sword", "assets/treasure_cards/SingingAndDancingSword.png", 2,
                 400, "hands", classes_prohibited=[ClassTypes.THIEF]),
            Item("Slimy Armor", "assets/treasure_cards/SlimyArmor.png", 1, 200, "armor"),
            Item("Sneaky Bastard Sword", "assets/treasure_cards/SneakyBastardSword.png", 2, 400, "hands"),
            # Item("Spiky Knees", "assets/treasure_cards/SpikyKnees.png", 1, 200, "armor"), rever items sem slot
            Item("Staff of Napalm", "assets/treasure_cards/StaffOfNapalm.png", 5, 800,
                 "hands", class_required=ClassTypes.WIZARD),
            Item("Stepladder", "assets/treasure_cards/Stepladder.png", 3, 400, "feet",
                 True, race_required=RaceTypes.HALFlING),
            Item("Swiss Army Polearm", "assets/treasure_cards/SwissArmyPolearm.png", 4, 600,
                 "hands", True, True, race_required=RaceTypes.HUMAN),

            #Item("Sword of Slashing", "image", 3, 400),
            #Item("Shield of Protection", 2, 300),
            #Item("Boots of Running", 1, 200),
            #Item("Helmet of Courage", 2, 250),
            #Item("Armor of Defense", 3, 450),
            #Item("Ring of Power", 1, 300),
            #Item("Cloak of Stealth", 2, 350),
            #Item("Amulet of Protection", 1, 200),
            #Item("Staff of Magic", 2, 400),
            #Item("Dagger of Speed", 1, 150),
        ]
        print(f"Adding {len(items)} items to deck")
        for item in items:
            self.add_card(item)

        treasure_buffs = [
            # TODO: Buffs
        ]
        print(f"Adding {len(treasure_buffs)} treasure buffs to deck")
        for buff in treasure_buffs:
            self.add_card(buff)

        print(f"Treasure deck initialized with {len(self.cards)} cards")
        self.shuffle()
        print("Treasure deck shuffled")

# TODO: Falta colocar os Buffs