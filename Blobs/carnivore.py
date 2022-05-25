from math import sqrt
from Blobs.blob import Blob
from settings import *

class Carnivore(Blob):
    def __init__(self, size:float, pos:list, window, dna = {}):
        super().__init__(size, pos, window, dna)

        self.energyConsumption = CARNIVORE_ENERGY_CONSUMPTION
        self.color = CARNIVORE_COLOR
        #self.eatCooldown = self.size * 3
        self.eatCooldown = 0
        self.eatEfficiency = 1
        self.isSeeFrame = False


    def move(self):
        super().move()
    
    def getNewTarget(self):
        super().getNewTarget()
        """
        if (ri(1, 100) < 100*self.dna["seeChance"]):
            self.seeTime = 5
        """
            

    def eat(self, blobs):
        if self.eatCooldown > 0: return
        for b in blobs: 
            if b.dna["type"] == "Carnivore" and b.size > self.size//2: continue # dont be a canibal (if the other guy is large)
            if self.distTo(b.pos) < self.size + (b.size*(3/4)) and self.size * 3 > b.size:
                if (b.dna["type"] == "Herbivore" or b.dna["type"] == "Carnivore") and not b is self:
                    # print(b.dna["type"] == "Carnivore")
                    #self.eatCooldown = b.size*(FPS*0.5)
                    self.eatCooldown = 0
                    self.size = sqrt(self.size**2 + b.size**2).real
                    b.dead = True
                    #self.seeTime = 0
   
    def update(self, blobs, foods, gamespeed):
        super().update(blobs,foods,gamespeed)

        self.eat(blobs)
                    

            

        