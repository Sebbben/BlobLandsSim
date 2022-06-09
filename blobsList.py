class BlobList:
    def __init__(self):
        self.blobs = []


    def __iadd__(self, b):
        self.blobs += b
        return self

    def __iter__(self):
        return self.blobs.__iter__()

    def __len__(self):
        return len(self.blobs)

    def append(self,b):
        self.blobs.append(b)
        
