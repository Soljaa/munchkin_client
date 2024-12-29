class Death:
    def __init__(self, player):
        self.player = player

    def apply(self):
        self.player.level = 0

    def draw(self):
        """Função que desenha o aviso de morte do player"""
        pass