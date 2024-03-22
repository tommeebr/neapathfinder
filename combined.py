import heapq
import math
import random
import numpy as np

class Node:
    def __init__(self, parent=None, pos=None):
        self.parent = parent # Parent node
        self.pos = pos # (x, y) coordinates
        self.g = 0 # Cost to start node
        self.h = 0 # Heuristic cost
        self.f = 0 # Total cost of the node

    def __eq__(self, other):
        return self.pos == other.pos

class PathFinder:
    def __init__(self, *args): 
        self.path = [] 
        self.fileInit = False
        if len(args) == 1 and isinstance(args[0], str): 
            self.loadFile(args[0])
            self.fileInit = True
        elif len(args) == 4 and all(isinstance(arg, tuple) for arg in args[:2]) and all(isinstance(arg, int) for arg in args[2:]): 
            self.start, self.end, self.height, self.width = args
            self.validateInputs()
            self.structInstance = StructureGenerator(self.start, self.end, self.height, self.width) 
        else: 
            raise ValueError("Must provide either a file path or height and width") 

                
    def validateInputs(self):
        if self.width % 2 == 0:
            self.width -= 1
            self.end = (self.end[0] - 1, self.end[1]) # Tuples are immutable, so have to assign it to a new one
            print(f'EVEN Width not permitted. Adjusting width to {self.width}')
        if self.height % 2 == 0:
            self.height -= 1
            self.end = (self.end[0], self.end[1] - 1) # ^^^
            print(f'EVEN Height not permitted. Adjusting height to {self.height}')
        if self.end[0] >= self.width or self.end[1] >= self.height:
            raise ValueError("End position must be within the bounds of the maze")
        if self.start[0] < 0 or self.start[1] < 0 or self.end[0] < 0 or self.end[1] < 0:
            raise ValueError("Start and end positions must be non-negative")
        
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
    
    def solvableStructure(self):
        if self.fileInit == True:
            self.aStar()
        else:
            while True:
                self.generateStructure()
                if self.aStar():
                    break

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

            children = self.getNeighbour(currentNode)
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
        try:
            with open(filePath, 'r') as file:
                lines = file.readlines()

            # Parse start and end positions
            self.start = tuple(map(int, lines[0].strip().split(',')))
            self.end = tuple(map(int, lines[1].strip().split(',')))

            # Construct the 2D array
            self.structure = [list(map(int, line.strip().split(','))) for line in lines[2:]]

            self.height, self.width = len(self.structure), len(self.structure[0])
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filePath} not found.")
        except ValueError:
            print("Could not parse the file. Make sure it is in the correct format.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    def generateStructure(self):
        raise NotImplementedError("This method should be overridden in a subclass")

class GridPathFinder(PathFinder):
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
        self.structInstance = GridGenerator(self.start, self.end, self.height, self.width)
        structure, self.width, self.height, self.end = self.structInstance.generateStructure()
        self.structure = structure

class MazePathFinder(PathFinder):
    def getNeighbour(self, node):
        neighbors = []
        for newPos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            nodePos = (node.pos[0] + newPos[0], node.pos[1] + newPos[1])
            if nodePos[0] < 0 or nodePos[0] >= len(self.structure) or nodePos[1] < 0 or nodePos[1] >= len(self.structure[0]):
                continue  # Node is out of bounds

            # Check for walls
            #* Bitwise AND operation to check for walls
            if newPos == (0, -1):  # Moving left
                if self.structure[node.pos[0]][node.pos[1]] & 1:  # There's a left wall 
                    continue
            elif newPos == (0, 1):  # Moving right
                if nodePos[0] < len(self.structure) and self.structure[nodePos[0]][nodePos[1]] & 1:  # There's a left wall in the next cell
                    continue
            elif newPos == (-1, 0):  # Moving up
                if self.structure[node.pos[0]][node.pos[1]] & 2:  # There's a top wall
                    continue
            elif newPos == (1, 0):  # Moving down
                if nodePos[0] < len(self.structure) and self.structure[nodePos[0]][nodePos[1]] & 2:  # There's a top wall in the next cell
                    continue

            neighbors.append(Node(node, nodePos))
        return neighbors
    
    def generateStructure(self):
        self.structInstance = MazeGenerator(self.start, self.end, self.height, self.width)
        structure, self.width, self.height, self.end = self.structInstance.generateStructure()
        self.structure = structure


    
class StructureGenerator():
    def __init__(self, start, end, width,height):
        self.start = start
        self.end = end
        self.width = width
        self.height = height
        self.array = np.ones((height, width), dtype=np.int8)
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, left, down, up
    
    def _dfs(self, x, y):
        #! Cannot use even numbers for width and height for some reason
        self.array[y][x] = 0
        np.random.shuffle(self.directions)
        for dx, dy in self.directions:
            nextX, nextY = x + 2*dx, y + 2*dy
            if (0 <= nextX < self.width) and (0 <= nextY < self.height) and self.array[nextY][nextX] == 1:
                self.array[nextY-dy][nextX-dx] = 0
                self._dfs(nextX, nextY)
    
    def generateStructure(self):
        raise NotImplementedError("This method should be overridden in a subclass")
    

class GridGenerator(StructureGenerator):
    def generateStructure(self):
        #! Ensure dimensions are odd - for some reason it makes the final row and column full of walls? could do with fixing this
        if self.width % 2 == 0:
            self.width -= 1
        if self.height % 2 == 0:
            self.height -= 1

        # Adjust end position if it falls outside the adjusted grid size
        if self.end[0] >= self.width:
            self.end = (self.width - 1, self.end[1])
        if self.end[1] >= self.height:
            self.end = (self.end[0], self.height - 1)

        self._dfs(self.start[0], self.start[1])
        self.array[self.start[1]][self.start[0]] = 0  # Ensure start is traversable
        self.array[self.end[1]][self.end[0]] = 0  # Ensure end is traversable
        return self.array.tolist(), self.width, self.height, self.end  # Return adjusted width, height and end
    
class MazeGenerator(StructureGenerator):
    def generateStructure(self):
        raise NotImplementedError("This method has not yet been implemented")
        
gridPF = GridPathFinder('assets/grid/grid1.txt')
gridPF.solvableStructure()

gridPF.displayStructure()
gridPF.displayPathOnStructure()