import random
from math import sqrt
import this
from Blobs.blob import Blob
from Blobs.herbivore import Herbivore


class Carnivore(Blob):
    def __init__(self, size:float, pos:list, window, SIMULATION_SIZE:list, dna = {}):
        super().__init__(size, pos, window, SIMULATION_SIZE, dna)

        self.energyConsumption = 1/450
        self.color = (200,50,50)
        self.eatCooldown = self.size * 3
        self.eatEfficiency = 1
        self.isSeeFrame = False

    def split(self):
        newBlobs = []
        self.mutate()
        for _ in range(self.dna["splittNumber"]):
            newSize = self.size//self.dna["splittNumber"]
            newX = self.pos[0]+random.randint(0,self.size//self.dna["splittNumber"])
            newY = self.pos[1]+random.randint(0,self.size//self.dna["splittNumber"])

            from Blobs.herbivore import Herbivore
            from Blobs.parasite import Parasite

            if self.dna["type"] == "Herbivore":
                blob = Herbivore(newSize, [newX,newY], self.window, self.SIMULATION_SIZE, self.dna.copy())
            elif self.dna["type"] == "Carnivore":
                blob = Carnivore(newSize, [newX,newY], self.window, self.SIMULATION_SIZE, self.dna.copy())
            elif self.dna["type"] == "Parasite":
                blob = Parasite(newSize, [newX,newY], self.window, self.SIMULATION_SIZE, self.dna.copy())

            newBlobs.append(blob)
        return newBlobs


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
            if self.distTo(b.pos) < self.size and self.size + self.size*2 > b.size > self.size*(0/4):
                if isinstance(b, Herbivore) and self.eatCooldown < 0:
                    self.eatCooldown = b.size*(FPS*0.5)
                    #self.eatCooldown = 0
                    #self.size = sqrt(self.size**2 + (b.size*self.eatEfficiency)**2)
                    print(sqrt(self.size**2 + b.size**2).real - self.size)
                    self.size = sqrt(self.size**2 + b.size**2).real

                    b.dead = True

        