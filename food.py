import pygame
from random import randint as ri

from settings import *

class Food:
    def __init__(self, window, age = 0) -> None:
                
        self.size = ri(5,10)
        self.color = FOOD_COLOR()
        self.maxAge = (30)*20  #  (FPS) * seconds
        self.age = age

        self.SIMULATION_SIZE = SIMULATION_SIZE
        
        self.pos = pygame.math.Vector2(ri(0,self.SIMULATION_SIZE[0]), ri(0, self.SIMULATION_SIZE[1]))
        self.window = window


    def update(self):
        #self.age += 1
        pass

    def draw(self, camera):
        pygame.draw.circle(self.window, self.color, camera.getScreenPos(self.pos), max(self.size*camera.zoomLvl, 1))
    
    def rotten(self):
        return self.age > self.maxAge