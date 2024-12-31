from game.game_phases.game_phases import GamePhases
from game.game_state import GamePhase


class CharityPhase(GamePhases):
    def __init__(self, game_state, renderer):
        super().__init__(game_state)  # Inicializa a classe base
        self.players = game_state.players
        self.current_player_index = game_state.current_player_index
        self.renderer = renderer

    def run(self, died=False):
        print("Executing Charity Phase")
        self.game_state.set_game_phase(GamePhase.CHARITY)
        self.renderer.set_message("Doing charity... Redistributing cards")

        current_player = self.players[self.current_player_index]
        donation_cards = current_player.hand if died else current_player.donate_cards()
        lowest_cards_players = self.get_lowest_cards_players()

        if len(donation_cards) == 1:
            print(f"Distributing single card to {lowest_cards_players[0].name}")
            lowest_cards_players[0].hand += donation_cards
            distribution = {lowest_cards_players[0]: donation_cards}
        else:
            print(f"Distributing {len(donation_cards)} cards among {len(lowest_cards_players)} players")
            distribution = self.distribute_cards(lowest_cards_players, donation_cards)

        for player, card_array in distribution.items():
            print(f"Player {player.name} receives {len(card_array)} cards")
            player.hand += card_array

        # Exclui o jogador atual da lista de jogadores antes de renderizar
        other_players = [player for player in self.players if player != current_player]
        
        # Chama a renderização para exibir todos os jogadores, exceto o atual
        self.renderer.draw_charity_fase_transition(other_players, distribution)

        return True


    def get_lowest_cards_players(self):
        print("Identifying players with the fewest cards")
        current_player = self.players[self.current_player_index]
        players_minus_current = [player for player in self.players if player != current_player]
        min_cards = min(len(player.hand) for player in players_minus_current)
        return [player for player in players_minus_current if len(player.hand) == min_cards]

    @staticmethod
    def distribute_cards(players, cards):
        if not players or not cards:
            return {player: [] for player in players}  # Retorna dicionário vazio para cada jogador

        distribution = {player: [] for player in players}
        num_players = len(players)

        for i, card in enumerate(cards):
            # Atribuir a carta ao jogador correspondente
            current_player = players[i % num_players]
            distribution[current_player].append(card)

        return distribution