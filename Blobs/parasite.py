import math
from Blobs.blob import Blob
from math import sqrt

from settings import *

class Parasite(Blob):
    def __init__(self, size:float, pos:list, window, dna = {}):
        super().__init__(size, pos, window, dna)


        self.dnaClamp["maxSize"] = [5,30]

        if not dna:
            self.dna["maxSize"] = 20

        self.color = PARASITE_COLOR
        self.host = None
        self.leachAmount = 5
        self.energyConsumption = PARASITE_ENERGY_CONSUMPTION
        self.speed = 1/2

        self.hostlessTimerResetTime = 2400
        self.hostlessTimer = self.hostlessTimerResetTime

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
