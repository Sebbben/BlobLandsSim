from math import sqrt
import pygame
import random

class Blob:
    def __init__(self, size, pos, window) -> None:
        self.targetRange = 100
        self.speed = 4
        self.color = (255,0,0)
        self.target = None

        self.size = size
        self.pos = pos
        self.rect = pygame.Rect((self.pos[0],self.pos[1]), (self.size,self.size))
        
        self.window = window

    def draw(self):
        pygame.draw.ellipse(self.window, self.color, self.rect, self.size)

    def move(self,x,y):
        self.rect = pygame.Rect.move(self.rect, x, y)
        self.pos[0] = self.rect.x
        self.pos[1] = self.rect.y
        
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
        #må sjekke at blobben kan dra til target 
        # return [self.pos[0] + random.randint(-r, r), self.pos[1] + random.randint(-r, r)]
        return [random.randint(0,self.window.get_width()-self.size), random.randint(0, self.window.get_height()-self.size)]
        # return [0,0]
        

    def update(self):
        if self.target == None or self.distToPoint(self.target[0], self.target[1]) < self.speed:
            self.target = self.newTarget(self.targetRange)
            print(self.target)
        else:
            self.moveTowards(self.target[0], self.target[1], self.speed)
