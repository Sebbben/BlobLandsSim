from random import randint as ri
# ---------- main settings -------------
FPS = 120 # frames per second setting
WIN_W = 1920
WIN_H = 1080

SIMULATION_SIZE = [4000, 4000]

FOOD_DENCITY = 1/7000
FOOD_AMOUNT = int((SIMULATION_SIZE[0]*SIMULATION_SIZE[1])*FOOD_DENCITY)
FOOD_COLOR = lambda: (0,ri(180,255),0)
NEW_FOOD_PER_FRAME = int(FOOD_AMOUNT/(FPS*5))

START_NUMBER_OF_BLOBS = 1
START_BLOB_SIZE = 20

CAMERA_SPEED = 10
WINDOW_RES = (1080,720)

# data collection settings

DATA_COLLECTION_FRAME_INTERVAL = FPS*5


# ---------- general blob settings ---------
 
MIN_BLOB_SIZE = 5
MAX_MUTATION = 1/4

# ---------- per blob settings ----------- 

# Herbivore
HERBIVORE_COLOR = (100,70,19)
HERBIVORE_ENERGY_CONSUMPTION = 1/100

# Carnivore
CARNIVORE_COLOR = (200,50,50)
CARNIVORE_ENERGY_CONSUMPTION = 1/1000

# Parasite
PARASITE_COLOR = (255,255,0)
PARASITE_ENERGY_CONSUMPTION = 1/1000
PARASITE_HOSTLESS_ENERGY_CONSUMPTION_MILTUPLIER = 1 


# --------------- camera settings ------------
CAMERA_ZOOM_SNAP_DISTANCE = 0.001
CAMERA_MOVE_SNAP_DISTANCE = 0.1
CAMERA_SMOOTHNESS = 1/50