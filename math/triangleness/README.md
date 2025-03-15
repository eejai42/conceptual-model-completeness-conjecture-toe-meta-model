# 
## 

Demonstration of a polygon model that checks for 3-edge polygons, right angles, etc. using only a tiny set of aggregator formulas.

**Date**: 
**Domain Identifier**: CMCC_ToEMM_TriangleMinimal

### Authors

### Abstract


![ Entity Diagram](triangle_demo.png)


### Key Points

### Implications

### Narrative

---

# Schema Overview

## Entity: Edge

**Description**: A simple edge record. (No advanced geometry; just a placeholder.)

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **label**  
  *Type:* scalar, *Datatype:* string  
  
- **polygon_id**  
  *Type:* lookup, *Datatype:*   
  





---

## Entity: Angle

**Description**: Represents a single angle (in degrees) belonging to a polygon.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **angle_degrees**  
  *Type:* scalar, *Datatype:* float  
  
- **polygon_id**  
  *Type:* lookup, *Datatype:*   
  





---

## Entity: Polygon

**Description**: A polygon with edges and angles. We’ll check if it’s a triangle, if it has a right angle, etc.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **label**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **edges**  
  *Target Entity:* Edge, *Type:* one_to_many  
    
  (Join condition: **Edge.polygon_id = this.id**)  
  *Description:* All edges that form this polygon.
- **angles**  
  *Target Entity:* Angle, *Type:* one_to_many  
    
  (Join condition: **Angle.polygon_id = this.id**)  
  *Description:* All angles belonging to this polygon.
- **angle_degrees**  
  *Target Entity:* this, *Type:* one_to_many  
    
  (Join condition: **this.angles.angle_degrees**)  
  *Description:* An array of the angles of a triangle.

### Aggregations
- **edge_count**  
  *Description:* Number of edges in this polygon.  
  *Formula:* `COUNT(this.edges)`
- **angle_count**  
  *Description:* Number of angles in this polygon.  
  *Formula:* `COUNT(this.angles)`
- **largest_angle**  
  *Description:* The maximum angle measure among angles.  
  *Formula:* `MAX(this.angle_degrees)`
- **sum_of_angles**  
  *Description:* Sum of all angle measures in degrees.  
  *Formula:* `SUM(this.angle_degrees)`
- **is_triangle**  
  *Description:* True if the polygon has exactly 3 edges.  
  *Formula:* `EQUAL(this.edge_count, 3)`
- **has_right_angle**  
  *Description:* True if any angle == 90.  
  *Formula:* `CONTAINS(this.angle_degrees, 90)`
- **shape_type**  
  *Description:* Naive categorization based on edge_count: 3 => triangle, 4 => quadrilateral, else other.  
  *Formula:* `IF( EQUAL(this.edge_count,3), 'triangle', IF(EQUAL(this.edge_count,4),'square','polygon') )`



---