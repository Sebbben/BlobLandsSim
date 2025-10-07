from pygame import Vector2, Rect
from settings import *

class Camera:
    def __init__(self, window):
        self.pos = Vector2()
        self.target = Vector2()
        self.smoothness = CAMERA_SMOOTHNESS
        self.zoomLvl = 1
        self.zoomTarget = 1
        self.window = window
        self.simsize = SIMULATION_SIZE

        self.visibleWorldTopLeft = None
        self.visibleWorldBottomRight = None
        self.visibleWorldRect = Rect((0,0), self.window.get_size())

        
    def nonSmoothMove(self, pos:Vector2|list):
        self.target += pos
        self.pos += pos

    def setTarget(self, target:Vector2):
        self.target = target 

    def moveTarget(self,x,y):
        self.target.x += x
        self.target.y += y

    def update(self):
        moveVec = (self.target - self.pos)*self.smoothness

        if moveVec.magnitude() < CAMERA_MOVE_SNAP_DISTANCE:
            self.pos = Vector2(self.target)
        else:
            self.pos += moveVec

        if round(abs(self.zoomTarget - self.zoomLvl),5) < CAMERA_ZOOM_SNAP_DISTANCE:
            self.zoomLvl = self.zoomTarget
        else:
            self.zoomLvl += (self.zoomTarget - self.zoomLvl)*self.smoothness

        self.visibleWorldTopLeft = self.getWorldPos([0,0])
        self.visibleWorldRect.update(self.visibleWorldTopLeft, [self.window.get_size()[0]/self.zoomLvl, self.window.get_size()[1]/self.zoomLvl])
        

    def zoom(self,z:float):
        self.zoomTarget += z
        
    def center(self):

        self.zoomLvl = 1
        self.zoomTarget = 1

        onscreenSimMidPos = self.getScreenPos([self.simsize[0]//2, self.simsize[1]//2])
        winSize = Vector2(self.window.get_width()//2,self.window.get_height()//2)
        
        diff = onscreenSimMidPos-winSize

        self.target += diff
        self.pos += diff
        
        zoomX = self.window.get_width()/self.simsize[0]
        zoomY = self.window.get_height()/self.simsize[1]

        self.zoomTarget = min(zoomX,zoomY)-0.1

    
    def getScreenPos(self, worldPos):
        return Vector2(
            int(worldPos[0] - self.pos[0]) * self.zoomLvl + self.window.get_width()/2, 
            int(worldPos[1] - self.pos[1]) * self.zoomLvl + self.window.get_height()/2
        )

    def getWorldPos(self, vec: Vector2|list):
        return Vector2(
            (vec[0] - self.window.get_width()/2)/self.zoomLvl +self.pos[0], 
            (vec[1] - self.window.get_height()/2)/self.zoomLvl +self.pos[1], 
        )

    def isOnScreen(self, vec: Vector2):
        if not self.visibleWorldRect: return True
        return self.visibleWorldRect.left <= vec.x <= self.visibleWorldRect.right and self.visibleWorldRect.top <= vec.y <= self.visibleWorldRect.bottom
        return self.visibleWorldRect.collidepoint(vec)