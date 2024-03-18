from pathfinder import PathFinder
from node import Node
import numpy as np

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

    
        