from pathfinder import PathFinder
from node import Node
from structuregenerator import StructureGenerator

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
        self.structInstance = StructureGenerator(self.start, self.end, self.height, self.width)
        structure, self.width, self.height, self.end = self.structInstance.generateMaze()
        self.structure = structure

