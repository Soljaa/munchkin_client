from game.card import CardType, Monster
from game.cards.monster_bad_stuff import LoseLevelBadStuff
from game.cards.monster_effect import CompositeEffect, NotPursueLevelEffect, PlayerLoseLevelsIfLevelIsBiggerThanMonsterEffect
from game.combat import Combat
from game.game_phases.game_phases import GamePhases
from game.game_state import GamePhase


class LookForTroublePhase(GamePhases):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.current_player = game_state.current_player()  # Jogador atual

    def run(self):
        """
        Executa a lógica da fase 'Look For Trouble'.
        """
        print("Entering LookForTroublePhase...")
        self.game_state.set_game_phase(GamePhase.LOOK_FOR_TROUBLE)

        # abre modal pro player escolher um monstro da mão, vou mocar com um monstro aleatorio mas
        # tem q fazer a lógica para ver se o cara tem monstro na mão e escolher o monstro mas precisa
        # melhorar o display de cartas primeiro, se nao tiver monstro, mostrar aviso e nao fazer
        # nada, so restando pra ele saquear

        # Simula a seleção de um monstro para combate (deve ser substituído por lógica de seleção real)
        monster_selected = Monster(
            name="Wight Brothers",
            image="assets/door_cards/WightBrothers.png",
            level=16,
            treasure=4,
            effect=CompositeEffect(
                PlayerLoseLevelsIfLevelIsBiggerThanMonsterEffect(2),
                NotPursueLevelEffect(3)
            ),
            bad_stuff=LoseLevelBadStuff(1),
        )

        if not monster_selected:
            print("No monster selected. Loot room instead.")
            print("No monster selected. Exiting LookForTroublePhase.")
            return

        # Inicia o combate
        # Lógica de "look_for_trouble" embutida
        print("Monster selected! Initializing combat...")
        combat = Combat(self.current_player, monster_selected)
        self.game_state.set_combat(combat)  # Define o combate no estado do jogo
        self.game_state.set_game_phase(GamePhase.COMBAT)  # Altera para a fase de combate
        print(f"Combat initialized with monster: {monster_selected.name}")

        # Mensagem de sucesso
        if self.game_state.current_combat:
            print(
                f"Combat started! Fighting {self.game_state.current_combat.monster.name}!"
            )
            print(f"Combat started with monster: {monster_selected.name}")
        else:
            print("Failed to start combat. Try another action.")
            print("Failed to initialize combat. Exiting LookForTroublePhase.")
