import pygame

from ui.button import Button

class HoverButton(Button):
    def __init__(self, image_path, x, y, width, height, scale_factor=1.1):
        # Chama o construtor da classe Button
        super().__init__(x, y, width, height, image_path)
        
        # Fator de escala para aumentar o tamanho no hover
        self.scale_factor = scale_factor
        self.original_width = width
        self.original_height = height

    def draw(self, screen):
        # Se o botão está sendo hoverado, aumenta o tamanho
        if self.is_hovered:
            # Aumenta o tamanho do botão em 20%
            new_width = int(self.original_width * self.scale_factor)
            new_height = int(self.original_height * self.scale_factor)
            scaled_rect = pygame.Rect(self.rect.x - (new_width - self.original_width) // 2,
                                      self.rect.y - (new_height - self.original_height) // 2,
                                      new_width, new_height)
            # Desenha a imagem redimensionada
            screen.blit(pygame.transform.scale(self.image, (new_width, new_height)), scaled_rect)
        else:
            # Caso contrário, desenha o botão com o tamanho original
            super().draw(screen)
