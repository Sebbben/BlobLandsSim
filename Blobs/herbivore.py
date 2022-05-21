import random
from Blobs.blob import Blob
from math import sqrt

from settings import *

class Herbivore(Blob):
    def __init__(self, size:float, pos:list, window, dna = {}):
        super().__init__(size, pos, window, dna)
        self.isSeeFrame = False
        self.color = HERBIVORE_COLOR
        self.energyConsumption = HERBIVORE_ENERGY_CONSUMPTION

    def move(self):
        self.updateTarget()

        self.pos[0] += self.xMove * self.gamespeed
        self.pos[1] += self.yMove * self.gamespeed

    def getNewTarget(self):
        super().getNewTarget()
        self.isSeeFrame = (random.randint(1, 100) < 100*self.dna["seeChance"]) 

    def eat(self, foods:list):
        newFoods = []
        for food in foods:
            if food.pos[0]<self.pos[0]-self.size*2 or food.pos[0]>self.pos[0]+self.size*2: # skip if food is too far left or right of self
                newFoods.append(food)
                continue 
            #if self.distTo(food.pos) < self.size-(food.size):
            if self.distTo(food.pos) < self.size+(food.size/2):
                self.size = sqrt(self.size**2 + food.size**2).real
            else:
                newFoods.append(food)
        foods.clear()
        foods.extend(newFoods)

        if self.isSeeFrame: 
            self.see(foods)
            self.size -= self.energyConsumption*(self.dna["speed"]/50)*5
            self.isSeeFrame = False
            
        self.makeMoveVector(self.target[0], self.target[1], self.speed * self.gamespeed)
