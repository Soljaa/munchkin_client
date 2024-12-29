from enum import Enum, auto


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

    def get_monster_strength(self):
        # Monster gets stronger with more players
        num_players = 1 + len(self.helpers)
        return (self.monster.level * (1 if num_players == 1 else 1.5)) + self.monster_modifiers

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

        if player_strength > monster_strength:
            return True, {
                'treasure': self.monster.treasure,
                'level_gain': 1,
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

