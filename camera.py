class Camera:
    def __init__(self):
        self.pos = [0,0]
        self.target = self.pos.copy()
        self.smoothness = 1/25
        
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