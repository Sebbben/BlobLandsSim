from abc import abstractclassmethod
from math import ceil
import math
import pygame
import random

from settings import *


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

        self.eatCooldown = self.size*3
        
        self.SIMULATION_SIZE = SIMULATION_SIZE

        self.dnaClamp = {
            "maxSize":[30, 160],
            "minSize": [15,50],
            "seeRange": [0, 10],
            "seeChance": [1, 50]
        }

        if dna:
            self.dna = dna
        else:
            self.dna = {
                "maxSize": 80,
                "minSize": 20,
                "type":"Herbivore",
                "seeRange":3,
                "seeChance":5
            }


        
        self.window = window


    def split(self):
        newBlobs = []
        self.mutate()
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
            if len(self.dnaClamp) == 2:
                self.dna[key] = max(self.dnaClamp[key][0], min(self.dnaClamp[key][1], self.dna[key]))
            else:
                self.dna[key] = max(self.dnaClamp[key][0], self.dna[key])
                
            
        

    def mutate(self):
        dnaKeys = list(self.dna.keys())
        for _ in random.choices([0,1,2],[45,50,5]):
            geneToMod = dnaKeys[random.randint(0,len(dnaKeys)-1)]
            if geneToMod == "maxSize":
                self.dna[geneToMod] += random.randint(-int(self.dna[geneToMod]*self.MAX_MUTATION),int(self.dna[geneToMod]*self.MAX_MUTATION))
            elif geneToMod == "minSize":
                self.dna[geneToMod] = min(int(self.dna["maxSize"]//2), self.dna[geneToMod] + random.randint(-int(self.dna[geneToMod]*self.MAX_MUTATION),int(self.dna[geneToMod]*self.MAX_MUTATION)))
            elif geneToMod == "type":
                self.dna[geneToMod] = random.choice(["Herbivore", "Carnivore", "Parasite"])
            elif geneToMod == "seeRange":
                self.dna[geneToMod] += random.uniform(-0.5, 0.5)
            elif geneToMod == "seeChance":
                self.dna[geneToMod] += random.randint(-1, 1)


        self.clampMutations()

    def draw(self, camera, drawLines):
        if drawLines:
            pygame.draw.line(self.window, self.color, camera.getScreenPos(self.pos), camera.getScreenPos(self.target), width=round(2*camera.zoomLvl))

        pygame.draw.circle(self.window, self.color, camera.getScreenPos(self.pos), round(self.size*camera.zoomLvl))
        
    def distTo(self, otherPos):
        return math.dist(otherPos,self.pos)

    def readyToSplitt(self) -> bool:
        return self.size > self.dna["maxSize"]


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

    def newTarget(self):
        return [random.randint(0,self.SIMULATION_SIZE[0]-ceil(self.size)), random.randint(0, self.SIMULATION_SIZE[1]-ceil(self.size))]
        

    def updateTarget(self):
        if self.target == None or self.distTo(self.target) < self.size - self.speed * self.gamespeed:
            self.getNewTarget()
            self.makeMoveVector(self.target[0], self.target[1], self.speed * self.gamespeed)
            
    def getNewTarget(self):
        self.target = self.newTarget()
        

    @abstractclassmethod
    def move():
        pass

    def update(self, blobs, foods, gamespeed, FPS):
        self.gamespeed = gamespeed
        self.size -= self.energyConsumption*self.gamespeed
        self.eatCooldown = max(-1, self.eatCooldown-1)
        self.FPS = FPS

        self.move()

        self.checkIfTooSmall()
        self.checkIfTooLarge(blobs)
        
    def see(self, nearbyFoods):
        min = self.distTo(nearbyFoods[0].pos)
        for f in nearbyFoods:
            dist = self.distTo(f.pos)
            #if self.distTo(f.pos) < self.dna["seeRange"]:
            if dist < min:      
                self.target = f.pos
                min = dist
        

from Blobs.blobFactory import BlobFactory # DO NOT MOVE, NEEDS TO MAKE IMPORT AS LAST THING THAT HAPPENES IN FILE