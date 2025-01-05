from game.card import DoorBuff
from game.cards.door_buff_effect import *
from game.cards.buff_restriction import *


DOOR_BUFFS = [
    DoorBuff(
        name="Baby",
        image="assets/door_cards/Baby.png",
        effect=IncreaseMonsterLevelBuff(-5),
        restriction=OnlyInCombatRestriction(),
        after_death_effect=DrawExtraTreasureBuff(-1)
    ),
    DoorBuff(
        name="Intelligent",
        image="assets/door_cards/Intelligent.png",
        effect=IncreaseMonsterLevelBuff(5),
        restriction=OnlyInCombatRestriction(),
        after_death_effect=DrawExtraTreasureBuff(1)
    ),
    DoorBuff(
        name="Enraged",
        image="assets/door_cards/Enraged.png",
        effect=IncreaseMonsterLevelBuff(5),
        restriction=OnlyInCombatRestriction(),
        after_death_effect=DrawExtraTreasureBuff(1)
    ),
    DoorBuff(
        name="Ancient",
        image="assets/door_cards/Ancient.png",
        effect=IncreaseMonsterLevelBuff(10),
        restriction=OnlyInCombatRestriction(),
        after_death_effect=DrawExtraTreasureBuff(2)
    ),
    DoorBuff(
        name="Humongous",
        image="assets/door_cards/Humongous.png",
        effect=IncreaseMonsterLevelBuff(10),
        restriction=OnlyInCombatRestriction(),
        after_death_effect=DrawExtraTreasureBuff(2)
    ),
    DoorBuff(
        name="HalfA...",
        image="assets/door_cards/HalfA....png",
        effect=IncreaseMonsterLevelBuff(-5),
        restriction=OnlyInCombatRestriction(),
        after_death_effect=DrawExtraTreasureBuff(-1)
    )
]