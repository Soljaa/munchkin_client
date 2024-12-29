from ui.button import Button

class HoverButton(Button):
    def __init__(self, image_path, x, y, width=None, height=None, scale_factor=1.1, acao=None):
        super().__init__(image_path, x, y, width, height, acao)
        
        # Fator de escala para aumentar o tamanho no hover
        self.scale_factor = scale_factor

        

        # Guarda o tamanho original do botão
        self.original_x = x
        self.original_y = y
        self.original_width = self.sprite.width 
        self.original_height = self.sprite.height
        self.hovered_width = self.original_width * self.scale_factor  
        self.hovered_height = self.original_height * self.scale_factor 

    def update(self):  # Atualiza o estado do botão (verifica hover)
        if self.mouse.is_over_object(self.sprite):
            self.sprite.set_scale(self.hovered_width / self.original_width, 
                                  self.hovered_height / self.original_height)  # Muda o tamanho
            self.sprite.x = self.original_x - self.sprite.width / 2  # Recentraliza o botão
            self.sprite.y = self.original_y - self.sprite.height / 2  # Recentraliza o botão

        else:
            self.sprite.set_scale(1, 1)  # Volta ao tamanho original
            self.sprite.x = self.original_x - self.sprite.width / 2  # Recentraliza o botão
            self.sprite.y = self.original_y - self.sprite.height / 2  # Recentraliza o botão

    def draw(self):  # Desenhar os Botões
        self.update()  # Atualiza o estado antes de desenhar
        self.sprite.draw()
