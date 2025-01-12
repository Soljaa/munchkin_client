from game.card import TreasureBuff
from game.cards.buff_restriction import *
from game.cards.treasure_buff_effect import *

TREASURE_BUFFS = [
    TreasureBuff(
        name="Instant Wall",
        image="assets/treasure_cards/InstantWall.png",
        value=300,
        effect=EveryoneScapesBuff(),
        restriction=OnlyInCombatRestriction()
    ),
    TreasureBuff(
        name="1.000 Gold Pieces",
        image="assets/treasure_cards/1000GoldPieces.png",
        effect=UpALevelBuff()
    ),
    TreasureBuff(
        name="Bribe GM With Food",
        image="assets/treasure_cards/BribeGMWithFood.png",
        effect=UpALevelBuff()
    ),
    TreasureBuff(
        name="Convenient Addition Error",
        image="assets/treasure_cards/ConvenientAdditionError.png",
        effect=UpALevelBuff()
    ),
    TreasureBuff(
        name="Invoke Obscure Rules",
        image="assets/treasure_cards/InvokeObscureRules.png",
        effect=UpALevelBuff()
    ),
    # TreasureBuff(
    #     name="Steal A Level",
    #     image="assets/treasure_cards/StealALevel.png",
    #     effect=StealALevelBuff()
    # )
]
