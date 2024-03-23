import numpy as np

class GeneratorStructure():
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