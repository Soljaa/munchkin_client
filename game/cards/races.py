from game.card import Race, RaceTypes


RACES = [
    Race(
        name="Dwarf",
        image="assets/door_cards/Dwarf.png",
        special_ability="Pode ter 6 cards na mão (era 5). Pode carregar infinitos itens grandes", # TODO: ainda não separamos o que é item grande (Big). Talvez vale ignorar
        race_type=RaceTypes.DWARF,
    ),
    Race(
        name="Elf",
        image="assets/door_cards/Elf.png",
        special_ability="+1 para Run Away. Sobe de level para cada monstro que você ajudar alguém a matar",
        race_type=RaceTypes.ELF,
    ),
    Race(
        name="Halfling",
        image="assets/door_cards/Halfling.png",
        special_ability="Pode vender 1 item todo turno pelo dobro do preço. Se falhar o primeiro Run Away, pode descartar uma carta e tentar novamente",
        race_type=RaceTypes.HALFlING,
    ),
    Race(
        name="Orc",
        image="assets/door_cards/Orc.png",
        special_ability="Pode sempre perder 1 nível para ignorar uma curse a partir de 2 níveis. Quando derrota sozinho um monstro 11+, sobe um nível.",
        race_type=RaceTypes.ORC,
    ),
]
