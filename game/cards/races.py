from game.card import Race, RaceTypes


RACES = [
    Race(
        name="Dwarf",
        image="assets/door_cards/Dwarf.png",
        special_ability="Pode ter 6 cards na mão (era 5).",
        race_type=RaceTypes.DWARF,
    ),
    Race(
        name="Elf",
        image="assets/door_cards/Elf.png",
        special_ability="+1 para Run Away.",
        race_type=RaceTypes.ELF,
    ),
    Race(
        name="Halfling",
        image="assets/door_cards/Halfling.png",
        special_ability="Pode vender items por 1.5x o preço.",
        race_type=RaceTypes.HALFlING,
    ),
    Race(
        name="Orc",
        image="assets/door_cards/Orc.png",
        special_ability="Quando derrota sozinho um monstro acima de 10 níveis, sobe um nível.",
        race_type=RaceTypes.ORC,
    ),
]
