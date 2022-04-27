import pygame
import sys, random
from blob import Blob
from food import Food


FOOD_AMOUNT = 300
START_NUMBER_OF_BLOBS = 3
START_BLOB_SIZE = 10


pygame.init()

window = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()


blobs = []
foods = []

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
            

def update():
    
    if len(foods) < FOOD_AMOUNT:
        foods.append(Food([random.randint(0,window.get_width()), random.randint(0, window.get_height())], window))
        
    
    for blob in blobs:
        blob.update()


    checkIfEaten()

    

def draw():
    for food in foods:
        food.draw()
    
    for blob in blobs:
        blob.draw()

while True:
    window.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    update()
    draw()    
        

    pygame.display.flip()

    fpsClock.tick(FPS)
