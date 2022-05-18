import random
from math import sqrt
from Blobs.blob import Blob

class Carnivore(Blob):
    def __init__(self, size:float, pos:list, window, SIMULATION_SIZE:list, dna = {}):
        from Blobs.herbivore import Herbivore
        super().__init__(size, pos, window, SIMULATION_SIZE, dna)

        self.energyConsumption = 1/450
        self.color = (200,50,50)
        self.eatCooldown = self.size * 3
        self.eatEfficiency = 1
        self.isSeeFrame = False


    def move(self):
        self.updateTarget()

        self.pos[0] += self.xMove * self.gamespeed
        self.pos[1] += self.yMove * self.gamespeed
    
    def getNewTarget(self):
        super().getNewTarget()
        self.isSeeFrame = (random.randint(1, self.dna["seeChance"]) == 1) 

    def eat(self, blobs, FPS):
        for b in blobs: 
            if b.dna["type"] == "Carnivore": continue # dont be a canibal
            if b.pos[0]<self.pos[0]-self.size*2 or b.pos[0]>self.pos[0]+self.size*2: continue # skip if self is too far left or right of self 
            if self.distTo(b.pos) < self.size and self.size + self.size*2 > b.size:# > self.size*(0/4):
                if b.dna["type"] == "Herbivore" or b.dna["type"] == "Carnivore" and self.eatCooldown < 0 and not b is self:
                    self.eatCooldown = b.size*(FPS*0.5)
                    self.size = sqrt(self.size**2 + b.size**2).real

                    b.dead = True

        