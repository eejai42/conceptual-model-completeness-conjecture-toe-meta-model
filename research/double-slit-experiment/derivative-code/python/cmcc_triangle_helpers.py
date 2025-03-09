"""
Auto-generated Python code from your quantum-walk rulebook.
It includes building-block definitions (SHIFT, BARRIER, EVOLVE, etc.)
and the classes with calculated fields referencing them.
"""
import math
import numpy as np

# ----- Building Block Lambdas (auto-injected) -----

# ----- Generated classes below -----

class Edge:
    def __init__(self, **kwargs):
        self.start_x = kwargs.get('start_x')
        self.start_y = kwargs.get('start_y')
        self.end_x = kwargs.get('end_x')
        self.end_y = kwargs.get('end_y')

    @property
    def length(self):
        """
        Original formula: SQRT( ADD( SUBTRACT(end_x, start_x)^2, SUBTRACT(end_y, start_y)^2 ) )
        """
        return math.sqrt((self.SUBTRACT(end_x, start_x)^2 + self.SUBTRACT(end_y, start_y)^2))

class Polygon:
    def __init__(self, **kwargs):
        self.edges = kwargs.get('edges')

    @property
    def edge_count(self):
        """
        Original formula: LEN(edges)
        """
        return len(self.edges)

    @property
    def perimeter(self):
        """
        Original formula: SUM(edges)
        """
        return np.sum(self.edges)
