import raimad as rai
import math
from rai_compos_pub import RAIText


class Wafer_flat_aligner(rai.Compo):
    """
    Alignment tool, used for aligning a mask with the flat of a wafer
    """
    class Options:
        flat_length = rai.Option.Geometric("total lenght of the wafer flat alligner", browser_default = 150)
        number_of_knots = rai.Option.Geometric("number of knots (wide rectangular linepiece) along the aligner", browser_default = 4) 
    
    def _make(self,
              flat_length:float = 1500,
              number_of_knots: int = 4 
             ):
        ## Shapes
        axis = rai.RectLW(flat_length+1.3,flat_length/1500*4).proxy()
        knot = rai.RectLW(flat_length/15*2,flat_length/150*4).proxy() 

        ## Subcompos
        self.subcompos.axis = axis
        axis_width = axis.bbox.length

        num = number_of_knots + 1
        for i in range(num-1):
            self.subcompos[f'knot{i}'] = (knot.proxy()
                                          .bbox.mid.to(self.subcompos.axis.bbox.mid_left)
                                          .movex((i+1)/num*axis_width)
                                         )
        ## Marks
        self.marks.center = self.subcompos.axis.bbox.mid
        
class Wafer_ruler_aligner(rai.Compo):
    """
    Alignment tool, used for aligning a mask with the contour of a wafer using a ruler-shaped object
    """
    class Options:
        knot_spacing= rai.Option.Geometric("spacing between the hearts of each knot (line widening)", browser_default =  10)
        back_length= rai.Option.Geometric("total lenght of the base of the ruler", browser_default =  70)
        back_height= rai.Option.Geometric("widht of the base of the ruler", browser_default =  6),
    
    def _make(self,
              knot_spacing:float = 50,
              back_length:float = 350,
              back_height:float = 30,
             ):
        
        back = rai.RectLW(back_length,back_height).proxy()
        knot = rai.RectLW(back_length/350*4,back_height/3).proxy()

        num = math.floor(back.bbox.length/knot_spacing)

        if num%2 == 0:
            num += 1

        ## Subcompos
        self.subcompos.back = back
        for i in range(num):
            label = i - (num-1)/2
            
            self.subcompos[f'knot{i}'] = (knot.proxy()
                                          .bbox.bot_mid.to(self.subcompos.back.bbox.top_mid)
                                          .movex(label*knot_spacing)
                                         )
            self.subcompos[f"label{i}"] = (RAIText(f'{label:.0f}')
                                           .proxy()
                                           .scale(knot_spacing/50*0.2)
                                           .snap_above(self.subcompos[f'knot{i}']).movey(5)
                                          )

            self.marks.center = self.subcompos.back.bbox.top_mid
            self.marks.back_center = self.subcompos.back.bbox.mid
