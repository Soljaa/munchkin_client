from game.card import Monster
from game.cards.monster_effect import *
from game.cards.monster_bad_stuff import *


MONSTERS = [
        Monster(
            name="3,872 Orcs",
            image="assets/door_cards/3872Orcs.png",
            level=10,
            treasure=3,
            effect=IncreaseMonsterLevelEffect('Dwarf', 6),
            bad_stuff=OrcsBadStuff(),
        ),
        # Amazon -->  se for mulher, não ter combate e dar tesouro
        Monster(
            name="Auntie Paladin",
            image="assets/door_cards/AuntiePaladin.png",
            level=18,
            treasure=4,
            effect=IncreaseMonsterLevelEffect("Cleric", 5), # TODO: também é +5 contra male character.
            bad_stuff=CompositeBadStuff(LoseEquippedItemBadStuff('armor'), LoseLevelBadStuff(3)),
            reward_two_levels=True
        ),
        # Bad Ass --> #TODO --> viável
        Monster(
            name="Bigfoot",
            image="assets/door_cards/Bigfoot.png",
            level=12,
            treasure=3,
            effect=CompositeEffect(
                IncreaseMonsterLevelEffect("Dwarf", 3),
                IncreaseMonsterLevelEffect("Halfling", 3),
            ),
            bad_stuff=LoseEquippedItemBadStuff('headgear'),
        ),
        # Big Fat Hairy Dale --> precisaria de multiplayer
        # Bipolar Bear --> roda dado, se for impar foge. Rola dado, se for par compra um tesouro face up?!
        Monster(
            name="Bullrog",
            image="assets/door_cards/Bullrog.png",
            level=18, 
            treasure=5, 
            effect=CompositeEffect(NotPursueLevelEffect(4)),
            bad_stuff=DeathBadStuff(),
            reward_two_levels=True
        ),
        # Crabs --> tem que impedir fugir dele
        Monster(
            name="Drooling Slime",
            image="assets/door_cards/DroolingSlime.png",
            level=1,
            treasure=1,
            effect=IncreaseMonsterLevelEffect('Elf', 4),
            bad_stuff=LoseEquippedItemOrLevelBadStuff('feet', 1)
        ),
        Monster(name="Face Sucker",
                image="assets/door_cards/FaceSucker.png",
                level=8,
                treasure= 2, 
                effect=CompositeEffect(IncreaseMonsterLevelEffect("Elf", 6)),
                bad_stuff=CompositeBadStuff(
                    LoseEquippedItemBadStuff('headgear'),
                    LoseLevelBadStuff(1),
                ),
            ),    
        # Floating Nose --> complicado de fazer
        # Flying Frogs --> -1 de Run Away
        # Gazebo --> não pode ajuda contra essa carta
        # Gelatinous Octahedron --> +1 Run Away e tem que dropar item grande
        # Ghoulfiends --> Itens ou bonus não podem ajudar pra matar ele
        # Ghost Writer --> #TODO viável, não tem hireling no deck pro badstuff
        Monster(
            name="Hairy Potter",
            image="assets/door_cards/HairyPotter.png",
            level=15,
            treasure=4,
            effect=CompositeEffect(IncreaseMonsterLevelEffect('Wizard', 4), IncreaseMonsterLevelEffect('Elf', -3), NotPursueLevelEffect(2)),
            bad_stuff=LoseAllClassItemsBadStuff(),
            reward_two_levels=True
        ),
        Monster(
            name="Harpies",
            image="assets/door_cards/Harpies.png",
            level=4,
            treasure=2,
            effect=IncreaseMonsterLevelEffect("Wizard", 5),
            bad_stuff=LoseLevelBadStuff(2)
        ),
        # Hippogriff --> impossivel sem multiplayer
        # Insurance Salesman --> level não conta pra matar ele
        # Katrina -> descarta todos menos os Big
        Monster(
            name="King Tut",
            image="assets/door_cards/KingTut.png",
            level=16,
            treasure=4,
            effect=CompositeEffect(
                NotPursueLevelEffect(3), 
                PlayerLoseLevelsIfLevelIsBiggerThanMonsterEffect(2)
            ),
            bad_stuff=CompositeBadStuff(
                LoseItemsBadStuff(),
                LoseHandCardsBadStuff(),
            ),
        ),        
        #Lame Goblin --> +1 Run Away
        #Large Angry Chicken --> detectar se matou com fire ou flame
        #Lawyers --> outro player comprar carta sua  
        Monster(
            name="Leperchaun",
            image="assets/door_cards/Leperchaun.png",
            level=4,
            treasure=2,
            effect=CompositeEffect(IncreaseMonsterLevelEffect("Elf", 5)),
            bad_stuff=LoseItemsBadStuff(2),
        ),
        Monster(
            name="Maul Rat",
            image="assets/door_cards/MaulRat.png",
            level=1,
            treasure=1,
            effect=CompositeEffect(IncreaseMonsterLevelEffect("Cleric", 3)),
            bad_stuff=LoseLevelBadStuff(1),
        ),
        # Misplacer Beast --> outros compram suas cartas
        Monster(
            name="Medusa",
            image="assets/door_cards/Medusa.png",
            level=19,
            treasure=5,
            effect=IncreaseMonsterLevelEffect("Elf", 4),
            bad_stuff=DeathBadStuff(), # TODO: E não permitir ninguém pegar os items.
            reward_two_levels=True
        ),
        # Mr. Bones --> obriga a fugir. Perde nível se escapar. Ele é undead
        # Net Troll --> player de maior level pega algum item seu 
        # Male CHauvinist Pig --> # extra treasure pra cada female ajudando, parece viável
        # Pit Bull --> tem que jogar um item (wand, pole ou staff) pra ganhar

        # Platycore #TODO Viável!
        #Monster("Platycore", "assets/door_cards/Platycore.png", 6, 2, "X"),

        # Polly Hedron --> falha próximo Run Away
        Monster(
            name="Plutonium Dragon",
            image="assets/door_cards/PlutoniumDragon.png",
            level=20,
            treasure=5, 
            effect=NotPursueLevelEffect(5),
            bad_stuff=DeathBadStuff(),
            reward_two_levels=True
        ),
        Monster(
            name="Potted Plant",
            image="assets/door_cards/PottedPlant.png",
            level=1,
            treasure=1, 
            effect= MoreTreasureEffect(1, "Elf"),
            bad_stuff=None
        ),

        # Pukachu --> extra level se derrotar sem usar ajuda ou bonus

        # Shrieking Geek #TODO Viável!
        #Monster("Shrieking Geek", "assets/door_cards/ShriekingGeek.png", 6, 2, "X"),

        # Snails on Speed --> -2 Run Away
        Monster(
            name="Squidzilla", 
            image="assets/door_cards/Squidzilla.png", 
            level=18, 
            treasure=4, 
            effect=CompositeEffect(IncreaseMonsterLevelEffect('Elf', 4), NotPursueLevelEffect(4, exclude_race='Elf')), 
            bad_stuff=DeathBadStuff(),
            reward_two_levels=True
        ),
        # Stoned Golem --> escolhe lugar com ele ou não
        # Tequila Mockingbird --> descarta 2 cards de sua escolha
        # The Dead Sea Trolls --> +1 Run away
        # Tongue Demon --> voce escolher 1 carta e ela é descartada antes do combate
        Monster(
            name="Undead Horse",
            image="assets/door_cards/UndeadHorse.png", 
            level=4, 
            treasure=2,
            effect=IncreaseMonsterLevelEffect("Dwarves", 5),
            bad_stuff=LoseLevelBadStuff(2),
        ), # TODO: Ele é undead
        
        # Unspeakably Awful Indescriblabe Horror #TODO Viável!
        #Monster("Unspeakably Awful Indescribable Horror", "assets/door_cards/UnspeakablyAwfulIndescribableHorror.png", 14, 4, "X"),
        # Wannabe Vampire --> Cleric dá instakill nele sem ganhar nível.   --> podemos reduzir vida do monstro se for clerigo. Mas como evitar level increase?
        
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
            reward_two_levels=True
        )
    ]
    