from game.card import TreasureBuff
from game.cards.buff_restriction import *
from game.cards.treasure_buff_effect import *

TREASURE_BUFFS = [
    TreasureBuff(
        name="Instant Wall",
        image="assets/treasure_cards/InstantWall.png",
        effect=EveryoneScapesBuff(),
        restriction=OnlyInCombatRestriction()
    ),
]
