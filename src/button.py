import pygame


class Button:
    button_down = False

    def __init__(self, x: float, y: float, text: str, font, text_color: tuple):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.text_color = text_color
        text_size = font.size(self.text)
        self.text_width = text_size[0]
        self.text_height = text_size[1]

    def render(self, surface):
        text = self.font.render(self.text, True, self.text_color)
        surface.blit(text, (self.x, self.y))

    def update(self, mouse: tuple):
        x = mouse[0]
        y = mouse[1]
        if self.hovered(mouse):
            self.text_color = (0, 0, 255)
        else:
            self.text_color = (255, 0, 0)

    def hovered(self, mouse: tuple) -> bool:
        x = mouse[0]
        y = mouse[1]
        if self.x + self.text_width > x > self.x:
            if self.y + self.text_height > y > self.y:
                return True
        return False

    def pressed(self, mouse: tuple, mouse_pressed: tuple) -> bool:
        if mouse_pressed[0] and self.button_down:
            if self.hovered(mouse):
                return True
        return False

    def offset(self, mode: int):
        if mode == 0:
            self.x -= self.text_width // 2
        return self
