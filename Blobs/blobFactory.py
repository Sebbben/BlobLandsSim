from pygame import Vector2


class BlobFactory:
    @staticmethod
    def createBlob(size:float, pos:Vector2, window, infant):
        if infant.dna["type"] == "Herbivore":
            return herbivore.Herbivore(size, pos, window, infant)
        if infant.dna["type"] == "Carnivore":
            return carnivore.Carnivore(size, pos, window, infant)
        if infant.dna["type"] == "Parasite":
            return parasite.Parasite(size, pos, window, infant)

import Blobs.carnivore as carnivore
import Blobs.herbivore as herbivore
import Blobs.parasite as parasite # DO NOT MOVE, NEEDS TO MAKE IMPORT AS LAST THING THAT HAPPENES IN FILE