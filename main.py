from node import Node
from gridpathfinder import GridPathFinder
from mazepathfinder import MazePathFinder
from structuregenerator import StructureGenerator


gridPF = GridPathFinder((0,0), (9,9), 10, 10)
gridPF.aStar()
gridPF.displayStructure()
gridPF.displayPathOnStructure()