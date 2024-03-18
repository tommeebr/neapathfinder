from pathfinder import PathFinder
from node import Node

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
