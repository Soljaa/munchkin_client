import random
from game.card import Monster, Item, Race
from game.death import Death
from game.cards.monster_effect import *
from game.cards.monster_bad_stuff import *

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
            self.discard(card)
        return card

    def discard(self, card):
        self.discard_pile.append(card)

class DoorDeck(Deck):
    def __init__(self):
        super().__init__()
        self._initialize_deck()

    def _initialize_deck(self):
        print("Initializing Door Deck...")
        # Add monsters with varying levels

        # TODO: Falta png do hairy potter

        monsters = [
            #TODO: O "BadStuff" está com X, pois tem uns que não são tão complexos como apenas "Lose 2 levels". Pensar em como fazer depois
            # 3,872 Orcs
            Monster(
                name="3,872 Orcs",
                image="assets/door_cards/3872Orcs.png",
                level=10,
                treasure=3,
                effect=IncreaseMonsterLevelEffect('Dwarf', 6),
                bad_stuff=OrcsBadStuff(),
            ),
            # Squidzilla
            Monster(
                name="Squidzilla", 
                image="assets/door_cards/Squidzilla.png", 
                level=18, 
                treasure=4, 
                effect=CompositeEffect(IncreaseMonsterLevelEffect('Elf', 4), NotPursueLevelEffect(4, exclude_race='Elf')), 
                bad_stuff=DeathBadStuff()
            ),
            # Hairy Potter
            Monster(
                name="Hairy Potter",
                image="assets/door_cards/HairyPotter.png",
                level=15,
                treasure=4,
                effect=CompositeEffect(IncreaseMonsterLevelEffect('Wizard', 4), IncreaseMonsterLevelEffect('Elf', -3), NotPursueLevelEffect(2)),
                bad_stuff=LoseAllClassItemsBadStuff()
            ),

            # Amazon #TODO
            Monster(name="Amazon", image="assets/door_cards/Amazon.png", level=8, treasure=2, bad_stuff=None),
            
            # Bigfoot
            Monster(
                name="Bigfoot",
                image="assets/door_cards/Bigfoot.png", 
                level=12,
                treasure=3,
                effect= CompositeEffect(
                    IncreaseMonsterLevelEffect("Dwarf", 3),
                    IncreaseMonsterLevelEffect("Halfling", 3),
                ),
                bad_stuff= LoseTheEquippedHeadgearBadStuff,
            ),
            #Bullrog
            Monster(
                name= "Bullrog",
                image= "assets/door_cards/Bullrog.png",
                level=18, 
                treasure=5, 
                effect= CompositeBadStuff(NotPursueLevelEffect(4)),
                bad_stuff= DeathBadStuff(),
            ),
            
            #Crabs
            Monster("Crabs", "assets/door_cards/Crabs.png", level=1, treasure=1, bad_stuff=None),
            # Drooling Slime #TODO
            Monster("Drooling Slime", "assets/door_cards/DroolingSlime.png", 1, 1, "X"),
            
            #Face Sucker
            Monster(name= "Face Sucker",
                    image= "assets/door_cards/FaceSucker.png",
                    level= 8,
                    treasure= 2, 
                    effect= CompositeEffect(IncreaseMonsterLevelEffect("Elf", 6)),
                    bad_stuff= CompositeBadStuff(
                        LoseTheEquippedHeadgearBadStuff(),
                        LoseLevelBadStuff(1),
                    ),
                ),
            
            # Floating Nose #TODO
            Monster("Floating Nose", "assets/door_cards/FloatingNose.png", 10, 3, "X"),
            # Flying Frogs #TODO
            Monster("Flying Frogs", "assets/door_cards/FlyingFrogs.png", 2, 1, "X"),
            # Gazebo #TODO
            Monster("Gazebo", "assets/door_cards/Gazebo.png", 8, 2, "X"),
            # Gelatinous Octahedron #TODO
            Monster("Gelatinous Octahedron", "assets/door_cards/Gazebo.png", 2, 1, "X"),
            # Ghoulfiends #TODO
            Monster("Ghoulfiends", "assets/door_cards/Ghoulfiends.png", 8, 2, "X"),
            # Harpies #TODO
            Monster("Harpies", "assets/door_cards/Harpies.png", 4, 2, "X"),
            # Hippogriff #TODO
            Monster("Hippogriff", "assets/door_cards/Hippogriff.png", 16, 4, "X"),
            # Insurance Salesman #TODO
            Monster("Insurance Salesman", "assets/door_cards/InsuranceSalesman.png", 14, 4, "X"),

            
            # King Tut
            Monster(
                name= "King Tut",
                image= "assets/door_cards/KingTut.png",
                level= 16,
                treasure= 4,
                effect=CompositeEffect(
                    NotPursueLevelEffect(3), 
                    PlayerLoseLevelsIfLevelIsBiggerThanMonsterEffect(2)
                ),
                bad_stuff= LoseAllItemsBadStuff(),
            ),
            
            #Lame Goblin #TODO
            Monster("Lame Goblin", "assets/door_cards/LameGoblin.png", 1, 1, "X"),
            #Large Angry Chicken #TODO
            Monster("Large Angry Chicken", "assets/door_cards/LargeAngryChicken.png", 2, 1, "X"),
            #Lawyers #TODO
            Monster("Lawyers", "assets/door_cards/Lawyers.png", 6, 2, "X"),
            
            #Leperchaun
            Monster(
                name= "Leperchaun",
                image= "assets/door_cards/Leperchaun.png",
                level= 4,
                treasure= 2,
                effect= CompositeEffect(IncreaseMonsterLevelEffect("Elf", 5)),
                bad_stuff= LoseItemsBadStuff(2),
            ),
            #Maul Rat
            Monster(
                name= "Maul Rat",
                    image="assets/door_cards/MaulRat.png",
                    level= 1,
                    treasure= 1,
                    effect= CompositeEffect(IncreaseMonsterLevelEffect("Cleric", 3)),
                    bad_stuff= LoseLevelBadStuff(1),
                ),
            
            #Mr. Bones #TODO
            Monster("Mr. Bones", "assets/door_cards/MrBones.png", 2, 1, "X"), # TODO: Ele é undead
            # Net Troll #TODO
            Monster("Net Troll", "assets/door_cards/NetTroll.png", 10, 3, "X"),
            #Pit Bull #TODO
            Monster("Pit Bull", "assets/door_cards/PitBull.png", 2, 1, "X"),
            # Platycore #TODO
            Monster("Platycore", "assets/door_cards/Platycore.png", 6, 2, "X"),
            
            # Plutonium Dragon
            Monster(
                name= "Plutonium Dragon",
                image= "assets/door_cards/PlutoniumDragon.png",
                level= 20,
                treasure= 5, 
                effect= CompositeEffect(NotPursueLevelEffect(5)),
                bad_stuff= DeathBadStuff(),
            ),
            # Potted Plant
            Monster(
                name= "Potted Plant",
                image= "assets/door_cards/PottedPlant.png",
                level= 1,
                treasure= 1, 
                effect= CompositeEffect(MoreTreasureEffect(1, "Elf")),
                bad_stuff= None
            ),

            # Pukachu #TODO
            Monster("Pukachu", "assets/door_cards/Pukachu.png", 6, 2, "X"),
            # Shrieking Geek #TODO
            Monster("Shrieking Geek", "assets/door_cards/ShriekingGeek.png", 6, 2, "X"),
            # Snails on Speed #TODO
            Monster("Snails on Speed", "assets/door_cards/SnailsOnSpeed.png", 4, 2, "X"),
            # Stoned Golem #TODO
            Monster("Stoned Golem", "assets/door_cards/StonedGolem.png", 14, 4, "X"),
            # Tongue Demon #TODO
            Monster("Tongue Demon", "assets/door_cards/TongueDemon.png", 12, 3, "X"), 
            
            # Undead Horse
            Monster(
                name="Undead Horse",
                image= "assets/door_cards/UndeadHorse.png", 
                level=4, 
                treasure=2,
                effect=CompositeEffect(IncreaseMonsterLevelEffect("Dwarves", 5)),
                bad_stuff= LoseLevelBadStuff(2),
            ), # TODO: Ele é undead
            
            # Unspeakably Awful Indescriblabe Horror #TODO
            Monster("Unspeakably Awful Indescribable Horror", "assets/door_cards/UnspeakablyAwfulIndescribableHorror.png", 14, 4, "X"),
            # Wannabe Vampire #TODO
            Monster("Wannabe Vampire", "assets/door_cards/WannabeVampire.png", 12, 3, "X"),
            # Wight Brothers
            
            Monster(
                name= "Wight Brothers",
                image= "assets/door_cards/WightBrothers.png",
                level= 16,
                treasure= 4,
                effect= CompositeEffect(
                    PlayerLoseLevelsIfLevelIsBiggerThanMonsterEffect(2), 
                    NotPursueLevelEffect(3)
                ),
                bad_stuff= LoseLevelBadStuff(1),
                
            )

            #Monster("Dragon", "image", 20, 5, "Lose 2 levels"),
            #Monster("Goblin", 1, 1, "Lose 1 level"),
            #Monster("Orc", 4, 2, "Lose a race card"),
            #Monster("Troll", 10, 3, "Lose your equipped items"),
            #Monster("Skeleton", 2, 1, "Lose your headgear"),
            #Monster("Vampire", 8, 2, "Lose 2 levels"),
            #Monster("Zombie", 3, 1, "Lose your footgear"),
            #Monster("Werewolf", 6, 2, "Lose your armor"),
            #Monster("Ghost", 5, 1, "Run away or lose a level"),
            #Monster("Giant Rat", 1, 1, "Lose your food items"),
        ]
        print(f"Adding {len(monsters)} monsters to deck")
        for monster in monsters:
            self.add_card(monster)

        curses = [

        ]

        print(f"Adding {len(curses)} races to deck")
        for curse in curses:
            self.add_card(curse)

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
            # TODO: Poção entra como item? 
            # TODO: Observar o "slot" e "size".
            Item("Bad-Ass Bandana", "assets/treasure_cards/BadAssBandana.png", 3, 400, "head"),
            Item("Boots of Butt-Kicking", "assets/treasure_cards/BootOfButtKicking.png", 2, 400, "feet"),
            Item("Bow with Ribbons", "assets/treasure_cards/BowWithRibbons.png", 4, 800, "hands"),
            Item("Broad Sword", "assets/treasure_cards/BroadSword.png", 3, 400, "hands"),
            Item("Buckler of Swashing", "assets/treasure_cards/BucklerOfSwashing.png", 2, 400, "hands"),
            Item("Chainsaw of Bloody Dismemberment", "assets/treasure_cards/ChainsawOfBloodyDismemberment.png", 3, 600, "hands" , "Big"),
            Item("Cheese Grater of Peace", "assets/treasure_cards/CheeseGraterOfPeace.png", 3, 400, "hands"),
            Item("Cloak of Obscurity", "assets/treasure_cards/CloakOfObscurity.png", 4, 600),
            Item("Dagger of Treachery", "assets/treasure_cards/DaggerOfTreachery.png", 3, 400, "hands"),
            Item("Eleven-Foot Pole", "assets/treasure_cards/ElevenFootPole.png", 1, 200, "hands"),
            Item("Flaming Armor", "assets/treasure_cards/FlamingArmor.png", 2, 400, "armor"),
            Item("Gentlemen´s Club", "assets/treasure_cards/GentlemensClub.png", 3, 400, "hands"),
            Item("Hammer of Kneecapping", "assets/treasure_cards/HammerOfKneecapping.png", 4, 600, "hands"),
            Item("Helm of Courage", "assets/treasure_cards/HelmOfCourage.png", 1, 200, "head"),
            Item("Horny Helmet", "assets/treasure_cards/HornyHelmet.png", "1, mas se for elfo é 3 ", 600, "head"), #TODO bonus. Como fazer?
            Item("Huge Rock", "assets/treasure_cards/HugeRock.png", 3, None, "hands", "Big"),
            Item("Leather Armor", "assets/treasure_cards/LeatherArmor.png", 1, 200, "armor"),
            Item("Limburger and Anchovy Sandwich", "assets/treasure_cards/LimburgerAndAnchovySandwich.png", 3, 400),
            Item("Mace of Sharpness", "assets/treasure_cards/MaceOfSharpness.png", 4, 600, "hands"),
            Item("Mithril Armor", "assets/treasure_cards/MithrilArmor.png", 3, 600, "armor", "Big"),
            Item("Pantyhose of Giant Strength", "assets/treasure_cards/PantyhoseOfGiantStrength.png", 3, 600),
            Item("Pointy Hat of Power", "assets/treasure_cards/PointyHatofPower.png", 3, 400, "head"),
            Item("Rapier of Unfairness", "assets/treasure_cards/RapierOfUnfairness.png", 3, 600, "hands"),
            Item("Rat on a Stick", "assets/treasure_cards/RatOnAStick.png", 1, None, "hands"),
            Item("Short Wide Armor", "assets/treasure_cards/ShortWideArmor.png", 3, 400, "armor"),
            Item("Singing & Dancing Sword", "assets/treasure_cards/SingingAndDancingSword.png", 2, 400),
            Item("Slimy Armor", "assets/treasure_cards/SlimyArmor.png", 1, 200, "armor"),
            Item("Sneaky Bastard Sword", "assets/treasure_cards/SneakyBastardSword.png", 2, 400, "hands"),
            Item("Spiky Knees", "assets/treasure_cards/SpikyKnees.png", 1, 200),
            Item("Staff of Napalm", "assets/treasure_cards/StaffOfNapalm.png", 5, 800),
            Item("Stepladder", "assets/treasure_cards/Stepladder.png", 3, 400),
            Item("Swiss Army Polearm", "assets/treasure_cards/SwissArmyPolearm.png", 4, 600),               

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

        # Add races with special abilities
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

        print(f"Treasure deck initialized with {len(self.cards)} cards")
        self.shuffle()
        print("Treasure deck shuffled")

# TODO: Falta colocar os Buffs