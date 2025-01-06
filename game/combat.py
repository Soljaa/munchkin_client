from enum import Enum, auto

from game.card import RaceTypes


class CombatStates(Enum):
    WINNING = auto()
    LOSING = auto()


class Combat:
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster
        self.player_modifiers = 0
        self.monster_modifiers = 0
        self.can_run_away = True
        self.helpers = []  # Other players who help in combat

    def get_player_strength(self):
        base_strength = self.player.calculate_combat_strength()
        helper_strength = sum(helper.calculate_combat_strength() for helper in self.helpers)
        return base_strength + helper_strength + self.player_modifiers

    def apply_monster_effect(self):
        self.monster.apply_effect(self.player)

    def get_monster_strength(self):
        return self.monster.level + self.monster_modifiers

    def add_helper(self, player):
        if player not in self.helpers and player != self.player:
            self.helpers.append(player)
            return True
        return False

    def remove_helper(self, player):
        if player in self.helpers:
            self.helpers.remove(player)
            return True
        return False

    def add_player_modifier(self, value):
        self.player_modifiers += value
        return self.get_player_strength()

    def add_monster_modifier(self, value):
        self.monster_modifiers += value
        return self.get_monster_strength()

    def try_to_run(self, value):
        success = value >= 5  # Need 5 or 6 to run away
        return success

    def resolve_combat(self):
        player_strength = self.get_player_strength()
        monster_strength = self.get_monster_strength()
        self.apply_monster_effect()

        if player_strength > monster_strength:
            if self.monster.after_death_effect:
                self.monster.apply_after_death_effect(self.player) # Pode aumentar os tesouros, por exemplo

            return True, {
                'treasure': self.monster.treasure,
                'level_gain': 2 if (self.player.race == RaceTypes.ORC and self.monster.level > 10) or self.monster.reward_two_levels else 1,
                'message': f"Victory! Gained {self.monster.treasure} treasure(s)!"
            }
        return False, {
            'bad_stuff': self.monster.bad_stuff,
            'message': f"Defeat! {self.monster.bad_stuff}"
        }

    def get_combat_state(self):
        player_strength = self.get_player_strength()
        monster_strength = self.get_monster_strength()

        if player_strength > monster_strength:
            return CombatStates.WINNING

        return CombatStates.LOSING

