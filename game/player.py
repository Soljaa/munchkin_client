class Player:
    def __init__(self, name, img_dir):
        self.name = name
        self.img_dir = img_dir
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

    def level_down(self):
        if self.level > 1:
            self.level -= 1
