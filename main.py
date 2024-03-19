from node import Node
from gridpathfinder import GridPathFinder
from mazepathfinder import MazePathFinder
from structuregenerator import StructureGenerator


gridPF = GridPathFinder((0,0), (70,70), 71, 71)
gridPF.aStar()
gridPF.displayStructure()
gridPF.displayPathOnStructure()