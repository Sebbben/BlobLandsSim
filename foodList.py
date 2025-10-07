class FoodList(list):
    def __init__(self):
        super().__init__()

    def append(self, f):
        for i in range(len(self)):
            if self[i].pos[0] > f.pos[0]:
                self.insert(i, f)
                break
        else:  
            super().append(f)
    
    def getRange(self, rng):
        """Returns a list of food objects that are in the given range on the x-axis"""
        upper = len(self)
        lower = 0

        xFind = []

        while upper > lower:
            x = (upper + lower) // 2
            if rng[0] < self[x].pos[0] < rng[1]:
                for i in range(x, upper):
                    if self[i].pos[0] < rng[1]:
                        xFind.append(self[i])
                    else:
                        break
                for i in range(x-1, lower, -1):
                    if rng[0] < self[i].pos[0]:
                        xFind.append(self[i])
                    else:
                        break
                break
            elif self[x].pos[0] > rng[1]:
                upper = x - 1
            else:
                lower = x + 1

        return xFind

    def removeRotten(self):
        self.blobs = filter(lambda f:f.rotten(), self)
        