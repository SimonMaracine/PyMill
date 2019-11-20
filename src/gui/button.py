import pygame


class Button:
    """Class representing a simple button object. Can be inherited to make more specialized buttons."""
    button_down = False

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255, 255, 255)
        self.locked = False

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def update(self, mouse: tuple):
        if not self.locked:
            if self.hovered(mouse):
                self.color = (16, 16, 16)
            else:
                self.color = (255, 255, 255)
        else:
            self.color = (60, 60, 60)

    def hovered(self, mouse: tuple) -> bool:
        x = mouse[0]
        y = mouse[1]
        if self.x + self.width > x > self.x:
            if self.y + self.height > y > self.y:
                return True
        return False

    def pressed(self, mouse: tuple, mouse_pressed: int) -> bool:
        if self.locked:
            return False
        if mouse_pressed == pygame.BUTTON_LEFT and self.button_down:
            if self.hovered(mouse):
                return True
        return False

    def offset(self, mode: int):
        """Offset the button's position.

        Args:
            mode (int): Specifies what offset should the method do.

        """
        if mode == 0:
            self.x -= self.width // 2
        return self

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False


class TextButton(Button):

    def __init__(self, x: int, y: int, text: str, font: pygame.font.Font, text_color: tuple):
        self.text = text
        self.font = font
        self.text_color = text_color
        text_size = font.size(self.text)
        self.text_width = text_size[0]
        self.text_height = text_size[1]
        super().__init__(x, y, self.text_width, self.text_height)

        self.render_background = False

    def render(self, surface: pygame.Surface):
        if self.render_background:
            super().render(surface)
        text = self.font.render(self.text, True, self.text_color)
        surface.blit(text, (self.x, self.y))

    def update(self, mouse: tuple):
        if not self.locked:
            if self.hovered(mouse):
                self.text_color = (0, 0, 255)
            else:
                self.text_color = (255, 0, 0)
        else:
            self.text_color = (60, 60, 60)


class ImageButton(Button):

    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.Surface):
        self.image = image
        self._scale_image(width,  height)
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        super().__init__(x, y, self.image_width, self.image_height)

    def render(self, surface: pygame.Surface):
        surface.blit((self.x, self.y), self.image)

    def update(self, mouse: tuple):
        pass

    def _scale_image(self, width: int, height: int):
        pygame.transform.scale(self.image, (width, height))
