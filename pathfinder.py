from node import Node
import math
import heapq
import numpy as np
from structuregenerator import StructureGenerator

class PathFinder:
    def __init__(self, *args):
        self.path = []
        if len(args) == 1 and isinstance(args[0], str):
            self.loadFile(args[0])
        elif len(args) == 4 and all(isinstance(arg, (int,tuple)) for arg in args):
            self.start, self.end, self.height, self.width = args
            self.structInstance = StructureGenerator(self.start, self.end, self.height, self.width)
            self.structure = self.structInstance.generateMaze()
        else:
            raise ValueError("Must provide either a file path or height and width")
        
    def manhattanDist(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def displayStructure(self):
        for row in self.structure:
            print(' '.join(str(cell) for cell in row))

    def displayPathOnStructure(self):
        for i in range(len(self.structure)):
            for j in range(len(self.structure[0])):
                if (i, j) in self.path:
                    print(' X', end='')
                else:
                    print(' -', end='')
            print()  # Newline after each row

    def aStar(self):
        startNode = Node(None, (self.start[1], self.start[0]))  
        endNode = Node(None, (self.end[1], self.end[0]))  

        openList = []
        closedList = []

        count = 0  # Counter for tie-breaking
        heapq.heappush(openList, (startNode.f, count, startNode))  # Add the start node

        while len(openList) > 0:
            currentNode = heapq.heappop(openList)[2]  # Node with the lowest f values
            closedList.append(currentNode)

            if currentNode == endNode:  # Found the goal
                path = []
                while currentNode is not None:
                    path.append(currentNode.pos)
                    currentNode = currentNode.parent
                self.path = path[::-1]  # Reverse the path

                # Calculate the Manhattan distances for the final path
                manhattanDistTotal = sum(self.manhattanDist(path[i], path[i+1]) for i in range(len(path) - 1))

                print("Total Manhattan distance for path:", manhattanDistTotal)
                return True

            children = self.getNeighbour(currentNode, self.structure)
            for child in children:
                if child in closedList:
                    continue  # Child is already in the closed list
                child.g = currentNode.g + 1
                child.h = self.manhattanDist(child.pos, endNode.pos)
                child.f = child.g + child.h

                if any(openNode for openNode in openList if child == openNode[2] and child.g > openNode[2].g):
                    continue  # Child is already in the open list and has a higher g value

                count += 1  # Increment counter
                heapq.heappush(openList, (child.f, count, child))  # Add the child to the open list          
        return False
    def getNeighbour(self, node, grid):
        raise NotImplementedError("This method should be overridden in a subclass")  

    def findPath(self):
        raise NotImplementedError("This method should be overridden in a subclass")

    def loadFile(self, filePath):
        with open(filePath, 'r') as file:
            lines = file.readlines()

        # Parse start and end positions
        self.start = tuple(map(int, lines[0].strip().split(',')))
        self.end = tuple(map(int, lines[1].strip().split(',')))

        # Construct the 2D array
        self.structure = np.array([list(map(int, line.strip().split(','))) for line in lines[2:]])