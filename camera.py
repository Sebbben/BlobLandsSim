class Camera:
    def __init__(self):
        self.pos = [0,0]
        self.target = self.pos.copy()
        
    def setTarget(self, target):
        self.target = target 

    def moveTarget(self,x,y):
        self.target[0] += x
        self.target[1] += y

    def update(self):
        self.pos = self.target