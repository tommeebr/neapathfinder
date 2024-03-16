from node import Node
import math
import heapq
import numpy as np

class PathFinder:
    def __init__(self, start, end):
        self.start = start
        self.end = end

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

    def getNeighbour(self, node, grid):
        raise NotImplementedError("This method should be overridden in a subclass")  

    def findPath(self):
        raise NotImplementedError("This method should be overridden in a subclass")

    def loadFile(self, file_path):
        pass

class GridPathFinder(PathFinder):
    def getNeighbour(self, node, grid):
        # ... existing code ...

    def aStar(self, grid):
        # ... existing code ...

class MazePathFinder(PathFinder):
    def getNeighbour(self, node, maze):
        # ... existing code ...

    def aStar(self, maze):
        # ... existing code ...

