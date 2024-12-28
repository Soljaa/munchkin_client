from ui.menu import Menu
import pygame
import sys


if __name__ == "__main__":
    menu = Menu(1280, 720)
    menu.run()

    pygame.quit()
    sys.exit()
