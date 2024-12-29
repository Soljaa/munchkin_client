from enum import Enum, auto
from game.dice import Dice
from game.deck import DoorDeck, TreasureDeck
from game.player import Player
from game.card import CardType
from game.combat import Combat


class GamePhase(Enum):
    SETUP = auto()
    KICK_DOOR = auto()
    LOOK_FOR_TROUBLE = auto()
    LOOT_ROOM = auto()
    COMBAT = auto()
    CHARITY = auto()


class EndGameException(Exception):
    pass


class GameState:
    _instance = None

    def __init__(self):
        GameState._instance = self
        self.door_deck = DoorDeck()
        self.treasure_deck = TreasureDeck()
        self.players: list[Player] = []
        self.dice = Dice()
        self.current_player_index = 0
        self.phase = GamePhase.SETUP
        self.current_combat = None

    @staticmethod
    def get_instance():
        return GameState._instance

    def add_player(self, name, img_dir):
        player = Player(name, img_dir)
        self.players.append(player)
        # Draw initial hand
        for _ in range(4):
            player.draw_card(self.door_deck)
            player.draw_card(self.treasure_deck)

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

        for curse in self.current_player().curse: # As curses recebidas são aplicadas no início do turno
            curse.apply_effect(self.current_player())
        self.current_player().clean_curses()

        self.phase = GamePhase.SETUP
        self.set_combat(None)

    def current_player(self):
        return self.players[self.current_player_index]

    def kick_down_door(self):
        print(f"Attempting to kick door in phase: {self.phase}")
        if self.phase != GamePhase.KICK_DOOR:
            print("Wrong phase for kicking door")
            return False

        card = self.door_deck.draw()
        if not card:
            print("No card drawn, reshuffling deck")
            self.door_deck.shuffle()
            card = self.door_deck.draw()
            if not card:
                print("Still no card after shuffle")
                return False

        print(f"Drew card: {card.name} of type {card.card_type}")
        if card.card_type == CardType.MONSTER:
            print("Monster encountered! Initializing combat...")
            self.set_combat(Combat(self.current_player(), card))
            self.set_game_phase(GamePhase.COMBAT) # Caso tenha saído um monstro, seta a fase de combate
            print(f"Combat initialized with monster: {card.name}")
        # handle curse
        elif card.card_type == CardType.CURSE:
            card.apply_effect(self.current_player())
            print(card.name)
        return True

    def resolve_combat(self):
        if not self.current_combat:
            return False
        try:
            success, result = self.current_combat.resolve_combat() # Ve se player ganha ou perde. Retorno: success(True ou False), result(informações do monstro)
            if success: # Se player ganhou o combate
                self.current_player().level_up()
                if self.current_player().level >= 10: 
                    raise EndGameException
                # Draw treasure cards based on monster's treasure value
                for _ in range(result['treasure']):
                    card = self.treasure_deck.draw() # Retira uma carda do deck de tesouro
                    if card: # Se foi retirado a carta
                        self.current_player().hand.append(card) # Coloca ela na mão do player
            else: # Se perdeu combate
                # Handle bad stuff
                if result['bad_stuff'] and result['bad_stuff'] is str:
                    if "level" in result['bad_stuff'].lower():
                        self.current_player().level_down()
            print(result['message'])

            self.current_combat = None
        except EndGameException:
            raise

    def loot(self):
        print(f"Attempting to loot the room in phase: {self.phase}")
        if self.phase != GamePhase.LOOT_ROOM:
            print("Wrong phase for looting the room")
            return False
        
        card = self.treasure_deck.draw()
        if not card:
            print("No card drawn, reshuffling deck")
            self.door_deck.shuffle()
            card = self.door_deck.draw()
            if not card:
                print("Still no card after shuffle")
                return False
        
        self.current_player().hand.append(card)

        return True

    def look_for_trouble(self, monster):
        print("Monster selected! Initializing combat...")
        self.set_combat(Combat(self.current_player(), monster))
        self.set_game_phase(GamePhase.COMBAT)
        print(f"Combat initialized with monster: {monster.name}")
        return True

    def set_game_phase(self, new_phase):
        if new_phase in [phase for phase in GamePhase]:
            self.phase = new_phase
            print("New phase set:", self.phase)

    def set_combat(self, combat):
        self.current_combat = combat
        if self.current_combat:
            print("New combat:", self.current_combat.__dict__)

    def play_charity_phase(self, died=False):
        # add delay or animation
        self.set_game_phase(GamePhase.CHARITY)
        donation_cards = self.players[self.current_player_index].hand \
            if died else self.players[self.current_player_index].donate_cards()
        lowest_cards_players = self.get_lowest_cards_players()
        if len(donation_cards) == 1:
            lowest_cards_players[0].hand += donation_cards
        distribution = distribute_cards(lowest_cards_players, donation_cards)
        for player, card_array in distribution.items():
            player.hand += card_array
        return True

    def get_lowest_cards_players(self):
        curr_player = self.players[self.current_player_index]
        players_minus_current = [player for player in self.players if player != curr_player]
        min_cards = min(len(player.hand) for player in players_minus_current)
        return [player for player in players_minus_current if len(player.hand) == min_cards]


# donation helper function move to utils
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
