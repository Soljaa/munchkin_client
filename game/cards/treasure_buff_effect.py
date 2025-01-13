from abc import ABC, abstractmethod


class TreasureBuffEffect(ABC):
    @abstractmethod
    def apply(self, target) -> None:
        pass

class EveryoneScapesBuff(TreasureBuffEffect):
    def __init__(self):
        pass

    def increase_global_turns(turn, game_state):
        print(f"Turno concluído. Próximo jogador: {game_state.current_player().name}")
        return turn + 1

    def apply(self, target) -> None:
        from game.game_state import GameState
        from ui.game_renderer import GameRenderer        
        from game.game_phases.charity_phase import CharityPhase
        game_state = GameState.get_instance()
        game_renderer = GameRenderer.get_instance()

        # é o que acontece quando foge no game_manager: elif action == "run_away"
        game_state.door_deck.discard(game_state.current_combat.monster)
        game_state.set_combat(None)
        charity_phase = CharityPhase(game_state, game_renderer)
        charity_phase.run()


class BonusToEitherSideBuff(TreasureBuffEffect):
    def __init__(self, bonus):
        self.bonus = bonus

    def apply(self, target) -> None:
        pass

class UpALevelBuff(TreasureBuffEffect):
    def apply(self, target) -> None:
        target.level_up()

class DrawExtraTreasureBuff(TreasureBuffEffect):
    def __init__(self, amount, treasure_deck):
        self.amount = amount
        self.treasure_deck = treasure_deck

    def apply(self, target):
        for _ in range(self.amount):
            target.draw_card(self.treasure_deck)

class StealALevelBuff(TreasureBuffEffect):
    def __init__(self, curr_player):
        self.curr_player = curr_player

    def apply(self, target):
        # TODO: Para ter esse Buff, precisará implementar a tela para o curr_player selecionar o target
        self.curr_player.level_up()
        target.level_down()
        