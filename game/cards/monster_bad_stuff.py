from abc import ABC, abstractmethod
from game.death import Death
from game.dice import Dice


class MonsterBadStuff(ABC):
    @abstractmethod
    def apply(self, player) -> None:
        pass

class CompositeBadStuff(MonsterBadStuff):
    def __str__(self):
        return "\n".join([str(bad_stuff) for bad_stuff in self.bad_stuffs])

    def __init__(self, *bad_stuffs: MonsterBadStuff):
        self.bad_stuffs = bad_stuffs
    
    def apply(self, player) -> None:
        for bad_stuff in self.bad_stuffs:
            bad_stuff.apply(player)

class DeathBadStuff(MonsterBadStuff):
    def __str__(self):
        return "Você morre."

    def __init__(self, exclude_race=None):
        self.exclude_race = exclude_race

    def apply(self, player):
        if self.exclude_race and player.race == self.exclude_race:
            return
        
        Death(player).apply()

class OrcsBadStuff(MonsterBadStuff):
    def __str__(self):
        return "Role um dado. 2 ou menos, você morre. Se não, perca o nível do dado."
 
    def apply(self, player) -> None:
        from ui.game_renderer import GameRenderer        
        game_renderer = GameRenderer.get_instance()
        dice = Dice()
        dice.roll()
        game_renderer.draw_dice_animation(dice)
        if dice.last_roll <= 2:
            Death(player).apply()
        else:
            player.level_down(dice.last_roll)

class LoseItemsBadStuff(MonsterBadStuff):
    def __str__(self):
        if self.qty == 0:
            return "Você perde todos os itens."
        item_word = "item" if self.qty == 1 else "itens"
        return "Você perde {} {}.".format(self.qty, item_word)

    def __init__(self, qty=None):
        self.qty = qty

    def apply(self, player) -> None:
        player.remove_equipped_items(self.qty)

class LoseHandCardsBadStuff(MonsterBadStuff):
    def __str__(self):
        if self.qty == 0:
            return "Você perde todas as cartas da mão."
        card_word = "carta" if self.qty == 1 else "cartas"
        return "Você perde {} {}.".format(self.qty, card_word)

    def __init__(self, qty=None):
        self.qty = qty

    def apply(self, player) -> None:
        player.remove_hand_cards(self.qty)

class LoseLevelBadStuff(MonsterBadStuff):
    def __str__(self):
        level_word = "nível" if self.level_loss == 1 else "níveis"
        return "Você perde {} {}.".format(self.level_loss, level_word)

    def __init__(self, level_loss: int):
        self.level_loss = level_loss

    def apply(self, player) -> None:
        player.level_down(self.level_loss)

class LoseEquippedItemBadStuff(MonsterBadStuff):
    def __str__(self):
        return "Você perde o item equipado de tipo {}.".format(self.item_type)

    def __init__(self, item_type: str):
        self.item_type = item_type

    def apply(self, player) -> None:
        player.remove_equipped_item_type(self.item_type) 
    
class LoseAllClassItemsBadStuff(MonsterBadStuff):
    def __str__(self):
        return "Você perde todos os itens da sua classe."

    def apply(self, player) -> None:
        player.lose_all_class_cards()

# TODO: Continuar com os outros bad stuffs