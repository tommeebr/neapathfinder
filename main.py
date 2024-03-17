from node import Node
from pathfinder import PathFinder, GridPathFinder, MazePathFinder

# pF = PathFinder() 

# grid = [
#     [0, 0, 0, 0, 1, 0, 0, 0, 0],
#     [1, 1, 0, 1, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 1, 0, 0, 0],
#     [0, 1, 1, 1, 1, 1, 1, 0, 1],
#     [0, 0, 0, 0, 0, 1 ,1 ,0 ,0]
# ]
# start = (0, 0)
# end = (4, 8)
# path = pF.aStarGrid(start, end, grid)
# print(path)  # Output: [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
# pF.displayPathOnGrid(grid,path)

# maze = [
#     [3,2,3,2,1,2,2,2,3,2],
#     [1,1,0,2,1,2,2,1,1,1],
#     [1,2,1,1,2,2,2,0,2,0],
#     [3,1,1,2,2,3,2,2,3,0],
#     [1,0,3,2,1,0,3,0,3,2],
#     [3,0,1,1,2,2,1,2,1,1],
#     [1,3,1,3,0,1,2,1,1,2],
#     [1,0,1,3,2,1,1,0,3,0],
#     [3,0,1,1,1,2,2,2,0,1],
#     [1,2,1,0,1,3,2,2,2,0]
# ]

# start = (0,4)
# end = (9,5)
# path = PathFinder.aStarMaze(start, end, maze)
# print(path)
# pF.displayPathOnGrid(maze,path)

gridPF = MazePathFinder('assets/mazes/maze1.txt')
path = gridPF.aStar(gridPF.start, gridPF.end, gridPF.structure)
gridPF.displayPathOnGrid(gridPF.structure, path)