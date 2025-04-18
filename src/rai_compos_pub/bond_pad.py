#!/usr/bin/env python
# coding: utf-8

# In[8]:


import raimad as rai

class Bond_pad(rai.Compo):
    def _make(self,
              slope_length: float = 50,
              line_width:float = 2,
              pad_trench_width:float = 20,
              line_trench_width:float = 1,
              pad_size:float = 40,
              mode: str = "trench"
             ):
        
        pad = rai.RectLW(pad_size,pad_size).proxy()
        poly = [tuple(pad.bbox.top_right),
                tuple(pad.bbox.bot_right),
                (pad.bbox.mid_right[0]+slope_length, pad.bbox.mid_right[1]-line_width/2),
                (pad.bbox.mid_right[0]+slope_length, pad.bbox.mid_right[1]+line_width/2)
               ]
        slope = rai.CustomPoly(poly).proxy()

        if mode == "trench":
            trench_pad = rai.RectLW(pad_size,pad_trench_width).proxy().snap_above(pad)
            trench_poly = [tuple(trench_pad.bbox.top_right),
                           tuple(trench_pad.bbox.bot_right),
                           poly[3],
                           (poly[3][0],poly[3][1]+line_trench_width)
                          ]
            slope_trench = rai.CustomPoly(trench_poly)
            end_trench = rai.RectLW(5,pad_size+2*pad_trench_width).proxy()
            
            self.subcompos.trench_pad_T = trench_pad.proxy().map("trench")
            self.subcompos.trench_pad_B = trench_pad.proxy().snap_below(pad).map("trench")
            self.subcompos.trench_slope_T = slope_trench.proxy().map("trench")
            self.subcompos.trench_slope_B = slope_trench.proxy().hflip().map("trench")
            self.subcompos.trench_end = end_trench.proxy().snap_left(pad).map("trench")

        else:
            self.subcompos.base_pad = pad.map('wire')
            self.subcompos.pad_slope = slope.map('wire')

        self.subcompos.bond_plate = pad.proxy().scale(1.05).map('bond_material')

        self.marks.connection_point = self.bbox.mid_right


# In[9]:


test = Bond_pad()
display(test)
rai.show(test)


# In[ ]:




