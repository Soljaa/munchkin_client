class Death:
    def __init__(self, player):
        self.player = player

    def apply(self):
        self.player.level = 0
        for item in self.player.equipped_items:
            self.player.add_to_discard_pile(item)

    def draw(self):
        """Função que desenha o aviso de morte do player"""
        pass
