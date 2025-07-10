"""
These layer functions can be used to manipulate a Raimad compo layer by specifying the compo and the layer

Layer_union:        creates a single layer rai.Compo in which all overlapping elements are fused
Layer_intersection: creates a single layer rai.Compo of the intersection between compo layers A and B  (A AND B)
Layer_merge:        creates a single layer rai.Compo of the union between compo layers A and B         (A OR  B)
Layer_difference:   creates a single layer rai.Compo of the difference between compo layers A and B    (A NOT B)

"""

import raimad as rai
import shapely

from shapely import MultiPolygon, Polygon
from shapely import unary_union
 
def compo_2_poly(compo: rai.Compo,
                 layer: str = "root",
                ):
    """
    Transforms a rai.Compo into a shapely.Polygon or shapely.MultiPolygon
    compo: rai.Compo
    layer: str
    """
    flat_compo_layer = compo.steamroll()[layer]
    if len(flat_compo_layer) == 1:
        output_poly = Polygon(flat_compo_layer[0])
    else:
        multipolylist = []
        for i, geom in enumerate(flat_compo_layer):
           multipolylist.append(Polygon(geom))

        output_poly = MultiPolygon(multipolylist)
    
    return output_poly


class Layer_union(rai.Compo):
    """
    Merges all elements in a rai.Compo layer into a new compo (fuses overlapping elements together)
    compo: rai.Compo
    layer: str
    """
    def _make(self,
              compo: rai.Compo = rai.Circle(3),
              layer: str = "root",
             ):
        
        poly= compo_2_poly(compo,layer)
    
        union_poly = shapely.unary_union([poly])

        if type(union_poly) == shapely.Polygon:
            self.subcompos.merge = rai.CustomPoly(list(union_poly.exterior.coords)).proxy()
        elif type(union_poly) == shapely.MultiPolygon:   
            for i,poly in enumerate(union_poly.geoms):
                self.subcompos[f"merge{i}"] = rai.CustomPoly(list(poly.exterior.coords)).proxy()

class Layer_intersection(rai.Compo):
    """
    Layer_Intersection: creates a single layer rai.Compo of the intersection between compo layers A and B  (A AND B)

    compo_1: rai.Compo
    compo_2: rai.Compo
    layer_1: str
    layer_2: str
    
    """
    def _make(self,
              compo_1: rai.Compo =  rai.RectLW(5,5).proxy(),
              compo_2: rai.Compo = rai.RectLW(5,5).proxy().move(3,2),
              layer_1: str = "root",
              layer_2: str = "root",
             ):

        compo_union_1 = Layer_union(compo_1)
        compo_union_2 = Layer_union(compo_2)
        
        poly_1 = compo_2_poly(compo_union_1,layer_1)
        poly_2 = compo_2_poly(compo_union_2,layer_2)
        
        output_poly = poly_1.intersection(poly_2)

        if type(output_poly) == shapely.Polygon:
            self.subcompos.merge = rai.CustomPoly(list(output_poly.exterior.coords)).proxy()
        elif type(output_poly) == shapely.MultiPolygon:
            for i,poly in enumerate(output_poly.geoms):
                self.subcompos[f"merge{i}"] = rai.CustomPoly(list(poly.exterior.coords)).proxy()


class Layer_merge(rai.Compo):
    """
    Layer_Merge:        creates a single layer rai.Compo of the union between compo layers A and B         (A OR  B)

    compo_1: rai.Compo
    compo_2: rai.Compo
    layer_1: str
    layer_2: str
    
    """
    def _make(self,
              compo_1: rai.Compo =  rai.RectLW(5,5).proxy(),
              compo_2: rai.Compo = rai.RectLW(5,5).proxy().move(3,2),
              layer_1: str = "root",
              layer_2: str = "root",
             ):
        
        poly_1 = compo_2_poly(compo_1,layer_1)
        poly_2 = compo_2_poly(compo_2,layer_2)
        
        output_poly = shapely.unary_union([poly_1,poly_2])

        if type(output_poly) == shapely.Polygon:
            self.subcompos.merge = rai.CustomPoly(list(output_poly.exterior.coords)).proxy()
        elif type(output_poly) == shapely.MultiPolygon:
            for i,poly in enumerate(output_poly.geoms):
                self.subcompos[f"merge{i}"] = rai.CustomPoly(list(poly.exterior.coords)).proxy()


class Layer_difference(rai.Compo):
    """
    Layer_Difference:   creates a single layer rai.Compo of the difference between compo layers A and B    (A NOT B)
    
    Creates a component reflecting the difference of layers A an B (A and not B)
    compo_1: rai.Compo
    compo_2: rai.Compo
    layer_1: str
    layer_2: str
    
    """
    def _make(self,
              compo_1: rai.Compo =  rai.RectLW(5,5).proxy(),
              compo_2: rai.Compo = rai.RectLW(5,5).proxy().move(3,2),
              layer_1: str = "root",
              layer_2: str = "root",
             ):
        compo_union_1 = Layer_union(compo_1)
        compo_union_2 = Layer_union(compo_2)
        
        poly_1 = compo_2_poly(compo_union_1,layer_1)
        poly_2 = compo_2_poly(compo_union_2,layer_2)

        
        output_poly = poly_1.difference(poly_2)
        output_poly_2 = poly_2.difference(poly_1)
        
        if type(output_poly) == shapely.Polygon:
            self.subcompos.merge = rai.CustomPoly(list(output_poly.exterior.coords)).proxy()
        elif type(output_poly) == shapely.MultiPolygon:
            for i,poly in enumerate(output_poly.geoms):
                self.subcompos[f"merge{i}"] = rai.CustomPoly(list(poly.exterior.coords)).proxy()





