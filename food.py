import pygame
from random import randint as ri

class Food:
    def __init__(self, pos, window, age = 0) -> None:
        self.size = ri(5,10)
        self.color = (0,ri(180,255),0)
        self.maxAge = (30)*20  #  (FPS) * seconds
        self.age = age

        self.pos = pos
        self.window = window


    def update(self):
        self.age += 1

    def draw(self):
        pygame.draw.circle(self.window, self.color, self.pos, self.size)