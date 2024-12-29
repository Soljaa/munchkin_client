class Death:
    def __init__(self, player):
        self.player = player

    def apply(self):
        self.player.level = 1
