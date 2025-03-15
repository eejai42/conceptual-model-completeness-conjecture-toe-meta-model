"""
Auto-generated Python code from your domain model.
Now with aggregator rewriting that references core_lambda_functions.
"""
import math
import numpy as np
from core_lambda_functions import COUNT, SUM, MAX, IF, CONTAINS, EQUAL

import uuid
import re

class CollectionWrapper:
    """A tiny helper so we can do something like: obj.someLookup.add(item)."""
    def __init__(self, parent_object, attr_name):
        self.parent_object = parent_object
        self.attr_name = attr_name
        if not hasattr(parent_object, '_collections'):
            parent_object._collections = {}
        if attr_name not in parent_object._collections:
            parent_object._collections[attr_name] = []

    def add(self, item):
        self.parent_object._collections[self.attr_name].append(item)

    def __iter__(self):
        return iter(self.parent_object._collections[self.attr_name])

    def __len__(self):
        return len(self.parent_object._collections[self.attr_name])

    def __getitem__(self, index):
        return self.parent_object._collections[self.attr_name][index]

# Below are aggregator stubs we haven't yet implemented in core_lambda_functions:
# e.g. 'AVG', 'EXISTS', 'MINBY', 'MODE', 'TOPN', 'MAXBY'
def AVG(collection):
    """Placeholder aggregator: real logic not yet implemented."""
    # Could do: return sum(collection)/len(collection) if numeric
    return f"/* AVG not implemented: {collection} */"

def EXISTS(condition_expr):
    return f"/* EXISTS not implemented: {condition_expr} */"

def MINBY(expr):
    return f"/* MINBY not implemented: {expr} */"

def MAXBY(expr):
    return f"/* MAXBY not implemented: {expr} */"

def MODE(expr):
    return f"/* MODE not implemented: {expr} */"

def TOPN(expr):
    return f"/* TOPN not implemented: {expr} */"


# ----- Generated classes below -----

class Edge:
    """Plain data container for Edge entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.label = kwargs.get('label')
        self.polygon_id = kwargs.get('polygon_id')

        # If any 'one_to_many' or 'many_to_many' lookups exist, store them as collection wrappers.

class Angle:
    """Plain data container for Angle entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.angle_degrees = kwargs.get('angle_degrees')
        self.polygon_id = kwargs.get('polygon_id')

        # If any 'one_to_many' or 'many_to_many' lookups exist, store them as collection wrappers.

class Polygon:
    """Plain data container for Polygon entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.label = kwargs.get('label')

        # If any 'one_to_many' or 'many_to_many' lookups exist, store them as collection wrappers.
        self.edges = CollectionWrapper(self, 'edges')
        self.angles = CollectionWrapper(self, 'angles')

    @property
    def edge_count(self):
        """Number of edges in this polygon.
        Original formula: COUNT(edges)
        """
        return COUNT(self.edges)

    @property
    def angle_count(self):
        """Number of angles in this polygon.
        Original formula: COUNT(angles)
        """
        return COUNT(angles)

    @property
    def largest_angle(self):
        """The maximum angle measure among angles.
        Original formula: MAX(angles.angle_degrees)
        """
        return MAX(angles.angle_degrees)

    @property
    def sum_of_angles(self):
        """Sum of all angle measures in degrees.
        Original formula: SUM(angles.angle_degrees)
        """
        return SUM(angles.angle_degrees)

    @property
    def is_triangle(self):
        """True if the polygon has exactly 3 edges.
        Original formula: EQUAL(edge_count, 3)
        """
        return EQUAL(edge_count, 3)

    @property
    def has_right_angle(self):
        """True if any angle == 90.
        Original formula: CONTAINS(angles.angle_degrees, 90)
        """
        return CONTAINS(angles.angle_degrees, 90)

    @property
    def shape_type(self):
        """Naive categorization based on edge_count: 3 => triangle, 4 => quadrilateral, else other.
        Original formula: IF( EQUAL(edge_count,3), 'Triangle', IF(EQUAL(edge_count,4),'Quadrilateral','Other') )
        """
        return IF( EQUAL(self.edge_count,3), 'Triangle', IF(EQUAL(self.edge_count,4),'Quadrilateral','Other') )
