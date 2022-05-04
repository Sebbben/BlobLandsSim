import pygame
import sys, random
from blob import Blob
from food import Food
import cProfile, pstats


FPS = 120 # frames per second setting
WIN_W = 1920
WIN_H = 1080

FOOD_PERC = 1/3456
FOOD_AMOUNT = int((WIN_W*WIN_H)*FOOD_PERC)
START_NUMBER_OF_BLOBS = 5
START_BLOB_SIZE = 20

lastBlobInfo = None
paused = False

pygame.init()

# window = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
window = pygame.display.set_mode((1920, 1080), pygame.SCALED)

fpsClock = pygame.time.Clock()


blobs = []
foods = []

#ctypes.windll.shcore.SetProcessDpiAwareness(1)

for _ in range(FOOD_AMOUNT//2):
    foods.append(Food([random.randint(0,window.get_width()), random.randint(0, window.get_height())], window, age=random.randint(0,FPS*20)))


for _ in range(START_NUMBER_OF_BLOBS):
    blobs.append(Blob(START_BLOB_SIZE,[random.randint(0,window.get_width()), random.randint(0, window.get_height())], window))
    # blobs.append(Blob(START_BLOB_SIZE,[window.get_width()//2, window.get_height()//2], window))

def checkIfEaten():
    global foods
    global blobs

    
    foods.sort(key=lambda f: f.pos[0])
    blobs.sort(key=lambda b: b.pos[0])


    for blob in blobs:
        if not blob.dna["meatEater"]:
            newFoods = []
            for food in foods:
                if food.pos[0]<blob.pos[0]-blob.size*2 or food.pos[0]>blob.pos[0]+blob.size*2: # skip if food is too far left or right of blob
                    newFoods.append(food)
                    continue 
                if blob.distTo(food.pos) < blob.size-(food.size):
                    blob.eat(food,FPS)
                else:
                    newFoods.append(food)
            foods = newFoods
        else:
            for b in blobs:
                if b.dna["meatEater"]: continue # dont be a canibal
                if b.pos[0]<blob.pos[0]-blob.size*2 or b.pos[0]>blob.pos[0]+blob.size*2: continue # skip if blob is too far left or right of blob 
                if blob.distTo(b.pos) < blob.size-b.size-10:
                    blob.eat(b,FPS)
                    b.dead = True

                           
            
def checkIfRottenFood():
    global foods
    foods = [food for food in foods if food.notRotten()]

def getBlobInfo():
    global blobs
    global lastBlobInfo

    lastBlobInfo = None
    mousePos = pygame.mouse.get_pos()
    for blob in blobs:
        if blob.distTo(mousePos) < blob.size*2:
            lastBlobInfo = blob.dna

def update():
    global blobs
    global foods

    if len(foods) < FOOD_AMOUNT:
        foods.append(Food([random.randint(0,window.get_width()), random.randint(0, window.get_height())], window))
        
    for food in foods:
        food.update()
    
    for blob in blobs:
        blob.update(blobs,food)
    
    blobs = [blob for blob in blobs if not blob.dead]

    checkIfRottenFood()
    checkIfEaten()
    

    
def draw():
    global lastBlobInfo

    for food in foods:
        food.draw()
    
    for blob in blobs:
        blob.draw()

    if pygame.font and lastBlobInfo:
        text = f.render(str(lastBlobInfo),True, (0,0,0))
        textPos = text.get_rect(centerx=window.convert().get_width()/2, y=10)
        window.blit(text,textPos)

        

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
        if blob.dna["meatEater"]:
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


# p()

while True:
    window.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            getBlobInfo()
        elif event.type == pygame.KEYDOWN:

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
                FPS += 10
            elif event.key == pygame.K_DOWN:
                FPS -= 10
            

    if not paused: update() 
    else: showStats()
    draw()    
        

    pygame.display.flip()

    fpsClock.tick(FPS)
