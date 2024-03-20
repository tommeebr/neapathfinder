import numpy as np

class StructureGenerator:
    def __init__(self, start, end, width,height):
        self.start = start
        self.end = end
        self.width = width
        self.height = height
        self.array = np.ones((height, width), dtype=np.int8)
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, left, down, up

    def generateGrid(self):
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
    
    def generateMaze(self):
        raise NotImplementedError("This method has not yet been implemented")
    
    def _dfs(self, x, y):
        #! Cannot use even numbers for width and height for some reason
        self.array[y][x] = 0
        np.random.shuffle(self.directions)
        for dx, dy in self.directions:
            nextX, nextY = x + 2*dx, y + 2*dy
            if (0 <= nextX < self.width) and (0 <= nextY < self.height) and self.array[nextY][nextX] == 1:
                self.array[nextY-dy][nextX-dx] = 0
                self._dfs(nextX, nextY)