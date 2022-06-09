class FoodList(list):
    def __init__(self):
        super().__init__()
    
    def getRange(self, rng):

        upper = len(self)
        lower = 0

        mid = lambda: (upper + lower) // 2
        xFind = []        

        while upper > lower:
            x = mid()
            if rng[0] < self[x].pos.x < rng[1] :#self[x] != self and self.pos.x-rng < self[x].pos.x < self.pos.x+rng:
                for i in range(x, upper):
                    if self[i].pos.x < rng[1]:
                        xFind.append(self[i])
                    else:
                        break
                for i in range(x-1, lower, -1):
                    if rng[0] < self[i].pos.x:
                        xFind.append(self[i])
                    else:
                        break
                break
            elif self[x].pos.x > rng[1]:
                upper = x - 1
            else:
                lower = x + 1

        return xFind

    def removeRotten(self):
        self.blobs = filter(lambda f:f.rotten(), self)
        