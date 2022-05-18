import math
import random
from Blobs.blob import Blob
from math import sqrt


class Parasite(Blob):
    def __init__(self, size:float, pos:list, window, SIMULATION_SIZE:list, dna = {}):
        super().__init__(size, pos, window, SIMULATION_SIZE, dna)


        self.dnaClamp["maxSize"] = [5,30]

        if not dna:
            self.dna["maxSize"] = 20

        self.color = (255,255,0)
        self.host = None
        self.leachAmount = 5
        self.energyConsumption = 1/1000
        self.speed = 1/2

        self.hostlessTimerResetTime = 1200
        self.hostlessTimer = self.hostlessTimerResetTime


    def split(self):
        from Blobs.carnivore import Carnivore
        from Blobs.herbivore import Herbivore
        newBlobs = []
        self.mutate()
        splittNumber = int(self.size // self.dna["minSize"])
        for _ in range(splittNumber):
            newSize = self.size//splittNumber
            newX = self.pos[0]+random.randint(0,self.size//splittNumber)
            newY = self.pos[1]+random.randint(0,self.size//splittNumber)

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
        self.updateHostTimer()

    def updateHostTimer(self):
        self.hostlessTimer -= 1
        if self.hostlessTimer < 0:
            self.dead = True
            return

        if self.host:
            self.hostlessTimer = self.hostlessTimerResetTime



    def updateHost(self,blobs):

        if self.host: # skip trying to get new host if it allready has one
            if self.host.size > self.size: # condition when parasite should leave host
                self.host = None
                self.getNewTarget()
                self.makeMoveVector(self.target[0], self.target[1], self.speed * self.gamespeed)
            else: # if has host and everythin is a ok
                return

        for blob in blobs:
            if isinstance(blob, Parasite): continue # skip if the other blob is parasite aka, don't be a canibal
            if blob.pos[0]<self.pos[0]-self.size*2 or blob.pos[0]>self.pos[0]+self.size*2: continue # skip if self is too far left or right of self 
            if self.distTo(blob.pos) < blob.size and self.eatCooldown < 0 and blob.size > self.size:
                self.host = blob
                break
                



    def move(self):
        if self.host:
            self.pos = self.host.pos.copy()
            self.target = self.host.pos.copy()
        else:
            self.updateTarget()

            self.pos[0] += self.xMove * self.gamespeed
            self.pos[1] += self.yMove * self.gamespeed

    def eat(self):
        if self.host: # and isinstance(self.host, Carnivore):

            if self.host.size**2-(self.leachAmount/math.pi) < 0:
                self.host = None
                self.getNewTarget()
                self.makeMoveVector(self.target[0], self.target[1], self.speed * self.gamespeed)
                return

            self.host.size = sqrt(self.host.size**2-(self.leachAmount/math.pi)).real
            self.size = sqrt(self.size**2+(self.leachAmount/math.pi)).real
