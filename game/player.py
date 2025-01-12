from game.card import CardType, ClassTypes, RaceTypes
from game.death import Death
import random


class Player:
    def __init__(self, name, avatar_img_dir, gender):
        self.name = name
        self.avatar_img_dir = avatar_img_dir
        self.level = 1
        self.combat_strength = 0
        self.hand = []
        self.equipped_items = []
        self.race = RaceTypes.HUMAN
        self.gold = 0  # Adicionando o atributo gold inicializado em 0
        self.class_ = None  # estava como array por causa do super munchkin, mas ele foi cancelado
        self.gender = gender
        # adicionar referencia a efeitos ativos, com referencia aos itens donos do efeito e
        # ver se vale dividir em etapas de aplicação dos efeitos como efeitos que se aplicam no setup,
        # ou no combate, ou na fuga e etc

    def calculate_combat_strength(self):
        base_strength = self.level
        item_bonus = sum(item.bonus for item in self.equipped_items)
        return base_strength + item_bonus

    def equip_item(self, item):
        from game.card import Item, Race, Class
        if isinstance(item, Item):
            # 2 hands restriction
            if item.two_hands:
                for equipped_item in self.equipped_items:
                    if equipped_item.slot == "hands":
                        return False

            # big item restriction
            if item.big:
                for equipped_item in self.equipped_items:
                    if equipped_item.big:
                        return False

            # type limit
            if item.slot == "hands":
                hands_limit = 0
                for equipped_item in self.equipped_items:
                    if equipped_item.two_hands:
                        return False
                    if equipped_item.slot == "hands":
                        hands_limit += 1
                if hands_limit > 1:
                    return False

            if item.slot == "head":
                for equipped_item in self.equipped_items:
                    if equipped_item.slot == "head":
                        return False

            if item.slot == "armor":
                for equipped_item in self.equipped_items:
                    if equipped_item.slot == "armor":
                        return False

            if item.slot == "feet":
                for equipped_item in self.equipped_items:
                    if equipped_item.slot == "feet":
                        return False

            # race restrictions
            if item.race_required:
                if not self.race or self.race == RaceTypes.HUMAN:
                    return False
                if self.race.race_type != item.race_required:
                    return False

            if item.races_prohibited:
                if self.race and self.race != RaceTypes.HUMAN and self.race in item.races_prohibited:
                    return False

            # class restrictions
            if item.class_required:
                if not self.class_:
                    return False
                if self.class_.class_type != item.class_required:
                    return False

            if item.classes_prohibited:
                if self.class_ and self.class_.class_type in item.classes_prohibited:
                    return False

            # gender restrictions
            if item.gender_required:
                if self.gender != item.gender_required:
                    return False

            if item.genders_prohibited:
                if self.gender in item.genders_prohibited:
                    return False

            self.equipped_items.append(item)
            self.hand.remove(item)
        return True

    def unequip_item(self, item):
        if item in self.equipped_items:
            self.equipped_items.remove(item)
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

        if card.type == CardType.DOOR_BUFF or card.type == CardType.CURSE or card.type == CardType.MONSTER or card.type == CardType.RACE or card.type == CardType.CLASS:
            door_deck.discard_pile.append(card)
        if card.type == CardType.TREASURE_BUFF or card.type == CardType.ITEM:
            treasure_deck.discard_pile.append(card)

    def play_card(self, card, game_state):
        from ui.game_renderer import GameRenderer        
        game_renderer = GameRenderer.get_instance()

        if (card.type == CardType.CURSE):
            print('Clicou em curse')
            player_target = game_renderer.draw_selection_player(game_state.players, game_state.current_player(), "Selecione o alvo da maldição")
            if not player_target:
                return
            card.apply_effect(player_target)
        elif card.type == CardType.RACE:
            print('Clicou em race')
            self.replace_race(card)
        elif card.type == CardType.CLASS:
            print('Clicou em class')
            self.replace_class(card)
        elif card.type == CardType.MONSTER:
            print('Clicou em monster')
            return
        elif (card.type == CardType.DOOR_BUFF):
            print('Clicou em door_buff')
            card.apply_effect(game_state.current_combat.monster) # OBS: A princípio, os targets do door_buff são os monstros do combate (tem restrição de só jogar em combate)
        elif (card.type == CardType.TREASURE_BUFF):
            print('Clicou em treasure_buff')
            card.apply_effect(self)

        self.add_to_discard_pile(card)

        if card in self.hand:
            self.hand.remove(card)
            return True
        return False

    def level_up(self):
        if self.level < 10:
            self.level += 1

    def level_down(self, value=1):
        if self.level > 1:
            self.level -= value
        if self.level < 1:
            self.level = 1

    def remove_class(self):
        if self.class_:
            self.add_to_discard_pile(self.class_)
            for item in self.equipped_items:
                if item.class_required and item.class_required == self.class_.class_type:
                    self.unequip_item(item)
            self.class_ = None

    def replace_class(self, card):
        self.remove_class()
        self.class_ = card

    def remove_race(self):
        if self.race != RaceTypes.HUMAN:
            self.add_to_discard_pile(self.race)
            for item in self.equipped_items:
                if item.race_required and item.race_required == self.race.race_type:
                    self.unequip_item(item)
        self.race = RaceTypes.HUMAN

    def replace_race(self, card):
        self.remove_race()
        self.race = card

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
                          if self.class_ and item.class_required == self.class_.class_type]
        
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

    def remove_all_hand_class_cards(self):
        items_to_remove = [item for item in self.hand if hasattr(item, 'class_required') and item.class_required == self.class_.class_type] # Adição da verificação se a carta tem o atributo "class_required", pois o DoorBuff não tem e dava bug.

        
        for item in items_to_remove:
            self.add_to_discard_pile(item)
            self.hand.remove(item)

    def lose_all_class_cards(self):
        self.lose_all_equipped_class_items()
        self.remove_all_hand_class_cards()

    def shuffle_hand(self):
        random.shuffle(self.hand)

    def donate_cards(self, max_hand_size=5):  # retorna a lista de cartas para doação ou [] se tiver 5 cartas
        hand_size = len(self.hand)
        if hasattr(self.race, 'race_type') and self.race.race_type == RaceTypes.DWARF: # Se for Dwarf, a mão pode ter 6 cartas
            max_hand_size = 6
        if hand_size > max_hand_size:
            self.shuffle_hand()
            donation_cards = [self.hand.pop() for _ in range(hand_size - max_hand_size)]
            return donation_cards
        return []

    def get_player_race(self):
        if self.race and self.race != RaceTypes.HUMAN:
            return self.race.race_type.value
        if self.race:
            return self.race.value
        return "Sem raça"