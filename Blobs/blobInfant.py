from settings import *
from functions import *
import random


class BlobInfant:
    def __init__(self, dna = {}, dnaClamp={}):

        self.dnaClamp = {
            "maxSize":[30, 160],
            "minSize": [15,50],
            "seeRange": [0, 1000],
            "seeChance": [0, 1],
            "seeTime": [0, 10*FPS],
            "speed": [0, 100],
        } | dnaClamp

        self.dna = {
            "maxSize": 80,
            "minSize": 20,
            "type":"Herbivore",
            "seeRange":300,
            "seeChance":1/(30*FPS),
            "seeTime": 2.5*FPS,
            "rgb":[0, 0, 0],
            "speed":50,
            "isCannibal":False
        } | dna

        self.mutate()

            
    def mutate(self):
        dnaKeys = list(self.dna.keys())
        for _ in range(random.choices([0,1,2,3,4,5,6],[15,15,30,20,10,5,5])[0]):
            geneToMod = dnaKeys[random.randint(0,len(dnaKeys)-1)]
            if geneToMod == "maxSize":
                self.dna[geneToMod] += random.randint(-int(self.dna[geneToMod]*MAX_MUTATION),int(self.dna[geneToMod]*MAX_MUTATION))
            elif geneToMod == "minSize":
                self.dna[geneToMod] = min(int(self.dna["maxSize"]//2), self.dna[geneToMod] + random.randint(-int(self.dna[geneToMod]*MAX_MUTATION),int(self.dna[geneToMod]*MAX_MUTATION)))
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

    def clampMutations(self):
        for key in self.dna:
            if not key in self.dnaClamp: continue

            self.dna[key] = clamp(self.dna[key], self.dnaClamp[key][0], self.dnaClamp[key][1])