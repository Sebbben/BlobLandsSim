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
        super().move()

    def getNewTarget(self):
        super().getNewTarget()
        self.isSeeFrame = (random.randint(1, 100) < 100*self.dna["seeChance"]) 

    def eat(self, foods:list):

        close = self.getClose(foods)

        newFoods = foods.copy()        

        for food in close:
            if self.distTo(food.pos) < self.size+(food.size/2):
                self.size = sqrt(self.size**2 + food.size**2).real
                newFoods.remove(food)

        foods.clear()
        foods.extend(newFoods)
            

        """
        if self.isSeeFrame: 
            self.see(foods)
            self.size -= self.energyConsumption*(self.dna["speed"]/50)*5
            self.isSeeFrame = False
        """            
        
            
        self.makeMoveVector(self.target[0], self.target[1], self.speed * self.gamespeed)
