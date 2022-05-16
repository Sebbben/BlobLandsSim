class Camera:
    def __init__(self, window):
        self.pos = [0,0]
        self.target = self.pos.copy()
        self.smoothness = 1/50
        self.zoomLvl = 1
        self.zoomTarget = 1
        self.moveSnapDistance = 10
        self.zoomSnap = 0.05
        self.window = window
        
    def setTarget(self, target):
        self.target = target 

    def moveTarget(self,x,y):
        self.target[0] += x
        self.target[1] += y

    def update(self):
        moveX = (self.target[0]-self.pos[0])*self.smoothness
        moveY = (self.target[1]-self.pos[1])*self.smoothness
        self.pos[0] += moveX
        self.pos[1] += moveY

        self.zoomLvl += (self.zoomTarget - self.zoomLvl)*self.smoothness

        



    def zoom(self,z:float):
        self.zoomTarget += z
        
    
    
    def getScreenPos(self, worldPos):
        return [int(worldPos[0] - self.pos[0]) *self.zoomLvl + self.window.get_width()/2, int(worldPos[1] - self.pos[1]) *self.zoomLvl + self.window.get_height()/2]