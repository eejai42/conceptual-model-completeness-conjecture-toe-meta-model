"""
Auto-generated Python code from your quantum-walk rulebook.
It includes building-block definitions (SHIFT, BARRIER, EVOLVE, etc.)
and the classes with calculated fields referencing them.
"""
import math
import numpy as np

# ----- Building Block Lambdas (auto-injected) -----

# ----- Generated classes below -----

class Vertex:
    def __init__(self, **kwargs):
        self.x = kwargs.get('x')
        self.y = kwargs.get('y')

class Edge:
    def __init__(self, **kwargs):
        self.start_vertex = kwargs.get('start_vertex')
        self.end_vertex = kwargs.get('end_vertex')
        self.belongs_to_polygon = kwargs.get('belongs_to_polygon')

    @property
    def start_x(self):
        """
        Original formula: start_vertex.x
        """
        return self.start_vertex.x

    @property
    def start_y(self):
        """
        Original formula: start_vertex.y
        """
        return self.start_vertex.y

    @property
    def end_x(self):
        """
        Original formula: end_vertex.x
        """
        return self.end_vertex.x

    @property
    def end_y(self):
        """
        Original formula: end_vertex.y
        """
        return self.end_vertex.y

    @property
    def length(self):
        """
        Original formula: SQRT( ADD( POWER( SUBTRACT(end_x, start_x), 2 ), POWER( SUBTRACT(end_y, start_y), 2 ) ) )
        """
        return math.sqrt((((self.end_x - self.start_x) ** 2) + ((self.end_y - self.start_y) ** 2)))

    @property
    def hypotenuse(self):
        """
        Original formula: EQUAL( length, belongs_to_polygon.max_edge_length )
        """
        return np.allclose(self.length, self.belongs_to_polygon.max_edge_length)

class Polygon:
    def __init__(self, **kwargs):
        self.vertices = kwargs.get('vertices')
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
        Original formula: SUM_OVER(edges, length)
        """
        return sum(getattr(item, 'length') for item in self.edges)

    @property
    def max_edge_length(self):
        """
        Original formula: MAX_OVER(edges, length)
        """
        return max(getattr(item, 'length') for item in self.edges)

    @property
    def shape_type(self):
        """
        Original formula: IF( EQUAL(edge_count, 3), 'Triangle', IF( EQUAL(edge_count, 4), 'Quadrilateral', 'Polygon'))
        """
        return ('Triangle' if np.allclose(self.edge_count, 3) else ('Quadrilateral' if np.allclose(self.edge_count, 4) else 'Polygon'))
