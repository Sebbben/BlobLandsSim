from abc import abstractclassmethod
from math import ceil
import pygame
from pygame import Vector2
import random
from Blobs.blobInfant import BlobInfant

from settings import *
from functions import clamp


class Blob:
    def __init__(self, size:float, pos:Vector2, window, infant) -> None:
        
        self.pos = pos
        self.size = size

        self.eatEfficiency = 1
        self.dead = False
        self.speed = 4
        self.color = (0,0,0)
        self.target = None
        self.energyConsumption = 1/100

        #self.eatCooldown = self.size*3
        self.eatCooldown = 0
                
        self.splitSizeFactor = 1
        
        self.seeTime = 0
        

        self.dna = infant.dna
        self.dnaClamp = infant.dnaClamp

        self.dna["rgb"] = self.dna["rgb"].copy()

        self.window = window


    def split(self):
        newBlobs = []
        splittNumber = int(self.size // self.dna["minSize"])
        for _ in range(splittNumber):
            newSize = self.size//splittNumber
            newPos = self.pos + [random.randint(0,self.size//splittNumber),random.randint(0,self.size//splittNumber)]

            infant = BlobInfant(self.dna, self.dnaClamp)

            blob = BlobFactory().createBlob(newSize, newPos, self.window, infant)

            newBlobs.append(blob)
        return newBlobs

    def draw(self, camera, drawLines):
        
        r = clamp(self.color[0] + self.dna["rgb"][0], 0, 255)
        g = clamp(self.color[1] + self.dna["rgb"][1], 0, 255)
        b = clamp(self.color[2] + self.dna["rgb"][2], 0, 255)

        color = [r, g, b]
        if drawLines:
            pygame.draw.line(self.window, color, camera.getScreenPos(self.pos), camera.getScreenPos(self.target), width=max(round(2*camera.zoomLvl), 1))

        pygame.draw.circle(self.window, color, camera.getScreenPos(self.pos), max(round(self.size*camera.zoomLvl), 1))
        
    def distTo(self, otherPos:Vector2):
        return (self.pos-otherPos).length()

    def readyToSplitt(self) -> bool:
        return self.size > self.dna["maxSize"] * self.splitSizeFactor

    def makeMoveVector(self,target, steps):
        
        newVec = target - self.pos
        newVec.scale_to_length(steps)

        self.moveVector = newVec
        

    def checkIfTooSmall(self):
        if self.size < MIN_BLOB_SIZE:
            self.dead = True

    def checkIfTooLarge(self,blobs:list,stats):
        if self.readyToSplitt():
            self.dead = True
            blobs += self.split()
            for key in stats:
                stats[key].append(self.dna[key])

    def newRandomTarget(self):
        return Vector2(random.randint(0,SIMULATION_SIZE[0]-ceil(self.size)), random.randint(0, SIMULATION_SIZE[1]-ceil(self.size)))
        
    def setTarget(self, pos):
        self.target = pos
        self.makeMoveVector(pos, self.speed*self.gamespeed*(self.dna["speed"]/50))

    def updateTarget(self):
        if self.target == None or self.distTo(self.target) < self.size or ((self.target-self.pos).length() != 0 and self.moveVector.length() != 0 and (self.target-self.pos).normalize() != self.moveVector.normalize()):
            self.setTarget(self.newRandomTarget())   

    def move(self):
        self.pos += self.moveVector*self.gamespeed

    def update(self, blobs, foods, gamespeed, stats):
        self.gamespeed = gamespeed
        self.size -= self.energyConsumption*self.gamespeed*(self.dna["speed"]/50)
        self.eatCooldown = max(-1, self.eatCooldown-1)
        self.seeTime = max(-1, self.seeTime-1)

        self.updateTarget()
        self.move()

        self.checkIfTooSmall()
        self.checkIfTooLarge(blobs, stats)
        
    def startSee(self):
        if random.randint(1, 10000) < self.dna["seeChance"]*100 and self.eatCooldown <= 0:
            self.seeTime = self.dna["seeTime"]
   
    @abstractclassmethod
    def canEat(blob):
        pass
    
    def nearEnoughBlob(self, blob):
        return self.distTo(blob.pos) < self.size+(blob.size/2)


    def findNearbyTarget(self, targets):
        if len(targets) <= 1: return # skip if this blob is only one

        self.size -= self.energyConsumption*(self.dna["speed"]/50) # use more energy if you see
        
        closest = None

        if not targets[0] is self: 
            closest = targets[0]
        else:
            closest = targets[1]

        closestdist = self.distTo(closest.pos)

        for f in targets:
            dist = self.distTo(f.pos)
            if 0 <= dist < closestdist and self.canEat(f):
                closestdist = dist
                closest = f

        if closestdist < self.dna["seeRange"]:
            return closest

            
    def getClose(self, xSorted, rng):

        upper = len(xSorted)
        lower = 0

        mid = lambda: (upper + lower) // 2
        xFind = []        

        while upper > lower:
            x = mid()
            if xSorted[x] != self and self.pos.x-rng < xSorted[x].pos.x < self.pos.x+rng:
                for i in range(x, upper):
                    if xSorted[i].pos.x < self.pos.x+rng:
                        xFind.append(xSorted[i])
                    else:
                        break
                for i in range(x-1, lower, -1):
                    if self.pos.x-rng < xSorted[i].pos.x:
                        xFind.append(xSorted[i])
                    else:
                        break
                break
            elif xSorted[x].pos.x > self.pos.x+rng:
                upper = x - 1
            else:
                lower = x + 1

        return xFind
        
        

from Blobs.blobFactory import BlobFactory # DO NOT MOVE, NEEDS TO MAKE IMPORT AS LAST THING THAT HAPPENES IN FILE