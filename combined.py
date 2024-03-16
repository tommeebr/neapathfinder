import heapq
import math

class Node:
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.pos == other.pos

from node import Node
import math
import heapq

class PathFinder:
    @staticmethod
    def manhattanDist(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    @staticmethod
    def getGridNeighbour(node, grid):
        neighbors = []
        for newPos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            nodePos = (node.pos[0] + newPos[0], node.pos[1] + newPos[1])
            if nodePos[0] < 0 or nodePos[0] >= len(grid) or nodePos[1] < 0 or nodePos[1] >= len(grid[0]):
                continue  # Node is out of bounds
            if grid[nodePos[0]][nodePos[1]] != 0:
                continue  # Node is not walkable
            neighbors.append(Node(node, nodePos))
        return neighbors

    @staticmethod
    def aStarGrid(start, end, grid):
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
                manhattanDistTotal = sum(PathFinder.manhattanDist(path[i], path[i+1]) for i in range(len(path) - 1))

                print("Total Manhattan distance for path:", manhattanDistTotal)


                return path

            children = PathFinder.getGridNeighbour(currentNode, grid)
            for child in children:
                if child in closedList:
                    continue  # Child is already in the closed list
                child.g = currentNode.g + 1
                child.h = PathFinder.manhattanDist(child.pos, endNode.pos)
                child.f = child.g + child.h

                if any(openNode for openNode in openList if child == openNode[2] and child.g > openNode[2].g):
                    continue  # Child is already in the open list and has a higher g value

                count += 1  # Increment counter
                heapq.heappush(openList, (child.f, count, child))  # Add the child to the open list
        
    @staticmethod
    def getMazeNeighbour(node, maze):
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
    

    @staticmethod
    def aStarMaze(start, end, maze):
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
                manhattanDistTotal = sum(PathFinder.manhattanDist(path[i], path[i+1]) for i in range(len(path) - 1))

                print("Total Manhattan distance for path:", manhattanDistTotal)

                return path

            children = PathFinder.getMazeNeighbour(currentNode, maze)
            for child in children:
                if child in closedList:
                    continue  # Child is already in the closed list
                child.g = currentNode.g + 1
                child.h = PathFinder.manhattanDist(child.pos, endNode.pos)
                child.f = child.g + child.h

                if any(openNode for openNode in openList if child == openNode[2] and child.g > openNode[2].g):
                    continue  # Child is already in the open list and has a higher g value

                count += 1  # Increment counter
                heapq.heappush(openList, (child.f, count, child))  # Add the child to the open list
        
    @staticmethod
    def displayPathOnGrid(grid, path):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if (i, j) in path:
                    print(' X', end='')
                else:
                    print(' -', end='')
            print()  # Newline after each row    

    


pF = PathFinder() 

grid = [
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 1 ,1 ,0 ,0]
]
start = (0, 0)
end = (4, 8)
path = pF.aStarGrid(start, end, grid)
print(path)  # Output: [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
pF.displayPathOnGrid(grid,path)

maze = [
    [3,2,3,2,1,2,2,2,3,2],
    [1,1,0,2,1,2,2,1,1,1],
    [1,2,1,1,2,2,2,0,2,0],
    [3,1,1,2,2,3,2,2,3,0],
    [1,0,3,2,1,0,3,0,3,2],
    [3,0,1,1,2,2,1,2,1,1],
    [1,3,1,3,0,1,2,1,1,2],
    [1,0,1,3,2,1,1,0,3,0],
    [3,0,1,1,1,2,2,2,0,1],
    [1,2,1,0,1,3,2,2,2,0]
]

start = (0,4)
end = (9,5)
path = PathFinder.aStarMaze(start, end, maze)
print(path)
pF.displayPathOnGrid(maze,path)