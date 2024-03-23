from node import Node
from pathfindergrid import PathFinderGrid
from pathfindermaze import PathFinderMaze
from generatorstructure import GeneratorStructure


def main():
    gridPF = PathFinderMaze((0,0),(9,9),11,11)
    gridPF.solvableStructure()
    gridPF.displayStructure()
    gridPF.displayPathOnStructure()

if __name__ == '__main__':
    main()