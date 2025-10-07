from pygame import Rect
import numpy as np
from settings import *

class Camera:
    def __init__(self, window):
        self.pos = np.array([0.0,0.0])
        self.target = np.array([0.0,0.0])
        self.smoothness = CAMERA_SMOOTHNESS
        self.zoomLvl = 1
        self.zoomTarget = 1
        self.window = window
        self.simsize = SIMULATION_SIZE

        self.visibleWorldTopLeft = np.array((0,0))
        self.visibleWorldBottomRight = np.array((0,0))

        
    def nonSmoothMove(self, pos:np.typing.NDArray):
        self.target += pos
        self.pos += pos

    def setTarget(self, target:np.typing.NDArray):
        self.target = target 

    def moveTarget(self,x,y): # TODO
        self.target += np.array([x,y])

    def update(self):
        moveVec = (self.target - self.pos)*self.smoothness

        if np.linalg.vector_norm(moveVec) < CAMERA_MOVE_SNAP_DISTANCE:
            self.pos = np.array(self.target)
        else:
            self.pos += moveVec

        if round(abs(self.zoomTarget - self.zoomLvl),5) < CAMERA_ZOOM_SNAP_DISTANCE:
            self.zoomLvl = self.zoomTarget
        else:
            self.zoomLvl += (self.zoomTarget - self.zoomLvl)*self.smoothness

        self.visibleWorldTopLeft = self.getWorldPos(np.array([0,0]))
        self.visibleWorldBottomRight = self.getWorldPos(np.array(self.window.get_size()))     

    def zoom(self,z:float):
        self.zoomTarget += z
        
    def center(self):
        onscreenSimMidPos = self.getScreenPos([self.simsize[0]/2, self.simsize[1]/2])
        winSize = np.array(self.window.get_size())/2
        
        diff = onscreenSimMidPos-winSize

        self.target += diff
        self.pos += diff
        
        zoomX = self.window.get_width()/self.simsize[0]
        zoomY = self.window.get_height()/self.simsize[1]

        self.zoomTarget = min(zoomX,zoomY)

    
    def getScreenPos(self, worldPos):
        return (worldPos - self.pos) * self.zoomLvl + (np.array(self.window.get_size())/2)

    def getWorldPos(self, vec: np.typing.NDArray):
        return (vec - (np.array(self.window.get_size())/2)) / self.zoomLvl + self.pos

    def isOnScreen(self, vec: np.typing.NDArray):
        # if not self.visibleWorldRect: return True
        return self.visibleWorldTopLeft[0] <= vec[0] <= self.visibleWorldBottomRight[0] and self.visibleWorldTopLeft[1] <= vec[1] <= self.visibleWorldBottomRight[1]
