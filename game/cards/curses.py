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
        effect=LoseEquippedItemBadStuff('feet')
    ),
    Curse(
        name="Curse! Lose The Armor You Are Wearing",
        image="assets/door_cards/Curse!LoseTheArmorYouAreWearing.png",
        effect=LoseEquippedItemBadStuff('armor')
    ),
    Curse(
        name="Curse! Lose The Headgear You Are Wearing",
        image="assets/door_cards/Curse!LoseTheHeadgearYouAreWearing.png",
        effect=LoseEquippedItemBadStuff('head')
    ),
    Curse(
        name="Curse! Lose Two Cards",
        image="assets/door_cards/Curse!LoseTwoCards.png",
        effect=LoseHandCardsBadStuff(2)
    ),
    Curse(
        name="Curse! Duck of Doom",
        image="assets/door_cards/Curse!DuckOfDoom.png",
        effect=LoseLevelBadStuff(2)
    ),
]
