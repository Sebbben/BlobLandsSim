from random import randint as ri 
from math import sqrt
from Blobs.blob import Blob
from settings import *

class Carnivore(Blob):
    def __init__(self, size:float, pos:list, window, dna = {}):
        super().__init__(size, pos, window, dna)

        self.energyConsumption = CARNIVORE_ENERGY_CONSUMPTION
        self.color = CARNIVORE_COLOR
        self.eatCooldown = self.size * 3
        self.eatEfficiency = 1
        self.isSeeFrame = False
        self.seeTime = 0


    def move(self):
        if (self.seeTime <= 0):
            self.updateTarget()


        self.pos[0] += self.xMove * self.gamespeed
        self.pos[1] += self.yMove * self.gamespeed
    
    def getNewTarget(self):
        super().getNewTarget()
        if (ri(1, 100) < 100*self.dna["seeChance"]):
            self.seeTime = 5
            

    def eat(self, blobs):
        for b in blobs: 
            if b.dna["type"] == "Carnivore" and b.size > self.size//2: continue # dont be a canibal (if the other guy is large)
            if self.distTo(b.pos) < self.size + (b.size/2) and self.size * 1.5 > b.size:
                if (b.dna["type"] == "Herbivore" or b.dna["type"] == "Carnivore") and self.eatCooldown < 0 and not b is self:
                    # print(b.dna["type"] == "Carnivore")
                    self.eatCooldown = b.size*(FPS*0.5)
                    self.size = sqrt(self.size**2 + b.size**2).real
                    b.dead = True
                    self.seeTime = 0
                    
        if self.seeTime >= 0: 
            self.seeTime -= 0.1*self.gamespeed
            self.see(blobs)
            self.size -= self.energyConsumption*self.gamespeed*(self.dna["speed"]/50)
            self.makeMoveVector(self.target[0], self.target[1], self.speed * self.gamespeed * (self.dna["speed"]/50))
                    

            

        