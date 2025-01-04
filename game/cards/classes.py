from game.card import Class, ClassTypes

# TODO: imagens. Habilidades vamos ignorar?
CLASSES = [
    Class(
        name="Warrior",
        image="",
        special_ability="Pode descartar até 3 cards em combate e cada um aumenta 1 de bonus. Vence empates no combate.",
        class_type=ClassTypes.WARRIOR,
    ),
    Class(
        name="Cleric",
        image="",
        special_ability="Para toda carta viradas pra cima que será comprada, pode escolher comprar uma carta do topo da pilha de descarte; e nesse caso descarta uma carta da sua mão. Pode descartar até 3 cards em combate contra Undead e cada uma aumenta 3 de bonus.",
        class_type=ClassTypes.CLERIC,
    ),
    Class(
        name="Thief",
        image="",
        special_ability="Para cada combate e para cada jogador, pode descartar 1 carta para reduzir 2 de dano no combate dele. Pode descartar 1 carta para rolar rolar um dado, e se tirar mais de 4 rouba um item pequeno de alguém, se menos, perde um nível.",
        class_type=ClassTypes.THIEF,
    ),
    Class(
        name="Wizard",
        image="",
        special_ability="Após rolar o dado de Run Away, pode descartar até 3 cards e cada um aumenta 1 de bônus. Pode descartar a mão toda (mínimo 3 cards) para matar 1 monstro sem ganhar níveis.",
        class_type=ClassTypes.WIZARD,
    ),
    Class(
        name="Bard",
        image="",
        special_ability="No combate do seu turno, pode quantas vezes quiser descartar 1 card e escolher um oponente: se seu dado for maior, ele tem que te ajudar sem pedir por recompensa; não pode vencer o jogo com isso. Quando vencer um combate no seu turno, compra 2 tesouros e descarta um.",
        class_type=ClassTypes.BARD,
    ),
]
