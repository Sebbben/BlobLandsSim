import pygame
from random import randint as ri

class Food:
    def __init__(self, window, SIMULATION_SIZE, age = 0) -> None:
        self.size = ri(5,10)
        self.color = (0,ri(180,255),0)
        self.maxAge = (30)*20  #  (FPS) * seconds
        self.age = age

        self.SIMULATION_SIZE = SIMULATION_SIZE
        
        self.pos = [ri(0,self.SIMULATION_SIZE[0]), ri(0, self.SIMULATION_SIZE[1])]
        self.window = window


    def update(self):
        self.age += 1

    def draw(self, camera):
        cameraX, cameraY = camera.pos
        pygame.draw.circle(self.window, self.color, [self.pos[0]-cameraX, self.pos[1]-cameraY], self.size)
    
    def notRotten(self):
        return self.age < self.maxAge