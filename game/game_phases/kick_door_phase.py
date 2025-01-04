from game.card import CardType
from game.combat import Combat
from game.game_phases.combat_phase import CombatPhase
from game.game_phases.game_phases import GamePhases
from game.game_state import GamePhase


class KickDoorFase(GamePhases):
    def __init__(self, game_state, renderer):
        super().__init__(game_state)  # Inicializa a classe base
        self.door_deck = game_state.door_deck  # Baralho de tesouros
        self.current_player = game_state.current_player()  # Jogador atual
        self.renderer = renderer

    def run(self):
        self.game_state.set_game_phase(GamePhase.KICK_DOOR)
        print(f"Attempting to kick door in phase: {self.game_state.phase}")

        # Desenha a carta
        card = self.door_deck.draw()
        if not card:
            print("No card drawn, reshuffling deck")
            self.door_deck.shuffle()
            card = self.door_deck.draw()
            if not card:
                print("Still no card after shuffle")
                return False

        print(f"Drew card: {card.name} of type {card.type}")
        
        # Se for monstro, inicia combate
        if card.type == CardType.MONSTER:
            combat_phase = CombatPhase(self.game_state, card, self.renderer)
            combat_phase.run()
        
        # Se for maldição, aplica o efeito
        elif card.type == CardType.CURSE:
            print(f"Cursed! {card.name}")
            card.effect.apply(self.current_player)

        return True
