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

    def eat(self, foods:list):

        close = self.getClose(foods, self.size*2)

        newFoods = foods.copy()        

        for food in close:
            if self.distTo(food.pos) < self.size+(food.size/2):
                self.size = sqrt(self.size**2 + food.size**2).real
                newFoods.remove(food)

        foods.clear()
        foods.extend(newFoods)
            
    def update(self, blobs, foods, gamespeed):
        super().update(blobs,foods,gamespeed)

        self.startSee()

        if self.seeTime > 0:
            target = self.findNearbyTarget(self.getClose(foods, self.dna["seeRange"]))
            if target:
                self.setTarget(target.pos)
            else:
                self.updateTarget()

        else:
            self.updateTarget()

        self.eat(foods)