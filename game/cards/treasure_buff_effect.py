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
        game_state.set_combat(None)
        game_state.door_deck.discard(game_state.current_combat.monster)
        charity_phase = CharityPhase(game_state, game_renderer)
        charity_phase.run()
        game_state.next_player()
        curr_turn = self.increase_global_turns(curr_turn, game_state)
        print("Turno:", curr_turn)

class BonusToEitherSide(TreasureBuffEffect):
    def __init__(self, bonus):
        self.bonus = bonus

    def apply(self, target) -> None:
        pass