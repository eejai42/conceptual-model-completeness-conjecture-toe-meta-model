#!/usr/bin/env python3

from triangleness_cmcc_sdk import *

def main():
    # 1) Create a new game
    polygon = Polygon()
    edge1 = Edge()
    angle90 = Angle()
    angle90.angle_degrees = 91
    polygon.edges.add(edge1)
    polygon.angles.add(angle90)
    print(polygon.shape_type)
    edge2 = Edge()
    angle53 = Angle()
    angle53.angle_degrees = 53    
    polygon.edges.add(edge2)
    polygon.angles.add(angle53)
    print(polygon.shape_type)
    edge3 = Edge()
    angle37 = Angle()
    angle37.angle_degrees = 37
    polygon.edges.add(edge3)
    polygon.angles.add(angle37)

    print(polygon.shape_type)
    print(polygon.is_triangle)
    print(polygon.has_right_angle)
    edge4 = Edge()
    polygon.edges.add(edge4)
    print(polygon.shape_type)
    print(polygon.is_triangle)

if __name__ == "__main__":
    main()
