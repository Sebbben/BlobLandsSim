class BlobFactory:
    @staticmethod
    def createBlob(size:float, pos:list, window, SIMULATION_SIZE:list, dna = {}):
        if not dna:
            return herbivore.Herbivore(size, pos, window, SIMULATION_SIZE, dna)
        if dna["type"] == "Herbivore":
            return herbivore.Herbivore(size, pos, window, SIMULATION_SIZE, dna)
        if dna["type"] == "Carnivore":
            return carnivore.Carnivore(size, pos, window, SIMULATION_SIZE, dna)
        if dna["type"] == "Parasite":
            return parasite.Parasite(size, pos, window, SIMULATION_SIZE, dna)

import Blobs.carnivore as carnivore
import Blobs.herbivore as herbivore
import Blobs.parasite as parasite # DO NOT MOVE, NEEDS TO MAKE IMPORT AS LAST THING THAT HAPPENES IN FILE