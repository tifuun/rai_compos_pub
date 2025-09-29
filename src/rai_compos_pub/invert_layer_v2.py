import raimad as rai
import numpy as np
import shapely

from shapely import MultiPolygon, Polygon

from shapely import unary_union
from shapely import symmetric_difference_all

def close_ring(coords):
    return coords if coords[0] == coords[-1] else coords + [coords[0]]

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

### Shape list manipulation
def open_ring(coords):
    if type(coords[0]) == tuple:
        return coords if coords[0] != coords[-1] else coords[:-1]
    else:
        for i, coord in enumerate(coords):
            if coord[0] !=coord[-1]:
                return coord
            else:
                return coord[:-1]
            
            return coords 

### Inner loop section
def find_south_point(coords):
    """
    Finds the southernmost point (tuple with the most negative second value).
    Returns the index and the tuple itself.
    """
    coords = open_ring(coords)
    # Look at the second value of each tuple (index 1)
    inner_start_index, inner_start_point = min(
        enumerate(coords), key=lambda coord: coord[1][1]
    )
    return inner_start_index, inner_start_point

def reshape_inner_path(inner_coords,index_inner_path, reverse = False):
    inner_loop = inner_coords[index_inner_path:] + inner_coords[:index_inner_path]
    
    if reverse == True:
        inner_loop = inner_loop[::-1]
    
    return close_ring(inner_loop)

### Outer loop section
def find_bridge_index_outer(outer_coords,start_point_inner):
    outer_coords_closed = close_ring(outer_coords) ## Closed loop in case the lowest point is also next to the first/last point.
    
    allowed_x_indices = []
    for i in range(len(outer_coords_closed) - 1):
        # "Is the target horizontal value in between the two following points"
        if outer_coords_closed[i][0] <= start_point_inner[0] <= outer_coords_closed[i + 1][0] or outer_coords_closed[i+1][0] <= start_point_inner[0] <= outer_coords_closed[i][0]:
            allowed_x_indices.append(i)
   
    lower_point_indices = []
    for i, index in enumerate(allowed_x_indices):
        # "Remove coordinates with higher vertical value that the start point"
        if outer_coords_closed[index][1] < start_point_inner[1]:
            lower_point_indices.append(index)
    
    if lower_point_indices == []:
        return "ERROR, inner shape does not fit in outer shape"
        
    difference = start_point_inner[1] - outer_coords_closed[lower_point_indices[0]][1]
    winner_index = lower_point_indices[0]
    
    for i, index in enumerate(lower_point_indices):
        #  Find the point with the highest Y value, Output the coordinate of the highest remaining point
        if start_point_inner[1] - outer_coords_closed[index][1] < difference:
            difference =  start_point_inner[1] - outer_coords_closed[index][1]
            winner_index = index
    
    return winner_index

def find_outer_bridge_point(outer_coords, break_index, inner_start_point):
    dr_outer = (outer_coords[break_index+1][0] - outer_coords[break_index][0], outer_coords[break_index+1][1] - outer_coords[break_index][1])
    dr_inner = (inner_start_point[0]              - outer_coords[break_index][0], inner_start_point[0]              - outer_coords[break_index+1][1])

    outer_bridge_point = (inner_start_point[0],(dr_inner[0]/dr_outer[0])*dr_outer[1]+outer_coords[break_index][1])
    return outer_bridge_point

### Bridge building
def build_bridge(outer_path,inner_loop,break_index,outer_bridge_point):
    full_loop = open_ring(outer_path)
    
    full_loop[break_index+1:break_index+1] = [outer_bridge_point] + close_ring(inner_loop) + [outer_bridge_point]## Merge and add point
    return full_loop


########## Invert Layer function ############

class Invert_layer_v2(rai.Compo):
    """
    note the reverse option reverses the order of the inner path, in case there are multiple objects in the inner compo all elements are treated the same.
    """
    def _make(self, 
              outer_compo, 
              inner_compos,
              outer_layer = "root",
              inner_layer= "root",
              reverse = False,
             ):
        ## Flattening polygons to single coordinate list or list of coordinate lists
        flat_outer_compo = outer_compo.steamroll()
        layer_outer_poly = union(flat_outer_compo[outer_layer])[0]
    
        flat_inner_compos = inner_compos.steamroll()
        layer_inner_polies = flat_inner_compos[inner_layer]
        
        outer_path = layer_outer_poly
        inner_path = layer_inner_polies

        path = outer_path

        for i, shape in enumerate(layer_inner_polies):
            inner_start_index, inner_start_point = find_south_point(inner_path[i])
            
            inner_loop = reshape_inner_path(shape, inner_start_index,reverse = reverse)

            
            index_split =  find_bridge_index_outer(path, inner_start_point)
            bridge_point = find_outer_bridge_point(path, index_split, inner_start_point)

            path = build_bridge(path, inner_loop,index_split,bridge_point)


        self.subcompos.loop = rai.CustomPoly(path).proxy()
