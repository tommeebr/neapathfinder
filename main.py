from node import Node
from gridpathfinder import GridPathFinder
from mazepathfinder import MazePathFinder
from structuregenerator import StructureGenerator


gridPF = GridPathFinder((0,0), (20,20), 21, 21)
gridPF.aStar()
gridPF.displayStructure()
gridPF.displayPathOnStructure()