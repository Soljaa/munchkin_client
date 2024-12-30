from game.card import CardType
from game.death import Death
import random


class Player:
    def __init__(self, name, avatar_img_dir):
        self.name = name
        self.avatar_img_dir = avatar_img_dir
        self.level = 1
        self.combat_strength = 0
        self.hand = []
        self.equipped_items = []
        self.race = None
        self.class_ = None

    def calculate_combat_strength(self):
        base_strength = self.level
        item_bonus = sum(item.bonus for item in self.equipped_items)
        return base_strength + item_bonus

    def equip_item(self, item):
        from game.card import Item
        if not isinstance(item, Item):
            return False
        if item.equipped or item not in self.hand:
            return False
            
        # Check if player can equip more items
        if len(self.equipped_items) >= 5:  # Basic limit of items
            return False
            
        self.equipped_items.append(item)
        item.equipped = True
        self.hand.remove(item)
        return True

    def unequip_item(self, item):
        if item in self.equipped_items:
            self.equipped_items.remove(item)
            item.equipped = False
            self.hand.append(item)

    def draw_card(self, deck):
        card = deck.draw()
        if card:
            self.hand.append(card)

    def add_to_discard_pile(self, card):
        from game.game_state import GameState
        game_state = GameState.get_instance()

        door_deck = game_state.door_deck
        treasure_deck = game_state.treasure_deck

        if card.card_type == CardType.DOOR_BUFF or card.card_type == CardType.CURSE or card.card_type == CardType.MONSTER or card.card_type == CardType.RACE or card.card_type == CardType.CLASS:
            door_deck.discard_pile.append(card)
        if card.card_type == CardType.TREASURE_BUFF or card.card_type == CardType.ITEM:
            treasure_deck.discard_pile.append(card)

    def play_card(self, card):
        # TODO: para CURSE, abrir opção para escolher qual alvo
        # if card.card_type == CardType.CURSE:
        #     target_player = open_target_menu()
        #     card.apply_effect(target_player)

        self.add_to_discard_pile(card)

        if card in self.hand:
            self.hand.remove(card)
            return True
        return False

    def level_up(self):
        if self.level < 10:
            self.level += 1

    def level_down(self, value=1):
        self.level -= value
        if self.level < 1:
            Death(self).apply()

    def replace_class(self, card):
        self.remove_class()
        self.class_ = card

    def remove_class(self):
        self.add_to_discard_pile(self.class_)
        self.class_ = None
    
    def remove_hand_card(self, card):
        self.add_to_discard_pile(card)
        self.hand.remove(card)

    def lose_all_hand_cards(self):
        for card in self.hand:
            self.remove_hand_card(card)

    def remove_equipped_items(self, quantity=None):
        if quantity:
            random.shuffle(self.equipped_items)
            for item in self.equipped_items[:quantity]:
                item.equipped = False
                self.add_to_discard_pile(item)
            self.equipped_items = self.equipped_items[quantity:]
        else:
            for item in self.equipped_items:
                item.equipped = False
                self.add_to_discard_pile(item)
            self.equipped_items.clear()

    def remove_hand_cards(self, quantity=None):
        if quantity:
            random.shuffle(self.hand)
            for card in self.hand[:quantity]:
                self.add_to_discard_pile(card)
            self.hand = self.hand[quantity:]
        else:
            for card in self.hand:
                self.add_to_discard_pile(card)
            self.hand.clear()

    def lose_all_equipped_class_items(self):
        items_to_remove = [item for item in self.equipped_items 
                          if item.class_required == self.class_]
        
        for item in items_to_remove:
            item.equipped = False
            self.add_to_discard_pile(item)
            self.equipped_items.remove(item)

    def remove_equipped_item_type(self, item_type: str):
        items_to_remove = [item for item in self.equipped_items if item.slot == item_type]
        
        for item in items_to_remove:
            item.equipped = False
            self.add_to_discard_pile(item)
            self.equipped_items.remove(item)

    #TODO
    def lose_all_class_cards(self):
        pass

    #TODO
    def lose_all_race_cards(self):
        pass

    def shuffle_hand(self):
        random.shuffle(self.hand)

    def donate_cards(self, max_hand_size=5):  # retorna a lista de cartas para doação ou [] se tiver 5 cartas
        hand_size = len(self.hand)
        if hand_size > max_hand_size:
            self.shuffle_hand()
            donation_cards = [self.hand.pop() for _ in range(hand_size - max_hand_size)]
            return donation_cards
        return []

