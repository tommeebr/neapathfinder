from node import Node
import math
import heapq
import numpy as np

class PathFinder:
    def __init__(self, *args):
        if len(args) == 2 and isinstance(args[0], str):
            self.loadFile(args[0])
        elif len(args) == 4 and all(isinstance(arg, int) for arg in args):
            self.start, self.end, height, width = args
            self.generateStructure(self.start,self.end,height, width)
        else:
            raise ValueError("Must provide either a file path or height and width")
        
    def manhattanDist(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def displayPathOnGrid(self, grid, path):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if (i, j) in path:
                    print(' X', end='')
                else:
                    print(' -', end='')
            print()  # Newline after each row
    
    def generateStructure(self, start, end, height, width):
        raise NotImplementedError("This method should be overridden in a subclass")

    def getNeighbour(self, node, grid):
        raise NotImplementedError("This method should be overridden in a subclass")  

    def findPath(self):
        raise NotImplementedError("This method should be overridden in a subclass")

    def loadFile(self, filePath):
        #! i need to implement start and ends in the files to read
        pass

class GridPathFinder(PathFinder):
    def getNeighbour(self, node, grid):
        # ... existing code ...

    def aStar(self, start, end, grid):
        # ... existing code ...

    def generateStructure(self, start, end, height, width):
        self.structure = np.zeros((height, width))

class MazePathFinder(PathFinder):
    def getNeighbour(self, node, maze):
        # ... existing code ...

    def aStar(self, start, end, maze):
        # ... existing code ...

    def generateStructure(self, start, end, height, width):
        self.structure = np.zeros((height, width))

