from game.card import Curse
from game.cards.curse_effect import *
from game.cards.monster_bad_stuff import LoseLevelBadStuff

CURSES = [       
    Curse(
        name="Curse! Lose 1 Level",
        image="assets/door_cards/Curse!LoseALevel1.png",
        effect=LoseLevelBadStuff(1)
    ),
    Curse(
        name="Curse! Lose 2 Levels",
        image="assets/door_cards/Curse!LoseALevel2.png",
        effect=LoseLevelBadStuff(2)
    ),
    # TODO: Falta png
    Curse(
        name="Curse! Dying Curse",
        image="assets/door_cards/Curse!DyingCurse.png",
        effect=ApplyDiscardCardBadStuffCurseEffect()
    )
]
