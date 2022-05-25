from Blobs.blob import Blob
from math import sqrt, pi

from settings import *

class Parasite(Blob):
    def __init__(self, size:float, pos:list, window, dna = {}):

        if not dna:
            self.dna["maxSize"] = 20
            super().__init__(size, pos, window, {"maxSize":20})
        else:
            super().__init__(size, pos, window, dna)



        self.dnaClamp["maxSize"] = [5,30]


        self.color = PARASITE_COLOR
        self.host = None
        self.leachAmount = 5
        self.energyConsumption = PARASITE_ENERGY_CONSUMPTION
        self.speed = 1/2

        self.hostlessTimerResetTime = 2400
        self.hostlessTimer = self.hostlessTimerResetTime
        
        self.splitSizeFactor = 0.5

    def update(self, blobs, food, gamespeed):
        super().update(blobs, food, gamespeed)
        self.updateHost(blobs)
        self.updateHostTimer()

        self.eat()

    def updateHostTimer(self):
        self.size -= PARASITE_HOSTLESS_ENERGY_CONSUMPTION_MILTUPLIER * (self.hostlessTimer/self.hostlessTimerResetTime) * self.energyConsumption
        self.hostlessTimer -= 1
        if self.hostlessTimer < 0:
            self.dead = True
            return

        if self.host:
            self.hostlessTimer = self.hostlessTimerResetTime



    def updateHost(self,blobs):

        if self.host: # skip trying to get new host if it allready has one
            if self.host.size < self.size: # condition when parasite should leave host
                self.host = None
                self.setTarget(self.newRandomTarget())
            else: # if has host and everythin is a ok
                return


        for blob in blobs:
            if blob.dna["type"] == "Parasite": continue # skip if the other blob is parasite aka, don't be a canibal
            if blob.pos[0]<self.pos[0]-self.size*2 or blob.pos[0]>self.pos[0]+self.size*2: continue # skip if self is too far left or right of self 
            if self.distTo(blob.pos) < blob.size and self.eatCooldown < 0 and blob.size > self.size:
                self.host = blob
                break
                



    def move(self):
        if self.host:
            self.pos = self.host.pos.copy()
            self.target = self.host.pos.copy()
        else:
            super().move()

    def eat(self):
        if self.host: # and isinstance(self.host, Carnivore):

            if self.host.size**2-(self.leachAmount/pi) < 0:
                self.host = None
                self.setTarget(self.newRandomTarget())
                return

            self.host.size = sqrt(self.host.size**2-(self.leachAmount/pi)).real
            self.size = sqrt(self.size**2+(self.leachAmount/pi)).real
