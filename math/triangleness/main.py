#!/usr/bin/env python3

import triangleness_cmcc_sdk

def main():
    # 1) Create a new game
    polygon = triangleness_cmcc_sdk.Polygon()
    edge1 = triangleness_cmcc_sdk.Edge()
    polygon.edges.add(edge1)
    print(polygon.shape_type)
    edge2 = triangleness_cmcc_sdk.Edge()
    polygon.edges.add(edge2)
    print(polygon.shape_type)
    edge3 = triangleness_cmcc_sdk.Edge()
    polygon.edges.add(edge3)
    print(polygon.shape_type)
    edge4 = triangleness_cmcc_sdk.Edge()
    polygon.edges.add(edge4)
    print(polygon.shape_type)

if __name__ == "__main__":
    main()
