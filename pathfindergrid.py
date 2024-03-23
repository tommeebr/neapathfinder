from pathfinder import PathFinder
from node import Node
import numpy as np
from generatorgrid import GeneratorGrid

class PathFinderGrid(PathFinder):
    def __init__(self, *args): 
        super().__init__(*args)

    def getNeighbour(self, node):
        neighbors = []
        for newPos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            nodePos = (node.pos[0] + newPos[0], node.pos[1] + newPos[1])
            if nodePos[0] < 0 or nodePos[0] >= self.height or nodePos[1] < 0 or nodePos[1] >= self.width:
                continue  # Node is out of bounds
            if self.structure[nodePos[0]][nodePos[1]] != 0:
                continue  # Node is not walkable
            neighbors.append(Node(node, nodePos))
        return neighbors
    
    def generateStructure(self):
        self.structInstance = GeneratorGrid(self.start, self.end, self.height, self.width)
        structure, self.width, self.height, self.end = self.structInstance.generateStructure()
        self.structure = structure

    
        