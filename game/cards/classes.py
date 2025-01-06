from game.card import Class, ClassTypes


CLASSES = [
    Class(
        name="Warrior",
        image="assets/door_cards/Warrior.png",
        class_type=ClassTypes.WARRIOR,
    ),
    Class(
        name="Cleric",
        image="assets/door_cards/Cleric.png",
        class_type=ClassTypes.CLERIC,
    ),
    Class(
        name="Thief",
        image="assets/door_cards/Thief.png",
        class_type=ClassTypes.THIEF,
    ),
    Class(
        name="Wizard",
        image="assets/door_cards/Wizard.png",
        class_type=ClassTypes.WIZARD,
    ),
    Class(
        name="Bard",
        image="assets/door_cards/Bard.png",
        class_type=ClassTypes.BARD,
    ),
]
