import pygame


class Button:
    def __init__(self, x, y, width, height, image_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_hovered = False
        self.is_active = True
        self.image = None
        if image_path:
            # Carrega e redimensiona a imagem para o tamanho do botão
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and self.is_active:
                return True
        return False

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
