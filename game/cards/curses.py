from game.card import Curse
from game.cards.curse_effect import *
from game.cards.monster_bad_stuff import *


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
    Curse(
        name="Curse! Change Class",
        image="assets/door_cards/Curse!ChangeClass.png",
        effect=ChangeClassCurseEffect()
    ),
    Curse(
        name="Curse! Change Race",
        image="assets/door_cards/Curse!ChangeRace.png",
        effect=ChangeRaceCurseEffect()
    ),
    Curse(
        name="Curse! Lose Your Race",
        image="assets/door_cards/Curse!LoseYourRace.png",
        effect=LoseRaceCurseEffect()
    ),
    Curse(
        name="Curse! Lose Your Class",
        image="assets/door_cards/Curse!LoseYourClass.png",
        effect=LoseClassCurseEffect()
    ),
    Curse(
        name="Curse! Dying Curse",
        image="assets/door_cards/Curse!DyingCurse.png",
        effect=ApplyDiscardCardBadStuffCurseEffect()
    ),
    Curse(
        name="Curse! Lose The Footgear You Are Wearing",
        image="assets/door_cards/Curse!LoseTheFootgearYouAreWearing.png",
        effect=LoseEquippedItemBadStuff('footgear')
    ),
]
