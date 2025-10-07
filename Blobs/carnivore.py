from math import sqrt
from Blobs.blob import Blob
from settings import *

class Carnivore(Blob):
    def __init__(self, size:float, pos:list, window, infant):
        super().__init__(size, pos, window, infant)

        self.energyConsumption = CARNIVORE_ENERGY_CONSUMPTION
        self.color = CARNIVORE_COLOR
        #self.eatCooldown = self.size * 3
        self.eatCooldown = 5*FPS
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
        
    def canEat(self, blob):
        return (
            (
                blob.dna["type"] == "Herbivore" or 
                (
                    self.dna["isCannibal"] and 
                    blob.dna["type"] == "Carnivore" and 
                    blob.size < self.size
                )
            ) and 
            blob.size < self.size * 3
        ) and self.eatCooldown <= 0

    def eat(self, blobs):
        for b in blobs: 
            if not self.canEat(b): continue 
            if not b.dead and self.distTo(b.pos) < self.size + (b.size*(3/4)):
                #self.eatCooldown = b.size*(FPS*0.5)
                self.eatCooldown = 0
                self.size = sqrt(self.size**2 + b.size**2).real
                b.dead = True
                   
    def update(self, blobs, foods, gamespeed, stats):
        super().update(blobs,foods,gamespeed, stats)
        if self.dead: return
        
        self.startSee()

        if self.seeTime > 0:
            target = None
            target = self.findNearbyTarget(blobs)
            if target != None:
                self.setTarget(target.pos)
            else:
                self.updateTarget()

        else:
            self.updateTarget()

        self.eat(blobs)
                    

            

        