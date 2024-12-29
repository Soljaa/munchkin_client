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
        return card

    def play_card(self, card):
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

    #TODO
    def lose_items(self, qty):
        pass

    # TODO
    def lose_all_class_items(self):
        pass

    #TODO
    def lose_all_class_cards(self):
        pass

    #TODO
    def lose_all_race_cards(self):
        pass

    #TODO
    def lose_all_items(self):
        pass

    #TODO
    def lose_equipped_headgear(self):
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

