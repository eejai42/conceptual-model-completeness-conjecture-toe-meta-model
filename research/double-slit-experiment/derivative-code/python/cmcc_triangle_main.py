from cmcc_triangle_helpers import *
def main():
    """
    Demonstrates emergent properties of a polygon.
    A triangle is defined by 3 edges, and this property
    is inferred from the edge count.
    """

    # Define three points
    p1 = {"x": 0, "y": 0}
    p2 = {"x": 4, "y": 0}
    p3 = {"x": 4, "y": 3}

    # Create edges using the generated Edge class
    e1 = Edge(start_x=p1["x"], start_y=p1["y"], end_x=p2["x"], end_y=p2["y"])
    e2 = Edge(start_x=p2["x"], start_y=p2["y"], end_x=p3["x"], end_y=p3["y"])
    e3 = Edge(start_x=p3["x"], start_y=p3["y"], end_x=p1["x"], end_y=p1["y"])

    # Store edges in a list
    edges = [e1, e2, e3]

    # Create a polygon
    polygon = Polygon(edges=[e.length for e in edges])

    # Compute emergent properties
    print(f"Edge lengths: {[e.length for e in edges]}")
    print(f"Edge count: {polygon.edge_count}")
    print(f"Perimeter: {polygon.perimeter}")

    # Check if it is a triangle
    if polygon.edge_count == 3:
        print("This polygon is a TRIANGLE.")
    else:
        print("This polygon is NOT a triangle.")

if __name__ == "__main__":
    main()
