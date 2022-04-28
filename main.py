import pygame
import sys, random
from blob import Blob
from food import Food

FPS = 120 # frames per second setting
WIN_W = 1920
WIN_H = 1080

FOOD_PERC = 1/3456
FOOD_AMOUNT = int((WIN_W*WIN_H)*FOOD_PERC)
START_NUMBER_OF_BLOBS = 1
START_BLOB_SIZE = 20
MIN_BLOB_SIZE = 5

lastBlobInfo = None

pygame.init()

# window = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
window = pygame.display.set_mode((1920, 1080), pygame.SCALED)

fpsClock = pygame.time.Clock()


blobs = []
foods = []

for _ in range(FOOD_AMOUNT//2):
    foods.append(Food([random.randint(0,window.get_width()), random.randint(0, window.get_height())], window))


for _ in range(START_NUMBER_OF_BLOBS):
    # blobs.append(Blob(START_BLOB_SIZE,[random.randint(0,window.get_width()), random.randint(0, window.get_height())], window))
    blobs.append(Blob(START_BLOB_SIZE,[window.get_width()//2, window.get_height()//2], window))

def checkIfEaten():
    global foods
    global blobs
    for blob in blobs:
        newFoods = []
        for food in foods:
            if blob.size > blob.distToPoint(food.pos[0], food.pos[1]):
                blob.eat(food)
            else:
                newFoods.append(food)
        foods = newFoods
            
def checkIfRottenFood():
    global foods
    newFoods = []

    for food in foods:
        if food.age < food.maxAge:
            newFoods.append(food)
    foods = newFoods


def checkIfTooSmall():
    global blobs
    newblobs = []
    for blob in blobs:
        if blob.size > MIN_BLOB_SIZE:
            newblobs.append(blob)
        else:
            print("Tragic death:", blob.dna)

    blobs = newblobs

def checkIfTooLarge():
    global blobs
    newblobs = []
    for blob in blobs:
        if blob.readyToSplitt():
            newblobs += blob.split()
        else:
            newblobs.append(blob)

    blobs = newblobs


def getBlobInfo():
    global blobs
    global lastBlobInfo

    lastBlobInfo = None
    mouseX,mouseY = pygame.mouse.get_pos()
    for blob in blobs:
        if blob.distToPoint(mouseX,mouseY) < blob.size*2:
            print(blob.dna)
            lastBlobInfo = blob.dna

def update():
    global blobs

    if len(foods) < FOOD_AMOUNT:
        foods.append(Food([random.randint(0,window.get_width()), random.randint(0, window.get_height())], window))
        
    
    for blob in blobs:
        blob.update()
        
    for food in foods:
        food.update()

    checkIfRottenFood()
    checkIfEaten()
    checkIfTooSmall()
    checkIfTooLarge()

    

def draw():
    global lastBlobInfo

    for food in foods:
        food.draw()
    
    for blob in blobs:
        blob.draw()

    if pygame.font and lastBlobInfo:
        f = pygame.font.Font(None, 64)
        text = f.render(str(lastBlobInfo),True, (0,0,0))
        textPos = text.get_rect(centerx=window.convert().get_width()/2, y=10)
        window.blit(text,textPos)

while True:
    window.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            getBlobInfo()

    update()
    draw()    
        

    pygame.display.flip()

    fpsClock.tick(FPS)
