import raimad as rai
import numpy as np

from shapely import Polygon

from shapely import unary_union
from shapely import symmetric_difference_all


### Boolean operations
# * Union (OR)
# * Difference (XOR)
# * Intersection (AND, pairwise)
# * Intersection_global) (AND, global)

def remove_duplicate_points(coords, tol=1e-12):
    """
    Remove consecutive duplicate points from a list of (x, y) coordinates.
    Keeps the ring closed if it originally was.
    """
    cleaned = [coords[0]]
    for pt in coords[1:]:
        if np.linalg.norm(np.array(pt) - np.array(cleaned[-1])) > tol:
            cleaned.append(pt)

    # Re-close the ring if necessary
    if cleaned[0] != cleaned[-1]:
        cleaned.append(cleaned[0])
    return cleaned


def union(input_polygons):
    """
    Union between different polygons. Can handle multiple groups of objects.
    Removes duplicate points.
    """
    # Convert each set of coordinates to a Shapely Polygon
    shapely_polygons = [Polygon(coords) for coords in input_polygons]
    
    # Compute the union of all polygons
    union = unary_union(shapely_polygons)
    
    # Format the result as a list of lists of (x, y) tuples
    if union.geom_type == 'Polygon':
        new_polygon = [remove_duplicate_points(list(union.exterior.coords))]
    elif union.geom_type == 'MultiPolygon':
        new_polygon = [
            remove_duplicate_points(list(poly.exterior.coords))
            for poly in union.geoms
        ]
    else:
        new_polygon = []

    return new_polygon

def difference(input_polygons):
    """
    Difference between different polygons. Can handle multiple groups of objects
    """
    # Convert each set of coordinates to Shapely Polygons
    shapely_polygons = [Polygon(coords) for coords in input_polygons]
    
    # Initialize list to hold non-overlapping pieces
    non_overlapping = []
    
    for i, poly in enumerate(shapely_polygons):
        others = shapely_polygons[:i] + shapely_polygons[i+1:]
        diff = poly.difference(unary_union(others))
        
        if diff.is_empty:
            continue
        elif diff.geom_type == 'Polygon':
            non_overlapping.append(list(diff.exterior.coords))
        elif diff.geom_type == 'MultiPolygon':
            non_overlapping.extend([list(p.exterior.coords) for p in diff.geoms])
    
    new_polygons = non_overlapping
    return new_polygons

def intersection(input_polygons):
    """
    Intersection (pairwise) between polygons.
    """
    shapely_polygons = [Polygon(coords) for coords in input_polygons]
    
    intersections = []
    
    for i in range(len(shapely_polygons)):
        for j in range(i + 1, len(shapely_polygons)):
            inter = shapely_polygons[i].intersection(shapely_polygons[j])
            if inter.is_empty:
                continue
            elif inter.geom_type == 'Polygon':
                intersections.append(list(inter.exterior.coords))
            elif inter.geom_type == 'MultiPolygon':
                intersections.extend([list(p.exterior.coords) for p in inter.geoms])
    
    new_poly = intersections
    return intersections


def intersection_global(input_polygons):
    """
    Intersection between all polygons. (global)
    """
    shapely_polygons = [Polygon(coords) for coords in input_polygons]
    
    # Start with the first polygon
    intersection = shapely_polygons[0]
    
    # Iteratively intersect with the others
    for poly in shapely_polygons[1:]:
        intersection = intersection.intersection(poly)
    
    # Format the result
    if intersection.is_empty:
        new_poly = []
    elif intersection.geom_type == 'Polygon':
        new_poly = [list(intersection.exterior.coords)]
    elif intersection.geom_type == 'MultiPolygon':
        new_poly = [list(p.exterior.coords) for p in intersection.geoms]
    else:
        raise ValueError(f"Unexpected geometry type: {intersection.geom_type}")

    return new_poly


#### Invert Layer section

def close_ring(coords):
    return coords if coords[0] == coords[-1] else coords + [coords[0]]

def closest_point_index(coords, target):
    coords_arr = np.array(coords)
    target_arr = np.array(target)
    dists = np.linalg.norm(coords_arr - target_arr, axis=1)
    return int(np.argmin(dists))

def find_left_bridge_point(inner_coords, outer_coords, tolerance=1e-5):
    # Find leftmost point of inner polygon
    inner_arr = np.array(inner_coords)
    left_idx = np.argmin(inner_arr[:, 0])
    p_inner = tuple(inner_arr[left_idx])

    # Find the closest outer point that is to the left of the inner point (same-ish y)
    candidates = [
        pt for pt in outer_coords 
        if pt[0] < p_inner[0] and abs(pt[1] - p_inner[1]) < tolerance
    ]

    if not candidates:
        # fallback: closest outer point (not filtered by y-alignment)
        i_outer = closest_point_index(outer_coords, p_inner)
        p_outer = outer_coords[i_outer]
    else:
        p_outer = min(candidates, key=lambda pt: np.linalg.norm(np.array(pt) - np.array(p_inner)))

    return p_outer, p_inner

def connect_outer_and_inner(outer_coords, inner_coords, rev_inner = True):
    """
    Outer shape should fully enclose the inner shape(s)
    The inner shape should not contain any other hole
    """


    outer_coords = close_ring(outer_coords)
    inner_coords = close_ring(inner_coords)

    p1, p2 = find_left_bridge_point(inner_coords, outer_coords)

    i1 = closest_point_index(outer_coords, p1)
    i2 = closest_point_index(inner_coords, p2)

    # Walk around outer polygon from p1
    outer_path = outer_coords[i1:] + outer_coords[1:i1+1]

    # Walk around inner polygon from p2 in reverse
    inner_path = inner_coords[i2:] + inner_coords[1:i2+1]
    if rev_inner == True:
        inner_path.reverse()

    # Build final shape
    path = outer_path + [inner_path[0]] + inner_path + [outer_path[0]]
    return path

class Invert_Layer(rai.Compo):
    """
    Inverts one layer of a compo enclosed within another compo
    """
    def _make(self,
              outer_compo: rai.Compo =  rai.RectLW(10,10).proxy(),
              inner_compos: rai.Compo = rai.Circle(3).proxy(),
              inner_layer: str = "root",
              outer_layer: str = "root",
             ):
        
        flat_outer_compo = outer_compo.steamroll()
        layer_outer_poly = union(flat_outer_compo[outer_layer])[0]

        flat_inner_compos = inner_compos.steamroll()
        layer_inner_poly = union(flat_inner_compos[inner_layer])

        outer_path = close_ring(layer_outer_poly)
        inner_path = close_ring(layer_inner_poly)

        path = outer_path
        for i, shape in enumerate(layer_inner_poly):
            path = connect_outer_and_inner(path, inner_path[i])
        
        self.subcompos.inverted_union = rai.CustomPoly(path).proxy().map(inner_layer)


