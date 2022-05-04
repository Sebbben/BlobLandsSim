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
        self.color = (255,0,0)
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
                #"meatEater":bool(random.randint(0,2))
                "meatEater":False
            }


        
        self.window = window

        self.mutate()

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
            self.dna[geneToMod] += random.randint(-int(self.dna[geneToMod]*self.MAX_MUTATION),int(self.dna[geneToMod]*self.MAX_MUTATION))

        if (random.randint(0, 60) == 2):
            self.dna["meatEater"] = not self.dna["meatEater"]
            
        if self.dna["meatEater"]:
            self.energyConsumption = 1/450
            self.color = (0,0,255)
            self.eatCooldown = self.size * 50
            self.eatEfficiency = 1/2

        self.clampMutations()

    def draw(self, cameraPos):
        cameraX, cameraY = cameraPos
        pygame.draw.circle(self.window, self.color, [int(self.pos[0]) - cameraX, int(self.pos[1]) - cameraY], round(self.size))


    def move(self):
        self.pos[0] += self.xMove
        self.pos[1] += self.yMove
             
        
    def distTo(self, otherPos):
        return math.dist(otherPos,self.pos)
        # return round(sqrt(abs(x-self.pos[0])**2 + abs(y-self.pos[+1])**2).real,2)

    def readyToSplitt(self) -> bool:
        return self.size > self.dna["maxSize"]

    def split(self):
        newBlobs = []
        for _ in range(self.dna["splittNumber"]):
            newBlobs.append(Blob(self.size//self.dna["splittNumber"], [self.pos[0]+random.randint(0,self.size//self.dna["splittNumber"]),self.pos[1]+random.randint(0,self.size//self.dna["splittNumber"])].copy(), self.window, self.SIMULATION_SIZE, self.dna.copy()))
        return newBlobs

    def makeMoveVector(self, x, y, steps):
        xOff = x-self.pos[0]
        yOff = y-self.pos[1]

        distToTarget = self.distTo([x,y])

        factor = steps/distToTarget

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
        
    def eat(self, food, FPS):
        if self.dna["meatEater"] and food is Blob:
            if self.eatCooldown < 0:
                self.eatCooldown = food.size*(FPS*0.5)
                # self.eatCooldown = 0
                self.size = sqrt(self.size**2 + (food.size*self.eatEfficiency)**2).real
        else:
            self.size = sqrt(self.size**2 + food.size**2).real

    def updateTarget(self):
        if self.target == None or self.distTo(self.target) < self.speed:
            self.target = self.newTarget(self.targetRange)
            self.makeMoveVector(self.target[0], self.target[1], self.speed)

    def update(self, blobs, food):
        self.size -= self.energyConsumption
        self.eatCooldown = max(-1, self.eatCooldown-1)

        self.updateTarget()
        self.move()

        self.checkIfTooSmall()
        self.checkIfTooLarge(blobs)
            
            
       
