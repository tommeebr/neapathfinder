import numpy as np

class StructureGenerator:
    def __init__(self, start, end, width,height):
        self.start = start
        self.end = end
        self.width = width
        self.height = height
        self.maze = np.ones((height, width), dtype=np.int8)
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, left, down, up

    def generateGrid(self):
        self._dfs(self.start[0], self.start[1])
        self.maze[self.start[1]][self.start[0]] = 0  # Ensure start is traversable
        self.maze[self.end[1]][self.end[0]] = 0  # Ensure end is traversable
        return self.maze.tolist()  # Convert back to list for compatibility with PathFinder

    def _dfs(self, x, y): # private method
        #! Cannot use even numbers for width and height for some reason
        self.maze[y][x] = 0
        np.random.shuffle(self.directions)
        for dx, dy in self.directions:
            nextX, nextY = x + 2*dx, y + 2*dy
            if (0 <= nextX < self.width) and (0 <= nextY < self.height) and self.maze[nextY][nextX] == 1:
                self.maze[nextY-dy][nextX-dx] = 0
                self._dfs(nextX, nextY)