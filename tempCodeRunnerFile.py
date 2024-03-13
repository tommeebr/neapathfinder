from node import Node
from pathfinder import PathFinder

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
path = pF.aStar(start, end, grid)
print(path)  # Output: [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]