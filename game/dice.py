import random

from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.animation import *


class Dice:
    def __init__(self):
        # Infos
        self.img_dir = "assets/game/dice/rolling_dice.png"    # Caminho da imagem do dado
        self.sides = 6        # Número de lados do dado
        self.last_roll = None     # Resultado do último lançamento

        # Sprites
        self.sprite_rolling_dice = Sprite(self.img_dir, 8) # Sprite (animação) do dado rolando
        self.sprite_rolling_dice.set_total_duration(500)
        self.sprite_value_dice = Sprite(f"assets/game/dice/dice_1.png")  # Sprite do dado estático com seu valor default

    def roll(self):
        """Lança o dado e retorna um valor aleatório entre 1 e o número de lados."""
        self.last_roll = random.randint(1, self.sides)  # Gera um valor aleatório
        self.sprite_value_dice = Sprite(f"assets/game/dice/dice_{self.last_roll}.png")
        return self.last_roll

    def draw_rolling_dice(self, x=0, y=0):
        self.sprite_rolling_dice.x = x
        self.sprite_rolling_dice.y = y
        """Faz a animação do rolamento de dado"""
        
        self.sprite_rolling_dice.update()
        self.sprite_rolling_dice.draw()
        
        pygame.display.update()

    def draw_value_dice(self, x=0, y=0):
        """Desenha o dado estático com seu valor pós rolamento"""
        self.sprite_value_dice.x = x
        self.sprite_value_dice.y = y
        self.sprite_value_dice.draw()
        
        pygame.display.update()


# EXEMPLO
if __name__ == "__main__":
    window = Window(400, 400)
    window.set_title("Exibição de Dado")

    dice = Dice()  

    has_rolled = False

    while True:
        window.set_background_color((255, 255, 255))  # Cor de fundo branco

        if not has_rolled:
            dice.roll()  # Rola o dado para obter um valor

            roll_time_seconds = 4  # Tempo total de animação do dado rolando em segundos
            elapsed_time = 0  # Variável para controlar o tempo de animação
            clock = pygame.time.Clock()
            while elapsed_time < roll_time_seconds:
                # Calcula o tempo entre quadros
                delta_time = clock.tick(60) / 1000.0  # 60 FPS
                elapsed_time += delta_time  # Atualiza o tempo decorrido
                dice.draw_rolling_dice()  # Animação do rolamento do dado
                window.set_background_color((255, 255, 255))
                
            has_rolled = True

        dice.draw_value_dice()  # Desenha o valor final do dado

        window.update()  # Atualiza a tela
