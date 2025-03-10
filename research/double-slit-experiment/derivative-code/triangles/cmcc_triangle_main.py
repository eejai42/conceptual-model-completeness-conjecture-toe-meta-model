from cmcc_triangle_helpers import Vertex, Edge, Polygon

def main():
    """
    Demonstrates emergent properties of a polygon using Vertex and Edge objects.
    A triangle is defined by 3 edges, and this property
    is inferred from the edge_count in the Polygon.
    """

    # 1) Define three Vertex objects
    p1 = Vertex(x=0, y=0)
    p2 = Vertex(x=4, y=0)
    p3 = Vertex(x=4, y=3)

    # 2) Create Edge objects referencing those Vertex objects
    e1 = Edge(start_vertex=p1, end_vertex=p2)
    e2 = Edge(start_vertex=p2, end_vertex=p3)
    e3 = Edge(start_vertex=p3, end_vertex=p1)

    # 3) Create a Polygon with these edges
    polygon = Polygon(
        vertices=[p1, p2, p3],     # or possibly just IDs
        edges=[e1, e2, e3]
    )

    # (Optional) If your JSON or aggregator references 'belongs_to_polygon' on each edge:
    # you could set it here so 'hypotenuse' works (Edge checks polygon.max_edge_length).
    for e in polygon.edges:
        e.belongs_to_polygon = polygon

    # 4) Print emergent properties
    print(f"Edge lengths: {[edge.length for edge in polygon.edges]}")
    print(f"Edge count: {polygon.edge_count}")
    print(f"Perimeter: {polygon.perimeter}")

    # 5) Check shape type
    print(f"Shape type: {polygon.shape_type}")
    if polygon.edge_count == 3:
        print("This polygon is a TRIANGLE.")
    else:
        print("This polygon is NOT a triangle.")

if __name__ == "__main__":
    main()