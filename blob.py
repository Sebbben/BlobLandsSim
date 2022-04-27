from math import ceil, pi, sqrt
from unittest.mock import seal
import pygame
import random

class Blob:
    def __init__(self, size:float, pos:list, window) -> None:
        self.targetRange = 100
        self.speed = 4
        self.color = (255,0,0)
        self.target = None

        self.pos = pos
        self.size = size
        
      
    
        self.window = window

    def draw(self):
        #pygame.draw.circle(self.window, self.color, self.pos, self.size)
        pygame.draw.circle(self.window, self.color, [int(self.pos[0]), int(self.pos[1])], round(self.size))


    def move(self,x,y):
        self.pos[0] += x
        self.pos[1] += y
        
        self.size -= 1/30
        
       
        
    def distToPoint(self, x,y):
        return round(sqrt(abs(x-self.pos[0])**2 + abs(y-self.pos[1])**2).real,2)


    def moveTowards(self, x, y, steps):
        
        xOff = x-self.pos[0]
        yOff = y-self.pos[1]

        distToTarget = self.distToPoint(x,y)

        factor = steps/distToTarget

        xMove = round(xOff*factor,2)
        yMove = round(yOff*factor,2)
        
        self.move(xMove,yMove)

    def newTarget(self, r):
        return [random.randint(0,self.window.get_width()-ceil(self.size)), random.randint(0, self.window.get_height()-ceil(self.size))]
        
    def eat(self, food):
        self.size = sqrt(self.size**2 + food.size**2).real
        print(self.size)

    def update(self):
        if self.target == None or self.distToPoint(self.target[0], self.target[1]) < self.speed:
            self.target = self.newTarget(self.targetRange)
        else:
            self.moveTowards(self.target[0], self.target[1], self.speed)
            
            
       
