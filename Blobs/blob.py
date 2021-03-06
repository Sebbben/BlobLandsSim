from abc import abstractclassmethod
from math import ceil, dist
import pygame
import random
from Blobs.blobInfant import BlobInfant
from pygame import Vector2

from settings import *
from functions import clamp


class Blob:
    def __init__(self, size:float, pos:Vector2, window, infant) -> None:
        
        self.pos = pos
        self.size = size

        self.MAX_MUTATION = 1/4

        self.eatEfficiency = 1
        self.dead = False
        self.MIN_BLOB_SIZE = MIN_BLOB_SIZE
        self.speed = 4
        self.color = (0,0,0)
        self.target = None
        self.energyConsumption = 1/100

        #self.eatCooldown = self.size*3
        self.eatCooldown = 0
        
        self.SIMULATION_SIZE = SIMULATION_SIZE
        
        self.splitSizeFactor = 1
        
        self.seeTime = 0
        
        self.type = "blob"

        self.dnaClamp = infant.dnaClamp

    
        self.dna = infant.dna

        self.dna["rgb"] = self.dna["rgb"].copy()


        self.mutate()
        self.window = window


    def split(self):
        newBlobs = []
        splittNumber = int(self.size // self.dna["minSize"])
        for _ in range(splittNumber):
            newSize = self.size//splittNumber
            newX = self.pos.x+random.randint(0,self.size//splittNumber)
            newY = self.pos.y+random.randint(0,self.size//splittNumber)

            blob = BlobFactory().createBlob(newSize, Vector2(newX,newY), self.window, BlobInfant(self.dna, self.dnaClamp))

            newBlobs.append(blob)
        return newBlobs

    def clampMutations(self):
        for key in self.dna:
            if not key in self.dnaClamp: continue

            self.dna[key] = clamp(self.dna[key], self.dnaClamp[key][0], self.dnaClamp[key][1])
                
            
        

    def mutate(self):
        dnaKeys = list(self.dna.keys())
        for _ in range(random.choices([0,1,2,3,4,5,6],[15,15,30,20,10,5,5])[0]):
            geneToMod = dnaKeys[random.randint(0,len(dnaKeys)-1)]
            if geneToMod == "maxSize":
                self.dna[geneToMod] += random.randint(-int(self.dna[geneToMod]*self.MAX_MUTATION),int(self.dna[geneToMod]*self.MAX_MUTATION))
            elif geneToMod == "minSize":
                self.dna[geneToMod] = min(int(self.dna["maxSize"]//2), self.dna[geneToMod] + random.randint(-int(self.dna[geneToMod]*self.MAX_MUTATION),int(self.dna[geneToMod]*self.MAX_MUTATION)))
            elif geneToMod == "type":
                self.dna[geneToMod] = random.choice(["Herbivore", "Carnivore", "Parasite"]) if random.randint(1,3) == 1 else self.dna["type"]
            elif geneToMod == "seeRange":
                self.dna[geneToMod] += random.randint(-50, 50)
            elif geneToMod == "seeChance":
                self.dna[geneToMod] += random.uniform(-0.2, 0.2)
            elif geneToMod == "seeTime":
                self.dna[geneToMod] += random.randint(-50, 50)
            elif geneToMod == "rgb":
                for __ in range(random.randint(1, 4)):
                    self.dna[geneToMod][random.randint(0, 2)] += random.randint(-10, 10)
            elif geneToMod == "speed":
                self.dna[geneToMod] += random.randint(-15, 15)
            elif geneToMod == "isCannibal":
                self.dna[geneToMod] = not self.dna[geneToMod]
                
        self.clampMutations()

    def draw(self, camera, drawLines):
        
        r = clamp(self.color[0] + self.dna["rgb"][0], 0, 255)
        g = clamp(self.color[1] + self.dna["rgb"][1], 0, 255)
        b = clamp(self.color[2] + self.dna["rgb"][2], 0, 255)

        color = [r, g, b]
        if drawLines:
            pygame.draw.line(self.window, color, camera.getScreenPos(self.pos), camera.getScreenPos(self.target), width=max(round(2*camera.zoomLvl), 1))

        pygame.draw.circle(self.window, color, camera.getScreenPos(self.pos), max(round(self.size*camera.zoomLvl), 1))
        
    def distTo(self, otherPos):
        return dist(otherPos,self.pos)

    def readyToSplitt(self) -> bool:
        return self.size > self.dna["maxSize"] * self.splitSizeFactor


    def makeMoveVector(self, x, y, steps):
        xOff = x-self.pos[0]
        yOff = y-self.pos[1]

        distToTarget = self.distTo([x,y])

        factor = (steps/distToTarget)

        self.xMove = round(xOff*factor,2)
        self.yMove = round(yOff*factor,2)
        
    

    def checkIfTooSmall(self):
        if self.size < self.MIN_BLOB_SIZE:
            self.dead = True

    def checkIfTooLarge(self,blobs:list,stats):
        if self.readyToSplitt():
            self.dead = True
            blobs += self.split()
            for key in stats:
                stats[key].append(self.dna[key])

    def newRandomTarget(self):
        return [random.randint(0,self.SIMULATION_SIZE[0]-ceil(self.size)), random.randint(0, self.SIMULATION_SIZE[1]-ceil(self.size))]
        
    def setTarget(self, pos):
        self.target = pos
        self.makeMoveVector(pos[0], pos[1], self.speed*self.gamespeed*(self.dna["speed"]/50))

    def updateTarget(self):
        if self.target == None or self.distTo(self.target) < self.size - self.speed * self.gamespeed:
            self.setTarget(self.newRandomTarget()) 
           

        

    def move(self):
        self.pos[0] += self.xMove * self.gamespeed
        self.pos[1] += self.yMove * self.gamespeed

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


    def findNearbyTarget(self, nearbyFoods):
    
        if len(nearbyFoods) == 0: return

        self.size -= self.energyConsumption*(self.dna["speed"]/50)
        


        closest = None
        if not nearbyFoods[0] is self:        
            closest = nearbyFoods[0]
        else:
            closest = nearbyFoods[1]

        closestdist = self.distTo(closest.pos)

        for f in nearbyFoods:
            dist = self.distTo(f.pos)
            if 0 < dist < closestdist and self.canEat(f):     
                closestdist = dist
                closest = f

        if closestdist < self.dna["seeRange"]:
            return closest

            


from Blobs.blobFactory import BlobFactory # DO NOT MOVE, NEEDS TO MAKE IMPORT AS LAST THING THAT HAPPENES IN FILE