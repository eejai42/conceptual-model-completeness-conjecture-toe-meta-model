# Triangle and Polygon Demo

This repository demonstrates a simple SDK for working with polygons, with a focus on triangles and their properties. The code uses a straightforward object model with properties that compute dynamically based on the shape's edges and angles.

## Data Model Visualization

The following shows how data builds up as we progress through creating different polygons:

### Creating an Empty Polygon

```python
polygon = Polygon()
```

**Data State:**
```json
{
  "Edge": [],
  "Angle": [],
  "Polygon": [
    {
      "edges": [],
      "angles": [],
      "edge_count": 0,
      "angle_count": 0,
      "angle_degrees": [],
      "largest_angle": null,
      "sum_of_angles": 0,
      "is_triangle": false,
      "has_right_angle": false,
      "shape_type": "polygon"
    }
  ]
}
```

### Adding First Edge and Right Angle (90°)

```python
edge1 = Edge()
angle90 = Angle()
angle90.angle_degrees = 90  # Right angle
polygon.edges.add(edge1)
polygon.angles.add(angle90)
```

**Data State:**
```json
{
  "Edge": [
    {}
  ],
  "Angle": [
    {
      "angle_degrees": 90
    }
  ],
  "Polygon": [
    {
      "edges": [
        {}
      ],
      "angles": [
        {
          "angle_degrees": 90
        }
      ],
      "edge_count": 1,
      "angle_count": 1,
      "angle_degrees": [90],
      "largest_angle": 90,
      "sum_of_angles": 90,
      "is_triangle": false,
      "has_right_angle": true,
      "shape_type": "polygon"
    }
  ]
}
```

### Adding Second Edge and Angle

```python
edge2 = Edge()
angle53 = Angle()
angle53.angle_degrees = 53    
polygon.edges.add(edge2)
polygon.angles.add(angle53)
```

**Data State:**
```json
{
  "Edge": [
    {},
    {}
  ],
  "Angle": [
    {
      "angle_degrees": 90
    },
    {
      "angle_degrees": 53
    }
  ],
  "Polygon": [
    {
      "edges": [
        {},
        {}
      ],
      "angles": [
        {
          "angle_degrees": 90
        },
        {
          "angle_degrees": 53
        }
      ],
      "edge_count": 2,
      "angle_count": 2,
      "angle_degrees": [90, 53],
      "largest_angle": 90,
      "sum_of_angles": 143,
      "is_triangle": false,
      "has_right_angle": true,
      "shape_type": "polygon"
    }
  ]
}
```

### Creating a Triangle - Adding Third Edge and Angle

```python
edge3 = Edge()
angle37 = Angle()
angle37.angle_degrees = 37
polygon.edges.add(edge3)
polygon.angles.add(angle37)
```

**Data State:**
```json
{
  "Edge": [
    {},
    {},
    {}
  ],
  "Angle": [
    {
      "angle_degrees": 90
    },
    {
      "angle_degrees": 53
    },
    {
      "angle_degrees": 37
    }
  ],
  "Polygon": [
    {
      "edges": [
        {},
        {},
        {}
      ],
      "angles": [
        {
          "angle_degrees": 90
        },
        {
          "angle_degrees": 53
        },
        {
          "angle_degrees": 37
        }
      ],
      "edge_count": 3,
      "angle_count": 3,
      "angle_degrees": [90, 53, 37],
      "largest_angle": 90,
      "sum_of_angles": 180,
      "is_triangle": true,
      "has_right_angle": true,
      "shape_type": "triangle"
    }
  ]
}
```

### Changing the Right Angle to 91° (No Longer Right)

```python
# Modify the existing angle
angle90.angle_degrees = 91
```

**Data State:**
```json
{
  "Edge": [
    {},
    {},
    {}
  ],
  "Angle": [
    {
      "angle_degrees": 91
    },
    {
      "angle_degrees": 53
    },
    {
      "angle_degrees": 37
    }
  ],
  "Polygon": [
    {
      "edges": [
        {},
        {},
        {}
      ],
      "angles": [
        {
          "angle_degrees": 91
        },
        {
          "angle_degrees": 53
        },
        {
          "angle_degrees": 37
        }
      ],
      "edge_count": 3,
      "angle_count": 3,
      "angle_degrees": [91, 53, 37],
      "largest_angle": 91,
      "sum_of_angles": 181,
      "is_triangle": true,
      "has_right_angle": false,
      "shape_type": "triangle"
    }
  ]
}
```

### Making a Square - Adding Fourth Edge and Angle

```python
edge4 = Edge()
angle90b = Angle()
angle90b.angle_degrees = 90
polygon.edges.add(edge4)
polygon.angles.add(angle90b)
```

**Data State:**
```json
{
  "Edge": [
    {},
    {},
    {},
    {}
  ],
  "Angle": [
    {
      "angle_degrees": 91
    },
    {
      "angle_degrees": 53
    },
    {
      "angle_degrees": 37
    },
    {
      "angle_degrees": 90
    }
  ],
  "Polygon": [
    {
      "edges": [
        {},
        {},
        {},
        {}
      ],
      "angles": [
        {
          "angle_degrees": 91
        },
        {
          "angle_degrees": 53
        },
        {
          "angle_degrees": 37
        },
        {
          "angle_degrees": 90
        }
      ],
      "edge_count": 4,
      "angle_count": 4,
      "angle_degrees": [91, 53, 37, 90],
      "largest_angle": 91,
      "sum_of_angles": 271,
      "is_triangle": false,
      "has_right_angle": true,
      "shape_type": "quadrilateral"
    }
  ]
}
```

## Key Features Demonstrated

1. **Dynamic Property Calculation:**
   - Edge and angle counts update automatically
   - Shape type changes based on edge count
   - Right angle detection
   - Sum of angles calculation

2. **Triangle Properties:**
   - A polygon is classified as a triangle when it has exactly 3 edges
   - Right triangle detection when any angle equals 90 degrees
   - Sum of angles should be 180 degrees (or close to it with rounding)

3. **Quadrilateral Properties:**
   - Identified when a polygon has 4 edges
   - Sum of angles should be 360 degrees for a proper quadrilateral