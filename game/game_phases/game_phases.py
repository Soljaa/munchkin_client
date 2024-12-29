from abc import ABC, abstractmethod


class GamePhases(ABC):
    def __init__(self, game_state):
        self.game_state = game_state
        
    @abstractmethod
    def run(self):
        pass
