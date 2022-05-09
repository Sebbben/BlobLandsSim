import pygame
import sys, random
from Blobs.carnivore import Carnivore
from Blobs.herbivore import Herbivore
from Blobs.parasite import Parasite
from food import Food
import cProfile, pstats
from camera import Camera

FPS = 120 # frames per second setting
WIN_W = 1920
WIN_H = 1080

SIMULATION_SIZE = [1500, 1500]
FOOD_DENCITY = 1/3456
FOOD_AMOUNT = int((SIMULATION_SIZE[0]*SIMULATION_SIZE[1])*FOOD_DENCITY)
START_NUMBER_OF_BLOBS = 5
START_BLOB_SIZE = 20
CAMERA_SPEED = 10
SPEED = 1

lastBlobInfo = None
paused = False

camMovingRight = False
camMovingLeft = False
camMovingUp = False
camMovingDown = False

cam = Camera()

pygame.init()



# window = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
window = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)

fpsClock = pygame.time.Clock()


blobs = []
foods = []

cameraPos = [window.get_width()/2, window.get_height()/2]


for _ in range(FOOD_AMOUNT//2):
    foods.append(Food(window,SIMULATION_SIZE, age=random.randint(0,FPS*20)))


for _ in range(START_NUMBER_OF_BLOBS):
    blob = Herbivore(START_BLOB_SIZE,[random.randint(0,SIMULATION_SIZE[0]), random.randint(0, SIMULATION_SIZE[1])], window, SIMULATION_SIZE)
    blobs.append(blob)

def checkIfEaten():
    global foods
    global blobs

    
    foods.sort(key=lambda f: f.pos[0])
    blobs.sort(key=lambda b: b.pos[0])


    for blob in blobs:
        if isinstance(blob, Herbivore):
            blob.eat(foods)
        elif isinstance(blob, Carnivore):
            blob.eat(blobs,FPS)
        elif isinstance(blob, Parasite):
            blob.eat()
            

                           
            
def checkIfRottenFood():
    global foods
    foods = [food for food in foods if food.notRotten()]

def getBlobInfo():
    global blobs
    global lastBlobInfo

    lastBlobInfo = None
    mouseX, mouseY = pygame.mouse.get_pos()
    mouseX += cam.pos[0]
    mouseY += cam.pos[1]
    mouseX *= cam.zoomLvl
    mouseY *= cam.zoomLvl

    for blob in blobs:
        if blob.distTo([mouseX,mouseY]) < blob.size*2:
            lastBlobInfo = blob
            cam.zoomTarget = 1

def update():
    global blobs
    global foods

    if len(foods) < FOOD_AMOUNT:
        foods.append(Food(window, SIMULATION_SIZE))
        
    for food in foods:
        food.update()
    
    for blob in blobs:
        blob.update(blobs,food,SPEED)

    if lastBlobInfo: 
        camX = lastBlobInfo.pos[0] - window.get_width()//2
        camY = lastBlobInfo.pos[1] - window.get_height()//2
        cam.setTarget([camX, camY])
    
    blobs = [blob for blob in blobs if not blob.dead]

    checkIfRottenFood()
    checkIfEaten()
    
    
def draw():
    global lastBlobInfo

    for food in foods:
        food.draw(cam)
    
    for blob in blobs:
        blob.draw(cam)

    if pygame.font and lastBlobInfo:
        f = pygame.font.Font(None, 32)
        text = f.render(str(lastBlobInfo.dna),True, (0,0,0))
        textPos = text.get_rect(centerx=window.convert().get_width()/2, y=10)
        window.blit(text,textPos)

    cam.update()

        

def showStats():
    global blobs
    avrgVegiDna = {
        "maxSize": [],
        "splittNumber": [],
    }
    avrgMeatEaterDna = {
        "maxSize": [],
        "splittNumber": [],
    }
    for blob in blobs:
        if blob.dna["type"] == "Carnivore":
            avrgMeatEaterDna["maxSize"].append(blob.dna["maxSize"])
            avrgMeatEaterDna["splittNumber"].append(blob.dna["splittNumber"])
        else:
            avrgVegiDna["maxSize"].append(blob.dna["maxSize"])
            avrgVegiDna["splittNumber"].append(blob.dna["splittNumber"])

    if len(avrgVegiDna["maxSize"]):
        for key in avrgVegiDna:
            avrgVegiDna[key] = sum(avrgVegiDna[key])//len(avrgVegiDna[key])
    if len(avrgMeatEaterDna["maxSize"]):
        for key in avrgMeatEaterDna:
            avrgMeatEaterDna[key] = sum(avrgMeatEaterDna[key])//len(avrgMeatEaterDna[key])

    if pygame.font:
        f = pygame.font.Font(None, 32)
        text = f.render("Vegi:"+ str(avrgVegiDna) + " "*50 + "MeatEater: " + str(avrgMeatEaterDna),True, (0,0,0))
        textPos = text.get_rect(centerx=window.convert().get_width()/2, y=10)
        window.blit(text,textPos)
    else:
        print("No font :(")





def p():
    profile = cProfile.Profile()
    profile.runcall(update)
    ps = pstats.Stats(profile)
    ps.print_stats()


    exit()


def handleMouseUp(event):
    if event.button == 1:
        getBlobInfo()

def handleMouseDown(event):
    if event.button == 4:
        cam.zoom(0.1)
    elif event.button == 5:
        cam.zoom(-0.1)

def handleKeyDown(event):
    pass


def handleKeyUp(event):
    if event.key == pygame.K_SPACE:
        paused = not paused
    elif event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
    elif event.key == pygame.K_BACKSPACE:
        p()
    elif event.key == pygame.K_f:
        blobs = [blob for blob in blobs if random.randint(0,2)]
    elif event.key == pygame.K_UP:
        SPEED += 0.1
        print(SPEED)
    elif event.key == pygame.K_DOWN:
        SPEED -= 0.1
        print(SPEED)
    elif event.key == pygame.K_RIGHT:
        cam.zoom(0.1)
    elif event.key == pygame.K_LEFT:
        cam.zoom(-0.1)


while True:
    window.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            handleMouseDown(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            handleMouseUp(event)
        elif event.type == pygame.KEYDOWN:
            handleKeyDown(event)
        elif event.type == pygame.KEYUP:
            handleKeyUp(event)

            
    keys = pygame.key.get_pressed()

    camMovingLeft = keys[pygame.K_a]
    camMovingRight = keys[pygame.K_d]
    camMovingUp = keys[pygame.K_w]
    camMovingDown = keys[pygame.K_s]


    camMoveX = (camMovingRight-camMovingLeft) * CAMERA_SPEED
    camMoveY = (camMovingDown-camMovingUp) * CAMERA_SPEED

    mouseMovement = pygame.mouse.get_rel() # needs to get called every frame to get accurate readings
    if pygame.mouse.get_pressed()[0]:
        cam.moveTarget(-mouseMovement[0], -mouseMovement[1])
        
    cam.moveTarget(camMoveX, camMoveY)
        
    if not paused: update() 
    else: showStats()
    draw()    
        

    pygame.display.flip()

    fpsClock.tick(FPS)
