from node import Node
import math
import heapq
import numpy as np

class PathFinder:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
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

    def aStar(self, start, end, grid):
        startNode = Node(None, start)
        endNode = Node(None, end)

        openList = []
        closedList = []

        count = 0  # Counter for tie-breaking
        heapq.heappush(openList, (startNode.f, count, startNode))  # Add the start node

        while len(openList) > 0:
            currentNode = heapq.heappop(openList)[2]  # Node with the lowest f value
            closedList.append(currentNode)

            if currentNode == endNode:  # Found the goal
                path = []
                while currentNode is not None:
                    path.append(currentNode.pos)
                    currentNode = currentNode.parent
                path = path[::-1]  # Reverse the path

                # Calculate the Manhattan distances for the final path
                manhattanDistTotal = sum(self.manhattanDist(path[i], path[i+1]) for i in range(len(path) - 1))

                print("Total Manhattan distance for path:", manhattanDistTotal)


                return path

            children = self.getNeighbour(currentNode, grid)
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
    

    def generateStructure(self, start, end, height, width):
        raise NotImplementedError("This method should be overridden in a subclass")

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
        self.structure = [list(map(int, line.strip().split(','))) for line in lines[2:]]


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

    def generateStructure(self, start, end, height, width):
        #* I need to implement this method
        pass

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

    def generateStructure(self, start, end, height, width):
        #* I need to implement this method
        pass

