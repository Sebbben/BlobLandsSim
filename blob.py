from math import pi, sqrt
import pygame
import random

class Blob:
    def __init__(self, size:int, pos:list, window) -> None:
        self.targetRange = 100
        self.speed = 4
        self.color = (255,0,0)
        self.target = None

        self.pos = pos
        self.size = size
    
        self.window = window

    def draw(self):
        #pygame.draw.circle(self.window, self.color, self.pos, self.size)
        pygame.draw.circle(self.window, self.color, [int(self.pos[0]), int(self.pos[1])], self.size)


    def move(self,x,y):
        self.pos[0] += x
        self.pos[1] += y
        
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
        return [random.randint(0,self.window.get_width()-self.size), random.randint(0, self.window.get_height()-self.size)]
        
    def eat(self, food):
        self.size = int(sqrt(self.size**2 + food.size**2).real)
        print(self.size)

    def update(self):
        if self.target == None or self.distToPoint(self.target[0], self.target[1]) < self.speed:
            self.target = self.newTarget(self.targetRange)
        else:
            self.moveTowards(self.target[0], self.target[1], self.speed)
