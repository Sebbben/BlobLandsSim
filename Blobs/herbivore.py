from pygame import Vector2
from Blobs.blob import Blob
from math import sqrt

from settings import *

class Herbivore(Blob):
    def __init__(self, size:float, pos:Vector2, window, infant):
        super().__init__(size, pos, window, infant)

        self.color = HERBIVORE_COLOR
        self.energyConsumption = HERBIVORE_ENERGY_CONSUMPTION
        

    def move(self):
        super().move() #hvorfor trengs ikke self som en parameter her?
        

    def canEat(self, blob):
        return True
        

    def eat(self, foods):

        close = foods.getRange([self.pos.x-self.size*2,self.pos.x+self.size*2])


        toRemove = []

        for food in close:
            if self.distTo(food.pos) < self.size+(food.size/2):
                self.size = sqrt(self.size**2 + food.size**2).real
                toRemove.append(food)

        for food in toRemove:
            foods.remove(food)

    def update(self, blobs, foods, gamespeed, stats):
        super().update(blobs,foods,gamespeed, stats)

        self.startSee()

        if self.seeTime > 0:
            target = self.findNearbyTarget(foods.getRange([self.pos.x-self.dna["seeRange"],self.pos.y+self.dna["seeRange"]]))
            if target:
                self.setTarget(target.pos)
            else:
                self.updateTarget()

        else:
            self.updateTarget()

        self.eat(foods)