from game.game_phases.game_phases import GamePhases
from game.game_state import GamePhase


class LootRoomPhase(GamePhases):
    def __init__(self, game_state):
        super().__init__(game_state)  
        self.treasure_deck = game_state.treasure_deck  
        self.current_player = game_state.current_player()  

    def run(self):
        print(f"Attempting to loot the room in phase: {self.game_state.phase}")
        
        # Verifica se a fase atual é LOOT_ROOM
        if self.game_state.phase != GamePhase.LOOT_ROOM:
            print("Wrong phase for looting the room")
            return False

        # Desenha uma carta do baralho de tesouros
        card = self.treasure_deck.draw()
        if not card:
            print("No card drawn, reshuffling deck")
            self.treasure_deck.shuffle()
            card = self.treasure_deck.draw()
            if not card:
                print("Still no card after shuffle")
                return False
        
        # Adiciona a carta à mão do jogador atual
        print(f"Player {self.current_player.name} looted: {card.name}")
        self.current_player.hand.append(card)

        return True
