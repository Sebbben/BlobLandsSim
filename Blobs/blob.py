from abc import abstractclassmethod
from math import ceil, sqrt
import math
import pygame
import random



class Blob:
    def __init__(self, size:float, pos:list, window, SIMULATION_SIZE:list, dna = {}) -> None:
        self.pos = pos
        self.size = size

        self.MAX_MUTATION = 1/4

        self.eatEfficiency = 1
        self.dead = False
        self.MIN_BLOB_SIZE = 5
        self.targetRange = 100
        self.speed = 4
        self.color = (100,70,19)
        self.target = None
        self.energyConsumption = 1/100

        self.eatCooldown = self.size*3
        
        self.SIMULATION_SIZE = SIMULATION_SIZE

        self.dnaClamp = {
            "maxSize":[30, 100],
            "splittNumber": [2,8]
        }

        if dna:
            self.dna = dna
        else:
            self.dna = {
                "maxSize": 40,
                "splittNumber": 2,
                "type":"Herbivore",
                "seeRange":3,
                "seeChance":3
            }


        
        self.window = window

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
            elif geneToMod == "splittNumber":
                self.dna[geneToMod] += random.randrange(-1,2)
            elif geneToMod == "type":
                self.dna[geneToMod] = random.choice(["Herbivore", "Carnivore", "Parasite"])


        self.clampMutations()

    def draw(self, camera):
        cameraX, cameraY = camera.pos
        pygame.draw.circle(self.window, self.color, [int(self.pos[0]*camera.zoomLvl) - cameraX, int(self.pos[1]*camera.zoomLvl) - cameraY], round(self.size*camera.zoomLvl))
        pygame.draw.line(self.window, (255, 0, 0), [int(self.pos[0]*camera.zoomLvl) - cameraX, int(self.pos[1]*camera.zoomLvl) - cameraY], [int(self.target[0]*camera.zoomLvl) - cameraX, int(self.target[1]*camera.zoomLvl) - cameraY], width=round(2*camera.zoomLvl))
        
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

    def checkIfTooLarge(self,blobs):
        if self.readyToSplitt():
            self.dead = True
            blobs += self.split()

    def newTarget(self, r):
        return [random.randint(0,self.SIMULATION_SIZE[0]-ceil(self.size)), random.randint(0, self.SIMULATION_SIZE[1]-ceil(self.size))]
        return [0, 0]
        

    def updateTarget(self):
        if self.target == None or self.distTo(self.target) < self.speed * self.gamespeed:
            self.getNewTarget()
            self.makeMoveVector(self.target[0], self.target[1], self.speed * self.gamespeed)
            
    def getNewTarget(self):
        self.target = self.newTarget(self.targetRange)
        

    @abstractclassmethod
    def move():
        pass

    def update(self, blobs, food, gamespeed):
        self.gamespeed = gamespeed
        self.size -= self.energyConsumption*self.gamespeed
        self.eatCooldown = max(-1, self.eatCooldown-1)

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
            
            
            
       
