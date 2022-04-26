import pygame

class Food:
    def __init__(self, pos, window) -> None:
        self.size = 5
        self.color = (0,255,0)

        self.pos = pos
        self.window = window

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)

    def draw(self):
        pygame.draw.ellipse(self.window, self.color, self.rect)
        #pygame.draw.ellipse(self.window, self.color, self.rect, self.size)