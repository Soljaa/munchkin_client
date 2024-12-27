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
        self.sprite_value_dice = Sprite(f"assets/game/dice/dice_{self.last_roll}.png") # Sprite do dado estático com seu valor

    def roll(self):
        """Lança o dado e retorna um valor aleatório entre 1 e o número de lados."""
        self.last_roll = random.randint(1, self.sides)  # Gera um valor aleatório
        self.sprite_value_dice = Sprite(f"assets/game/dice/dice_{self.last_roll}.png")
        return self.last_roll
    
    def draw_rolling_dice(self):
        """Faz a animação do rolamento de dado"""
        self.sprite_rolling_dice.update()
        self.sprite_rolling_dice.draw()

    def draw_value_dice(self):
        "Desenha o dado estático com seu valor pós rolamento"
        self.sprite_value_dice.draw()
         


###
###
###

# EXEMPLO
if __name__ == "__main__":
    ### Início da execução do jogo ###
    window = Window(400, 400)
    window.set_title("Exibição de Dado")

    dado = Dice()  # Caminho para a imagem do dado

    segundos_de_dado_rolando = 4  # Tempo total de animação do dado rolando em segundos
    segundos_rolados = 0  # Variável para controlar o tempo de animação
    foiRolado = False

    while True:
        window.set_background_color((255, 255, 255))  # Cor de fundo branco

        if not foiRolado:
            while segundos_rolados < segundos_de_dado_rolando:
                window.set_background_color((255, 255, 255))  # Cor de fundo branco
                segundos_rolados += window.delta_time()  # Adiciona o tempo de cada quadro
                dado.draw_rolling_dice()  # Desenha o dado rolando
                window.update()

            dado.roll()
            print(dado.last_roll)

            foiRolado = True

        dado.draw_value_dice()  # Desenha o valor final do dado

        window.update()  # Atualiza a tela