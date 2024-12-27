from enum import Enum, auto
from game.deck import DoorDeck, TreasureDeck
from game.player import Player
from game.card import CardType
from game.combat import Combat


class GamePhase(Enum):
    SETUP =  auto()
    KICK_DOOR = auto()
    LOOK_FOR_TROUBLE = auto()
    LOOT_ROOM = auto()
    COMBAT = auto()
    CHARITY = auto()


class GameState:
    def __init__(self):
        self.door_deck = DoorDeck()
        self.treasure_deck = TreasureDeck()
        self.players = []
        self.current_player_index = 0
        self.phase = GamePhase.SETUP
        self.current_combat = None

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
            self.current_combat = Combat(self.current_player(), card)
            self.phase = GamePhase.COMBAT
            print(f"Combat initialized with monster: {card.name}")
        else:
            print("Non-monster card drawn, adding to hand")
            self.current_player().hand.append(card)
            self.phase = GamePhase.LOOK_FOR_TROUBLE
        return True

    def resolve_combat(self):
        if not self.current_combat:
            return False
        
        success, result = self.current_combat.resolve_combat()
        if success:
            self.current_player().level_up()
            # Draw treasure cards based on monster's treasure value
            for _ in range(result['treasure']):
                card = self.treasure_deck.draw()
                if card:
                    self.current_player().hand.append(card)
            print(f"Combat won! Gained {result['treasure']} treasure(s)")
        else:
            # Handle bad stuff
            print(f"Combat lost! {result['bad_stuff']}")
            if "level" in result['bad_stuff'].lower():
                self.current_player().level_down()

        self.current_combat = None
        self.phase = GamePhase.CHARITY
        return True
