from settings import *

class Camera:
    def __init__(self, window):
        self.pos = [0,0]
        self.target = self.pos.copy()
        self.smoothness = 1/50
        self.zoomLvl = 1
        self.zoomTarget = 1
        self.window = window
        self.simsize = SIMULATION_SIZE
        
    def nonSmoothMove(self, pos:list):
        self.target[0] += pos[0]
        self.target[1] += pos[1]
        self.pos[0] += pos[0]
        self.pos[1] += pos[1]

    def setTarget(self, target):
        self.target = target 

    def moveTarget(self,x,y):
        self.target[0] += x
        self.target[1] += y

    def update(self):
        moveX = (self.target[0]-self.pos[0])*self.smoothness
        moveY = (self.target[1]-self.pos[1])*self.smoothness
        
        if abs(moveX) + abs(moveY) < 0.1:
            self.pos[0] = self.target[0]
            self.pos[1] = self.target[1]
        else:
            self.pos[0] += moveX
            self.pos[1] += moveY


        if round(abs(self.zoomTarget - self.zoomLvl),5) < 0.001:
            self.zoomLvl = self.zoomTarget
        else:
            self.zoomLvl += (self.zoomTarget - self.zoomLvl)*self.smoothness

    def zoom(self,z:float):
        self.zoomTarget += z
        
    def center(self):

        self.zoomLvl = 1
        self.zoomTarget = 1

        onscreenSimMidPos = self.getScreenPos([self.simsize[0]//2, self.simsize[1]//2])
        
        diffX = onscreenSimMidPos[0] - self.window.get_width()//2
        diffY = onscreenSimMidPos[1] - self.window.get_height()//2


        self.target[0] += diffX
        self.target[1] += diffY
        self.pos[0] += diffX
        self.pos[1] += diffY

        zoomX = self.window.get_width()/self.simsize[0]
        zoomY = self.window.get_height()/self.simsize[1]

        self.zoomTarget = min(zoomX,zoomY)-0.1


    def getScreenPos(self, worldPos):
        return [int(worldPos[0] - self.pos[0]) *self.zoomLvl + self.window.get_width()/2, int(worldPos[1] - self.pos[1]) *self.zoomLvl + self.window.get_height()/2]