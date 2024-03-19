import heapq
import math
import random
import numpy as np

class Node:
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.pos == other.pos

class PathFinder:
    def __init__(self, *args):
        self.path = []
        if len(args) == 1 and isinstance(args[0], str):
            self.loadFile(args[0])
        elif len(args) == 4 and all(isinstance(arg, (int,tuple)) for arg in args):
            self.start, self.end, self.height, self.width = args
            if self.width % 2 == 0:
                self.width -= 1
                self.end = (self.end[0] - 1, self.end[1]) # Tuples are immutable, so have to assign it to a new one
            if self.height % 2 == 0:
                self.height -= 1
                self.end = (self.end[0], self.end[1] - 1) # ^^^
            if self.end[0] >= self.width or self.end[1] >= self.height:
                raise ValueError("End position must be within the bounds of the maze")
            if self.start[0] < 0 or self.start[1] < 0 or self.end[0] < 0 or self.end[1] < 0:
                raise ValueError("Start and end positions must be non-negative")
            self.structInstance = StructureGenerator(self.start, self.end, self.height, self.width)
            self.structure, self.width, self.height, self.end = self.structInstance.generateMaze()  # Update width, height and end
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

class GridPathFinder(PathFinder):
    def getNeighbour(self, node, grid):
        neighbors = []
        for newPos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            nodePos = (node.pos[0] + newPos[0], node.pos[1] + newPos[1])
            if nodePos[0] < 0 or nodePos[0] >= len(grid) or nodePos[1] < 0 or nodePos[1] >= len(grid[0]):
                continue  # Node is out of bounds
            if grid[nodePos[0]][nodePos[1]] != 0:
                continue  # Node is not walkable
            neighbors.append(Node(node, nodePos))
        return neighbors

class MazePathFinder(PathFinder):
    def getNeighbour(self, node, maze):
        neighbors = []
        for newPos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            nodePos = (node.pos[0] + newPos[0], node.pos[1] + newPos[1])
            if nodePos[0] < 0 or nodePos[0] >= len(maze) or nodePos[1] < 0 or nodePos[1] >= len(maze[0]):
                continue  # Node is out of bounds

            # Check for walls
            if newPos == (0, -1):  # Moving left
                if maze[node.pos[0]][node.pos[1]] & 1:  # There's a left wall
                    continue
            elif newPos == (0, 1):  # Moving right
                if nodePos[0] < len(maze) and maze[nodePos[0]][nodePos[1]] & 1:  # There's a left wall in the next cell
                    continue
            elif newPos == (-1, 0):  # Moving up
                if maze[node.pos[0]][node.pos[1]] & 2:  # There's a top wall
                    continue
            elif newPos == (1, 0):  # Moving down
                if nodePos[0] < len(maze) and maze[nodePos[0]][nodePos[1]] & 2:  # There's a top wall in the next cell
                    continue

            neighbors.append(Node(node, nodePos))
        return neighbors

<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
class StructureGenerator:
    def __init__(self, start, end, width,height):
        self.start = start
        self.end = end
        self.width = width
        self.height = height
        self.maze = np.ones((height, width), dtype=np.int8)
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, left, down, up

    def generateMaze(self):
        #! Ensure dimensions are odd - for some reason it makes the final row and column full of walls? could fix this
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
        self.maze[self.start[1]][self.start[0]] = 0  # Ensure start is traversable
        self.maze[self.end[1]][self.end[0]] = 0  # Ensure end is traversable
        return self.maze.tolist(), self.width, self.height, self.end  # Return adjusted width, height and end
    
    def _dfs(self, x, y):
        #! Cannot use even numbers for width and height for some reason
        self.maze[y][x] = 0
        np.random.shuffle(self.directions)
        for dx, dy in self.directions:
            nextX, nextY = x + 2*dx, y + 2*dy
            if (0 <= nextX < self.width) and (0 <= nextY < self.height) and self.maze[nextY][nextX] == 1:
                self.maze[nextY-dy][nextX-dx] = 0
                self._dfs(nextX, nextY)


gridPF = GridPathFinder((0, 0), (9, 9), 10, 10)
gridPF.aStar()
gridPF.displayStructure()
gridPF.displayPathOnStructure()