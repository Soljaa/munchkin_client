from ui.menu import Menu
from game.game_manager import main
import pygame
import sys


if __name__ == "__main__":
    menu = Menu(1280, 720)
    player_name = menu.run()
    main(player_name)
    pygame.quit()
    sys.exit()
