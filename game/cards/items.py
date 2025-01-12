from game.card import ClassTypes, Gender, Item, RaceTypes
from game.cards.item_effect import *


ITEMS = [
    Item(
        name="Bad-Ass Bandana",
        image="assets/treasure_cards/BadAssBandana.png",
        bonus=3,
        value=400,
        slot="head",
        race_required=RaceTypes.HUMAN
    ),
    Item(
        name="Boots of Butt-Kicking",
        image="assets/treasure_cards/BootOfButtKicking.png",
        bonus=2,
        value=400,
        slot="feet"
    ),
    Item(
        name="Boots of Running Really Fast",
        image="assets/treasure_cards/BootOfButtKicking.png",
        bonus=0,
        value=400,
        slot="feet",
        effect=IncreaseDiceRollEffect(value=2)
    ),
    Item(
        name="Bow with Ribbons",
        image="assets/treasure_cards/BowWithRibbons.png",
        bonus=4,
        value=800,
        slot="hands",
        two_hands=True,
        race_required=RaceTypes.ELF
    ),
    Item(
        name="Broad Sword",
        image="assets/treasure_cards/BroadSword.png",
        bonus=3,
        value=400,
        slot="hands",
        gender_required=Gender.FEMALE
    ),
    Item(
        name="Buckler of Swashing",
        image="assets/treasure_cards/BucklerOfSwashing.png",
        bonus=2,
        value=400,
        slot="hands"
    ),
    Item(
        name="Chainsaw of Bloody Dismemberment",
        image="assets/treasure_cards/ChainsawOfBloodyDismemberment.png",
        bonus=3,
        value=600,
        slot="hands",
        two_hands=True,
    ),
    Item(
        name="Cheese Grater of Peace",
        image="assets/treasure_cards/CheeseGraterOfPeace.png",
        bonus=3,
        value=400,
        slot="hands",
        class_required=ClassTypes.CLERIC
    ),
    Item(
        name="Cloak of Obscurity",
        image="assets/treasure_cards/CloakOfObscurity.png",
        bonus=4,
        value=600,
        class_required=ClassTypes.THIEF
    ),
    Item(
        name="Dagger of Treachery",
        image="assets/treasure_cards/DaggerOfTreachery.png",
        bonus=3,
        value=400,
        slot="hands",
        class_required=ClassTypes.THIEF
    ),
    Item(
        name="Eleven-Foot Pole",
        image="assets/treasure_cards/ElevenFootPole.png",
        bonus=1,
        value=200,
        slot="hands",
        two_hands=True
    ),
    Item(
        name="Flaming Armor",
        image="assets/treasure_cards/FlamingArmor.png",
        bonus=2,
        value=400,
        slot="armor"
    ),
    Item(
        name="Gentlemen´s Club",
        image="assets/treasure_cards/GentlemensClub.png",
        bonus=3,
        value=400,
        slot="hands",
        gender_required=Gender.MALE
    ),
    Item(
        name="Hammer of Kneecapping",
        image="assets/treasure_cards/HammerOfKneecapping.png",
        bonus=4,
        value=600,
        slot="hands",
        race_required=RaceTypes.DWARF
    ),
    Item(
        name="Helm of Courage",
        image="assets/treasure_cards/HelmOfCourage.png",
        bonus=1,
        value=200,
        slot="head"
    ),
    Item(
        name="Horny Helmet",
        image="assets/treasure_cards/HornyHelmet.png",
        bonus=1,
        value=600,
        slot="head",
        effect=BonusByRace(RaceTypes.ELF, 2)
    ),
    Item(
        name="Huge Rock",
        image="assets/treasure_cards/HugeRock.png",
        bonus=3,
        value=None,
        slot="hands",
        two_hands=True,
    ),
    Item(
        name="Leather Armor",
        image="assets/treasure_cards/LeatherArmor.png",
        bonus=1,
        value=200,
        slot="armor"
    ),
    Item(
        name="Limburger and Anchovy Sandwich",
        image="assets/treasure_cards/LimburgerAndAnchovySandwich.png",
        bonus=3,
        value=400,
        race_required=RaceTypes.HALFlING
    ),
    Item(
        name="Mace of Sharpness",
        image="assets/treasure_cards/MaceOfSharpness.png",
        bonus=4,
        value=600,
        slot="hands",
        class_required=ClassTypes.CLERIC
    ),
    Item(
        name="Mithril Armor",
        image="assets/treasure_cards/MithrilArmor.png",
        bonus=3,
        value=600,
        slot="armor",
        big=True,
        classes_prohibited=[ClassTypes.WIZARD]
    ),
    Item(
        name="Pantyhose of Giant Strength",
        image="assets/treasure_cards/PantyHoseOfGiantStrength.png",
        bonus=3,
        value=600,
        classes_prohibited=[ClassTypes.WARRIOR]
    ),
    Item(
        name="Pointy Hat of Power",
        image="assets/treasure_cards/PointyHatOfPower.png",
        bonus=3,
        value=400,
        slot="head",
        class_required=ClassTypes.WIZARD
    ),
    Item(
        name="Rapier of Unfairness",
        image="assets/treasure_cards/RapierOfUnfairness.png",
        bonus=3,
        value=600,
        slot="hands",
        race_required=RaceTypes.ELF
    ),
    Item(
        name="Rat on a Stick",
        image="assets/treasure_cards/RatOnAStick.png",
        bonus=1,
        value=None,
        slot="hands",
        effect=EscapeCombat(8)
    ),
    # Item("Sandal of Protection", "assets/treasure_cards/SandalsOfProtection.png", 0,
    #      700, "feet", effect=BlockCurses()), rever items sem slot
    Item(
        name="Short Wide Armor",
        image="assets/treasure_cards/ShortWideArmor.png",
        bonus=3,
        value=400,
        slot="armor",
        race_required=RaceTypes.DWARF
    ),
    Item(
        name="Singing & Dancing Sword",
        image="assets/treasure_cards/SingingAndDancingSword.png",
        bonus=2,
        value=400,
        slot="hands",
        classes_prohibited=[ClassTypes.THIEF]
    ),
    Item(
        name="Slimy Armor",
        image="assets/treasure_cards/SlimyArmor.png",
        bonus=1,
        value=200,
        slot="armor"
    ),
    Item(
        name="Sneaky Bastard Sword",
        image="assets/treasure_cards/SneakyBastardSword.png",
        bonus=2,
        value=400,
        slot="hands"
    ),
    Item(
        name="Spiky Knees",
        image="assets/treasure_cards/SpikyKnees.png",
        bonus=1,
        value=200
    ),
    Item(
        name="Staff of Napalm",
        image="assets/treasure_cards/StaffOfNapalm.png",
        bonus=5,
        value=800,
        slot="hands",
        class_required=ClassTypes.WIZARD
    ),
    Item(
        name="Stepladder",
        image="assets/treasure_cards/Stepladder.png",
        bonus=3,
        value=400,
        two_hands=True,
        race_required=RaceTypes.HALFlING
    ),
    Item(
        name="Swiss Army Polearm",
        image="assets/treasure_cards/SwissArmyPolearm.png",
        bonus=4,
        value=600,
        slot="hands",
        big=True,
        two_hands=True,
        race_required=RaceTypes.HUMAN
    ),
    Item(
        name="Really Impressive Title",
        image="assets/treasure_cards/Really.png",
        bonus=3,
        value=None,
    ),
    Item(
        name="Hireling",
        image="assets/treasure_cards/Hireling.png",
        bonus=1,
        value=None,
        effect=None  # adicionar efeitos
    ),

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
