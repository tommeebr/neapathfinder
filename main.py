from node import Node
from gridpathfinder import GridPathFinder
from mazepathfinder import MazePathFinder
from structuregenerator import StructureGenerator


gridPF = MazePathFinder('assets/mazes/maze1.txt')
gridPF.aStar()
gridPF.displayStructure()
gridPF.displayPathOnStructure()