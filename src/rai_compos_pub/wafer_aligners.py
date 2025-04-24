import raimad as rai
import math
from rai_compos_pub import RAIText


class Wafer_flat_aligner(rai.Compo):
    """
    Alignment tool, used for aligning a mask with the flat of a wafer
    """
    def _make(self,
              flat_length:float = 1500,
              number_of_knots: int = 4 
             ):
        ## Shapes
        axis = rai.RectLW(flat_length+1.3,4).proxy()
        knot = rai.RectLW(200,40).proxy() 

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
    Alignment tool, used for aligning a mask with the contour of a wafer
    """
    def _make(self,
              knot_spacing:float = 50,
              back_length:float = 350,
              back_height:float = 30,
             ):
        
        back = rai.RectLW(back_length,back_height).proxy()
        knot = rai.RectLW(4,10).proxy()

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
                                           .scale(0.2)
                                           .snap_above(self.subcompos[f'knot{i}']).movey(5)
                                          )

            self.marks.center = self.subcompos.back.bbox.top_mid
            self.marks.back_center = self.subcompos.back.bbox.mid
