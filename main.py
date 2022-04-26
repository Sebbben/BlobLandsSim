import pygame
import sys, random
from blob import Blob
from food import Food


FOOD_AMOUNT = 100

pygame.init()

window = pygame.display.set_mode((800, 600))


FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()



blobs = []
foods = []

for _ in range(2):
    blobs.append(Blob(10,[random.randint(0,window.get_width()), random.randint(0, window.get_height())], window))

for _ in range(2):
    foods.append(Food([random.randint(0,window.get_width()), random.randint(0, window.get_height())], window))

def update():
    
    if len(foods) < FOOD_AMOUNT:
        foods.append(Food([random.randint(0,window.get_width()), random.randint(0, window.get_height())], window))
        
    
    for blob in blobs:
        blob.update()

    

def draw():
    for blob in blobs:
        blob.draw()
    
    for food in foods:
        food.draw()

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
