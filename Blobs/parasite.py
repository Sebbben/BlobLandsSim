import random
from Blobs.blob import Blob
from math import sqrt

from Blobs.carnivore import Carnivore

class Parasite(Blob):
    def __init__(self, size:float, pos:list, window, SIMULATION_SIZE:list, dna = {}):
        super().__init__(size, pos, window, SIMULATION_SIZE, dna)

        self.color = (255,255,0)
        self.host = None
        self.leachAmount = 10

    def split(self):
        from Blobs.carnivore import Carnivore
        from Blobs.herbivore import Herbivore
        newBlobs = []
        self.mutate()
        for _ in range(self.dna["splittNumber"]):
            newSize = self.size//self.dna["splittNumber"]
            newX = self.pos[0]+random.randint(0,self.size//self.dna["splittNumber"])
            newY = self.pos[1]+random.randint(0,self.size//self.dna["splittNumber"])

            if self.dna["type"] == "Herbivore":
                blob = Herbivore(newSize, [newX,newY], self.window, self.SIMULATION_SIZE, self.dna.copy())
            elif self.dna["type"] == "Carnivore":
                blob = Carnivore(newSize, [newX,newY], self.window, self.SIMULATION_SIZE, self.dna.copy())
            elif self.dna["type"] == "Parasite":
                blob = Parasite(newSize, [newX,newY], self.window, self.SIMULATION_SIZE, self.dna.copy())
            newBlobs.append(blob)
        return newBlobs

    def update(self, blobs, food, gamespeed):
        super().update(blobs, food, gamespeed)
        self.updateHost(blobs)

    def updateHost(self,blobs):
        if self.host and self.host.size > 10: return # skip if has host and host is large enough
        self.host = None
        for blob in blobs:
            if isinstance(blob, Carnivore):
                if blob.pos[0]<self.pos[0]-self.size*2 or blob.pos[0]>self.pos[0]+self.size*2: continue # skip if self is too far left or right of self 
                if self.distTo(blob.pos) < self.size and blob.size > 10:
                    self.host = blob
                    break



    def move(self):
        if self.host:
            self.pos = self.host.pos

    def eat(self):
        if self.host:
            self.host.size = sqrt(self.host.size**2-self.leachAmount).real
            self.size = sqrt(self.size**2+self.leachAmount).real