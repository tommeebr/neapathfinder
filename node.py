import heapq
import math

class Node:
    def __init__(self, parent=None, pos=None):
        self.parent = parent # Parent node
        self.pos = pos # (x, y) coordinates
        self.g = 0 # Cost to start node
        self.h = 0 # Heuristic cost
        self.f = 0 # Total cost of the node

    def __eq__(self, other):
        return self.pos == other.pos

