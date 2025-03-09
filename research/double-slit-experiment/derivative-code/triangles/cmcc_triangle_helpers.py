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
        self.start_x = kwargs.get('start_x')
        self.start_y = kwargs.get('start_y')
        self.end_x = kwargs.get('end_x')
        self.end_y = kwargs.get('end_y')
        self.belongs_to_polygon = kwargs.get('belongs_to_polygon')

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
        Original formula: SUM(edges)
        """
        return np.sum(self.edges)

    @property
    def max_edge_length(self):
        """
        Original formula: MAX(edges)
        """
        # Parser error for formula: MAX(edges)
        return None

    @property
    def area(self):
        """
        Original formula: SHOELACE(vertices)
        """
        # Parser error for formula: SHOELACE(vertices)
        return None

    @property
    def shape_type(self):
        """
        Original formula: IF( EQUAL(edge_count, 3), 'Triangle', IF( EQUAL(edge_count, 4), 'Quadrilateral', 'Polygon') )
        """
        # Parser error for formula: IF( EQUAL(edge_count, 3), 'Triangle', IF( EQUAL(edge_count, 4), 'Quadrilateral', 'Polygon') )
        return None
