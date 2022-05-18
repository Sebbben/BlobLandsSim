import math
import random
from Blobs.blob import Blob
from math import sqrt

from Blobs.carnivore import Carnivore

class Parasite(Blob):
    def __init__(self, size:float, pos:list, window, SIMULATION_SIZE:list, dna = {}):
        super().__init__(size, pos, window, SIMULATION_SIZE, dna)

        self.color = (255,255,0)
        self.host = None
        self.leachAmount = 100
        self.energyConsumption = 1/1000
        self.speed = 1/2


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

    def update(self, blobs, food, gamespeed, FPS):
        super().update(blobs, food, gamespeed, FPS)
        self.updateHost(blobs)

    def updateHost(self,blobs):
        if self.host and (self.host.size > self.size): 
            return # skip trying to get new host if it allready has one that is large enough
        self.host = None
        for blob in blobs:
            if isinstance(blob, Parasite): continue # skip if the other blob is parasite
            if blob.pos[0]<self.pos[0]-self.size*2 or blob.pos[0]>self.pos[0]+self.size*2: continue # skip if self is too far left or right of self 
            if self.distTo(blob.pos) < blob.size and self.eatCooldown < 0 and blob.size > self.size:
                self.eatCooldown = blob.size*(self.FPS*0.5)
                self.host = blob
                if isinstance(blob, Carnivore):
                    break



    def move(self):
        if self.host != None:
            self.pos = self.host.pos
            self.target = self.host.pos
        else:
            self.updateTarget()

            self.pos[0] += self.xMove * self.gamespeed
            self.pos[1] += self.yMove * self.gamespeed

    def eat(self):
        if self.host: # and isinstance(self.host, Carnivore):
            self.host.size = sqrt(self.host.size**2-(self.leachAmount/math.pi)).real
            # self.size = sqrt(self.size**2+(self.leachAmount/math.pi)).real
            self.size += 1