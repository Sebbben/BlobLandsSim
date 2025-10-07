import pygame
from random import randint
import numpy as np

from settings import *

class Food:
    def __init__(self, window, age = 0) -> None:
                
        self.size = randint(5,10)
        self.color = FOOD_COLOR()
        self.maxAge = (30)*20  #  (FPS) * seconds
        self.age = age

        self.SIMULATION_SIZE = SIMULATION_SIZE
        
        self.pos = np.array((randint(0,self.SIMULATION_SIZE[0]), randint(0, self.SIMULATION_SIZE[1])))
        self.window = window


    def update(self):
        #self.age += 1
        pass

    def draw(self, camera):
        if self.size * camera.zoomLvl > 1 and camera.isOnScreen(self.pos):
            pygame.draw.circle(self.window, self.color, camera.getScreenPos(self.pos), self.size*camera.zoomLvl)
            return 1
        return 0
    
    def rotten(self):
        return self.age > self.maxAge