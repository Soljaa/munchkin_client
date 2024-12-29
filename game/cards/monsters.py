from game.card import Monster
from game.cards.monster_effect import *
from game.cards.monster_bad_stuff import *

MONSTERS = [
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
        # TODO: Falta png
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
            effect=CompositeEffect(
                IncreaseMonsterLevelEffect("Dwarf", 3),
                IncreaseMonsterLevelEffect("Halfling", 3),
            ),
            bad_stuff=LoseTheEquippedHeadgearBadStuff,
        ),
        #Bullrog
        Monster(
            name="Bullrog",
            image="assets/door_cards/Bullrog.png",
            level=18, 
            treasure=5, 
            effect=CompositeBadStuff(NotPursueLevelEffect(4)),
            bad_stuff=DeathBadStuff(),
        ),
        
        #Crabs
        Monster("Crabs", "assets/door_cards/Crabs.png", level=1, treasure=1, bad_stuff=None),
        # Drooling Slime #TODO
        Monster("Drooling Slime", "assets/door_cards/DroolingSlime.png", 1, 1, "X"),
        
        #Face Sucker
        Monster(name="Face Sucker",
                image="assets/door_cards/FaceSucker.png",
                level=8,
                treasure= 2, 
                effect=CompositeEffect(IncreaseMonsterLevelEffect("Elf", 6)),
                bad_stuff=CompositeBadStuff(
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
            name="King Tut",
            image="assets/door_cards/KingTut.png",
            level=16,
            treasure=4,
            effect=CompositeEffect(
                NotPursueLevelEffect(3), 
                PlayerLoseLevelsIfLevelIsBiggerThanMonsterEffect(2)
            ),
            bad_stuff=LoseAllItemsBadStuff(),
        ),
        
        #Lame Goblin #TODO
        Monster("Lame Goblin", "assets/door_cards/LameGoblin.png", 1, 1, "X"),
        #Large Angry Chicken #TODO
        Monster("Large Angry Chicken", "assets/door_cards/LargeAngryChicken.png", 2, 1, "X"),
        #Lawyers #TODO
        Monster("Lawyers", "assets/door_cards/Lawyers.png", 6, 2, "X"),
        
        #Leperchaun
        Monster(
            name="Leperchaun",
            image="assets/door_cards/Leperchaun.png",
            level=4,
            treasure=2,
            effect=CompositeEffect(IncreaseMonsterLevelEffect("Elf", 5)),
            bad_stuff=LoseItemsBadStuff(2),
        ),
        #Maul Rat
        Monster(
            name="Maul Rat",
                image="assets/door_cards/MaulRat.png",
                level=1,
                treasure=1,
                effect=CompositeEffect(IncreaseMonsterLevelEffect("Cleric", 3)),
                bad_stuff=LoseLevelBadStuff(1),
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
            name="Plutonium Dragon",
            image="assets/door_cards/PlutoniumDragon.png",
            level=20,
            treasure=5, 
            effect=CompositeEffect(NotPursueLevelEffect(5)),
            bad_stuff=DeathBadStuff(),
        ),
        # Potted Plant
        Monster(
            name="Potted Plant",
            image="assets/door_cards/PottedPlant.png",
            level=1,
            treasure=1, 
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
            image="assets/door_cards/UndeadHorse.png", 
            level=4, 
            treasure=2,
            effect=CompositeEffect(IncreaseMonsterLevelEffect("Dwarves", 5)),
            bad_stuff=LoseLevelBadStuff(2),
        ), # TODO: Ele é undead
        
        # Unspeakably Awful Indescriblabe Horror #TODO
        Monster("Unspeakably Awful Indescribable Horror", "assets/door_cards/UnspeakablyAwfulIndescribableHorror.png", 14, 4, "X"),
        # Wannabe Vampire #TODO
        Monster("Wannabe Vampire", "assets/door_cards/WannabeVampire.png", 12, 3, "X"),
        # Wight Brothers
        
        Monster(
            name="Wight Brothers",
            image="assets/door_cards/WightBrothers.png",
            level=16,
            treasure=4,
            effect=CompositeEffect(
                PlayerLoseLevelsIfLevelIsBiggerThanMonsterEffect(2), 
                NotPursueLevelEffect(3)
            ),
            bad_stuff=LoseLevelBadStuff(1),
            
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