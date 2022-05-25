from abc import abstractclassmethod
from math import ceil, dist
import pygame
import random

from settings import *
from functions import clamp


class Blob:
    def __init__(self, size:float, pos:list, window, dna = {}) -> None:
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

        self.dnaClamp = {
            "maxSize":[30, 160],
            "minSize": [15,50],
            "seeRange": [0, 200],
            "seeChance": [0, 1],
            "seeTime": [0, 10*FPS],
            "speed": [0, 100]
        }

    
        self.dna = {
            "maxSize": 80,
            "minSize": 20,
            "type":"Herbivore",
            "seeRange":100,
            "seeChance":1/(30*FPS),
            "seeTime": 5*FPS,
            "rgb":[0, 0, 0],
            "speed":50
        } | dna

        self.dna["rgb"] = self.dna["rgb"].copy()

        self.mutate()

        self.window = window


    def split(self):
        newBlobs = []
        splittNumber = int(self.size // self.dna["minSize"])
        for _ in range(splittNumber):
            newSize = self.size//splittNumber
            newX = self.pos[0]+random.randint(0,self.size//splittNumber)
            newY = self.pos[1]+random.randint(0,self.size//splittNumber)

            blob = BlobFactory().createBlob(newSize, [newX,newY], self.window, self.dna)

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
                self.dna[geneToMod] = random.choice(["Herbivore", "Carnivore", "Parasite"]) if random.randint(1,5) == 1 else self.dna["type"]
            elif geneToMod == "seeRange":
                self.dna[geneToMod] += random.uniform(-0.5, 0.5)
            elif geneToMod == "seeChance":
                self.dna[geneToMod] += random.uniform(-0.2, 0.2)
            elif geneToMod == "seeTime":
                self.dna[geneToMod] += random.randint(-5, 5)
            elif geneToMod == "rgb":
                for __ in range(random.randint(1, 4)):
                    self.dna[geneToMod][random.randint(0, 2)] += random.randint(-10, 10)
            elif geneToMod == "speed":
                self.dna[geneToMod] += random.randint(-10, 10)
                
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

    def checkIfTooLarge(self,blobs:list):
        if self.readyToSplitt():
            self.dead = True
            blobs += self.split()

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

    def update(self, blobs, foods, gamespeed):
        self.gamespeed = gamespeed
        self.size -= self.energyConsumption*self.gamespeed*(self.dna["speed"]/50)
        self.eatCooldown = max(-1, self.eatCooldown-1)

        self.updateTarget()
        self.move()

        self.checkIfTooSmall()
        self.checkIfTooLarge(blobs)
        

    def startSee(self):
        if random.randint(1, 100) < self.dna["seeChance"]*100:
            self.seeTime = self.dna["seeTime"]


    def findNearbyTarget(self, nearbyFoods):
    
        if not nearbyFoods: return

        self.size -= self.energyConsumption*(self.dna["speed"]/50)
        self.seeTime = max(-1, self.seeTime-1)


        closest = None
        if not nearbyFoods[0] is self:        
            closest = nearbyFoods[0]
        else:
            closest = nearbyFoods[1]

        closestdist = self.distTo(closest.pos)

        for f in nearbyFoods:
            dist = self.distTo(f.pos)
            if 0 < dist < closestdist and not f is self:    
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
            if self.pos[0]-rng < xSorted[x].pos[0] < self.pos[0]+rng and xSorted[x] != self:
                for i in range(x, upper):
                    if xSorted[i].pos[0] < self.pos[0]+rng:
                        xFind.append(xSorted[i])
                    else:
                        break
                for i in range(x-1, lower, -1):
                    if self.pos[0]-rng < xSorted[i].pos[0]:
                        xFind.append(xSorted[i])
                    else:
                        break
                break
            elif xSorted[x].pos[0] > self.pos[0]+rng:
                upper = x - 1
            else:
                lower = x + 1

        return xFind
        
        

from Blobs.blobFactory import BlobFactory # DO NOT MOVE, NEEDS TO MAKE IMPORT AS LAST THING THAT HAPPENES IN FILE