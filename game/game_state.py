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
        self.phase = GamePhase.SETUP
        self.set_combat(None)

    def current_player(self):
        return self.players[self.current_player_index]

    def resolve_combat(self):
        if not self.current_combat:
            return False
        try:
            success, result = self.current_combat.resolve_combat() # Ve se player ganha ou perde. Retorno: success(True ou False), result(informações do monstro)
            if success: # Se player ganhou o combate
                # TODO: Pode desenhar o boneco vencendo a luta contra o monstro (não consegui pois a IA tem filtro para não desenhar coisas "sensíveis", nesse caso é a luta, guerra, batalha)
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

    def set_game_phase(self, new_phase):
        if new_phase in [phase for phase in GamePhase]:
            self.phase = new_phase
            print("New phase set:", self.phase)

    def set_combat(self, combat):
        self.current_combat = combat
        if self.current_combat:
            print("New combat:", self.current_combat.__dict__)
