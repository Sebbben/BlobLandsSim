from math import ceil, sqrt
import pygame
import random

class Blob:
    def __init__(self, size:float, pos:list, window, dna = {}) -> None:
        self.MAX_MUTATION = 1/2

        self.targetRange = 100
        self.speed = 4
        self.color = (255,0,0)
        self.target = None
        self.energyConsumption = 1/100

        self.dnaClamp = {
            "maxSize":[30, 100],
            "splittNumber": [2,8]
        }

        if dna:
            self.dna = dna
        else:
            self.dna = {
                "maxSize": 40,
                "splittNumber": 2
            }

        self.pos = pos
        self.size = size
        
        self.window = window

        self.mutate()

    def clampMutations(self):
        for key in self.dna:
            if len(self.dnaClamp) == 2:
                self.dna[key] = max(self.dnaClamp[key][0], min(self.dnaClamp[key][1], self.dna[key]))
            else:
                self.dna[key] = max(self.dnaClamp[key][0], self.dna[key])
        

    def mutate(self):
        dnaKeys = list(self.dna.keys())
        for _ in random.choices([0,1,2],[45,50,5]):
            geneToMod = dnaKeys[random.randint(0,len(dnaKeys)-1)]
            # print("Pre-mutation,:",geneToMod,self.dna[geneToMod])
            self.dna[geneToMod] += random.randint(-int(self.dna[geneToMod]*self.MAX_MUTATION),int(self.dna[geneToMod]*self.MAX_MUTATION))
            # print("Post-mutation:",self.dna[geneToMod])
            # print()
        self.clampMutations()

    def draw(self):
        pygame.draw.circle(self.window, self.color, [int(self.pos[0]), int(self.pos[1])], round(self.size))


    def move(self,x,y):
        self.pos[0] += x
        self.pos[1] += y
        
        
       
        
    def distToPoint(self, x,y):
        return round(sqrt(abs(x-self.pos[0])**2 + abs(y-self.pos[1])**2).real,2)

    def readyToSplitt(self) -> bool:
        return self.size > self.dna["maxSize"]

    def split(self):
        newBlobs = []
        for _ in range(self.dna["splittNumber"]):
            newBlobs.append(Blob(self.size//self.dna["splittNumber"], [self.pos[0]+random.randint(0,self.size//self.dna["splittNumber"]),self.pos[1]+random.randint(0,self.size//self.dna["splittNumber"])], self.window, self.dna))
        return newBlobs

    def moveTowards(self, x, y, steps):
        
        xOff = x-self.pos[0]
        yOff = y-self.pos[1]

        distToTarget = self.distToPoint(x,y)

        factor = steps/distToTarget

        xMove = round(xOff*factor,2)
        yMove = round(yOff*factor,2)
        
        self.move(xMove,yMove)

    def newTarget(self, r):
        return [random.randint(0,self.window.get_width()-ceil(self.size)), random.randint(0, self.window.get_height()-ceil(self.size))]
        
    def eat(self, food):
        self.size = sqrt(self.size**2 + food.size**2).real

    def update(self):

        self.size -= self.energyConsumption

        if self.target == None or self.distToPoint(self.target[0], self.target[1]) < self.speed:
            self.target = self.newTarget(self.targetRange)
        else:
            self.moveTowards(self.target[0], self.target[1], self.speed)
            
            
       
