from game.card import CardType
from game.combat import Combat
from game.game_phases.game_phases import GamePhases
from game.game_state import GamePhase


class KickDoorFase(GamePhases):
    def __init__(self, game_state):
        super().__init__(game_state)  # Inicializa a classe base
        self.door_deck = game_state.door_deck  # Baralho de tesouros
        self.current_player = game_state.current_player()  # Jogador atual

    def run(self):
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

        print(f"Drew card: {card.name} of type {card.card_type}")
        
        # Se for monstro, inicia combate
        if card.card_type == CardType.MONSTER:
            print("Monster encountered! Initializing combat...")
            self.game_state.set_combat(Combat(self.current_player, card))
            self.game_state.set_game_phase(GamePhase.COMBAT)  # Muda para fase de combate
            print(f"Combat initialized with monster: {card.name}")
        
        # Se for maldição, aplica o efeito
        elif card.card_type == CardType.CURSE:
            print(f"Cursed! {card.name}")
            card.effect.apply(self.current_player)

        return True
