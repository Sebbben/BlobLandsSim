import pygame, sys, random, math, cProfile, pstats

import pandas as pd

from Blobs.carnivore import Carnivore
from Blobs.herbivore import Herbivore
from Blobs.parasite import Parasite

from food import Food
from camera import Camera

from settings import *
from functions import *



class Game:

    def __init__(self):
        self.SPEED = 1
        self.SEE_TARGET_LINES = False
        self.lastBlobInfo = None
        self.paused = False

        self.dataIntervalTimer = 0
        self.data = {
            "numberOfBlobs":[],
            "numberOfHerbivores":[],
            "numberOfCarnivores":[],
            "numberOfParasites":[],
            "avrageSize":[],
            "avrageSizeHerbivore":[],
            "avrageSizeCarnivore":[],
            "avrageSizeParasite":[],
            "foodAmount":[],
        }

        self.camMovingRight = False
        self.camMovingLeft = False
        self.camMovingUp = False
        self.camMovingDown = False


        pygame.init()

        self.window = pygame.display.set_mode(WINDOW_RES, pygame.RESIZABLE)
        pygame.display.set_caption("BlobLandSim")

        self.cam = Camera(self.window)
        self.cam.center()

        self.fpsClock = pygame.time.Clock()

        self.blobs = []
        self.foods = []

        self.populateLists()

    def start(self):
        while True:
            
            self.window.fill((255, 255, 255))

            if len(self.blobs) == 0:
                self.quitGame()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitGame()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handleMouseDown(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handleMouseUp(event)
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyDown(event)
                elif event.type == pygame.KEYUP:
                    self.handleKeyUp(event)
                

            self.updateCam()

            if not self.paused: self.update() 
            else: self.showStats()
            self.draw()    
                

            pygame.display.flip()

            self.fpsClock.tick(FPS)

    def update(self):

        if self.dataIntervalTimer > DATA_COLLECTION_FRAME_INTERVAL:
            self.dataIntervalTimer = 0
            self.collectData()

        self.dataIntervalTimer += 1
        
        for i in range(NEW_FOOD_PER_FRAME):
            if random.randint(1, 2) == 1:
                f = Food(self.window)
                for i in range(len(self.foods)):
                    if self.foods[i].pos[0] > f.pos[0]:
                        self.foods.insert(i, f)
                        break        

        for food in self.foods:
            food.update()
        
        for blob in self.blobs:
            blob.update(self.blobs,self.foods,self.SPEED)

        if self.lastBlobInfo: 
            [posX,posY] = self.cam.getScreenPos(self.lastBlobInfo.pos)
            self.cam.nonSmoothMove([posX-self.window.get_width()//2, posY-self.window.get_height()//2])
        
        self.blobs = [blob for blob in self.blobs if not blob.dead]

        self.checkIfRottenFood()


        
    def draw(self):

        for food in self.foods:
            food.draw(self.cam)
        
        for blob in self.blobs:
            blob.draw(self.cam, self.SEE_TARGET_LINES)

        if pygame.font and self.lastBlobInfo:
            f = pygame.font.Font(None, 32)
            text = f.render(str(round(self.lastBlobInfo.size,2)) + str(round(self.lastBlobInfo.eatCooldown,2)) + "," + str(self.lastBlobInfo.dna),True, (0,0,0))
            textPos = text.get_rect(centerx=self.window.convert().get_width()/2, y=10)
            self.window.blit(text,textPos)

        self.cam.update()

    def collectData(self):
        numberOfBlobs = len(self.blobs)
        numberOfHerbivores = 0
        numberOfCarnivores = 0
        numberOfParasites = 0
        avrageSize = []
        avrageSizeHerbivore = []
        avrageSizeCarnivore = []
        avrageSizeParasite = []
        foodAmount = len(self.foods)

        for blob in self.blobs:
            avrageSize.append(blob.size)
            if blob.dna["type"] == "Herbivore":
                numberOfHerbivores += 1
                avrageSizeHerbivore.append(blob.size)
            elif blob.dna["type"] == "Carnivore":
                numberOfCarnivores += 1
                avrageSizeCarnivore.append(blob.size)
            elif blob.dna["type"] == "Parasite":
                numberOfParasites += 1
                avrageSizeParasite.append(blob.size)
        
        avrageSize = avrg(avrageSize)
        avrageSizeHerbivore = avrg(avrageSizeHerbivore)
        avrageSizeCarnivore = avrg(avrageSizeCarnivore)
        avrageSizeParasite = avrg(avrageSizeParasite)

        self.data["numberOfBlobs"].append(numberOfBlobs)
        self.data["numberOfHerbivores"].append(numberOfHerbivores)
        self.data["numberOfCarnivores"].append(numberOfCarnivores)
        self.data["numberOfParasites"].append(numberOfParasites)
        self.data["avrageSize"].append(avrageSize)
        self.data["avrageSizeHerbivore"].append(avrageSizeHerbivore)
        self.data["avrageSizeCarnivore"].append(avrageSizeCarnivore)
        self.data["avrageSizeParasite"].append(avrageSizeParasite)
        self.data["foodAmount"].append(foodAmount)

    def populateLists(self):
        for _ in range(FOOD_AMOUNT//2):
            self.foods.append(Food(self.window, age=random.randint(0,FPS*20)))

        self.foods.sort(key=lambda f:f.pos[0])

        for _ in range(START_NUMBER_OF_BLOBS): self.blobs.append(Herbivore(START_BLOB_SIZE,[random.randint(0,SIMULATION_SIZE[0]), random.randint(0, SIMULATION_SIZE[1])], self.window))

        for _ in range(3): self.blobs.append(Carnivore(START_BLOB_SIZE,[random.randint(0,SIMULATION_SIZE[0]), random.randint(0, SIMULATION_SIZE[1])], self.window))

               
    def checkIfRottenFood(self):
        self.foods = [food for food in self.foods if food.notRotten()]

    def getBlobInfo(self):
        
        self.lastBlobInfo = None
        mousePos = pygame.mouse.get_pos()

        for blob in self.blobs:
            if math.dist(self.cam.getScreenPos(blob.pos), mousePos) < blob.size * self.cam.zoomLvl:
                self.lastBlobInfo = blob
                self.cam.zoomTarget = 1
    def showStats(self):
        
        avrgVegiDna = {
            "maxSize": [],
            "minSize": [],
        }
        avrgMeatEaterDna = {
            "maxSize": [],
            "minSize": [],
        }
        for blob in self.blobs:
            if isinstance(blob, Carnivore):
                avrgMeatEaterDna["maxSize"].append(blob.dna["maxSize"])
                avrgMeatEaterDna["minSize"].append(blob.dna["minSize"])
            else:
                avrgVegiDna["maxSize"].append(blob.dna["maxSize"])
                avrgVegiDna["minSize"].append(blob.dna["minSize"])

        if len(avrgVegiDna["maxSize"]):
            for key in avrgVegiDna:
                avrgVegiDna[key] = sum(avrgVegiDna[key])//len(avrgVegiDna[key])
        if len(avrgMeatEaterDna["maxSize"]):
            for key in avrgMeatEaterDna:
                avrgMeatEaterDna[key] = sum(avrgMeatEaterDna[key])//len(avrgMeatEaterDna[key])

        if pygame.font:
            f = pygame.font.Font(None, 32)
            text = f.render("Vegi:"+ str(avrgVegiDna) + " "*50 + "MeatEater: " + str(avrgMeatEaterDna),True, (0,0,0))
            textPos = text.get_rect(centerx=self.window.convert().get_width()/2, y=10)
            self.window.blit(text,textPos)
        else:
            print("No font :(")

    def p(self):
        profile = cProfile.Profile()
        profile.runcall(self.update)
        ps = pstats.Stats(profile)
        ps.print_stats()


        exit()

    def handleMouseUp(self,event):
        if event.button == 1:
            self.getBlobInfo()

    def handleMouseDown(self,event):
        if event.button == 4:
            self.cam.zoom(0.1)
        elif event.button == 5:
            self.cam.zoom(-0.1)

    def handleKeyDown(self,event):
        pass

    def handleKeyUp(self,event):
        
        if event.key == pygame.K_SPACE:
            self.paused = not self.paused
        elif event.key == pygame.K_ESCAPE:
            self.quitGame()
        elif event.key == pygame.K_BACKSPACE:
            self.p()
        elif event.key == pygame.K_f:
            self.blobs = [blob for blob in self.blobs if random.randint(0,2)]
        elif event.key == pygame.K_UP:
            self.SPEED += 0.1
        elif event.key == pygame.K_DOWN:
            self.SPEED -= 0.1
        elif event.key == pygame.K_LSHIFT:
            self.cam.zoom(0.1)
        elif event.key == pygame.K_LCTRL:
            self.cam.zoom(-0.1)
        elif event.key == pygame.K_t:
            self.SEE_TARGET_LINES = not self.SEE_TARGET_LINES
        elif event.key == pygame.K_RETURN:
            self.cam.center()
        elif event.key == pygame.K_o:
            self.blobs.append(Carnivore(START_BLOB_SIZE*2,[random.randint(0,SIMULATION_SIZE[0]), random.randint(0, SIMULATION_SIZE[1])], self.window, dna={"type":"Carnivore","seeChance":1}))
        elif event.key == pygame.K_i:
            self.blobs.append(Herbivore(START_BLOB_SIZE*2,[random.randint(0,SIMULATION_SIZE[0]), random.randint(0, SIMULATION_SIZE[1])], self.window, dna={"type":"Herbivore"}))
            

    def updateCam(self):
        keys = pygame.key.get_pressed()

        camMovingLeft = keys[pygame.K_a]
        camMovingRight = keys[pygame.K_d]
        camMovingUp = keys[pygame.K_w]
        camMovingDown = keys[pygame.K_s]

        
        camMoveX = (camMovingRight-camMovingLeft) * CAMERA_SPEED
        camMoveY = (camMovingDown-camMovingUp) * CAMERA_SPEED

        mouseMovement = pygame.mouse.get_rel() # needs to get called every frame to get accurate readings
        if pygame.mouse.get_pressed()[0]:
            self.cam.nonSmoothMove([-mouseMovement[0], -mouseMovement[1]])
            
        self.cam.moveTarget(camMoveX, camMoveY)

    def quitGame(self):

        pd.DataFrame(self.data).to_csv("blobData.csv")

        pygame.quit()
        sys.exit()

    

game = Game()
game.start()