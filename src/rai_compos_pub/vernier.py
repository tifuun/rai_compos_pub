#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import raimad as rai
import numpy as np

from rai_compos_pub import RAIText

class Ruler_marker(rai.Compo):
    """
    A rudimentary ruler shape
    """
    class Options:
        pass

    class Marks:
        pass
    
    def _make(self,
              height: float =10,
              length: float =50,
              gap: float = 10,
              number_of_bars: int = 11,
              zero_bar_ratio: float = 1.4,
              indicator_bar_ratio: float = 1.2,
              indicator_number: int = 5
             ):
        
        bars_dict = {}  # Dictionary to store bars

        if number_of_bars %2 == 0:
            print("number of bars should be an odd integer")
            return
        
        for i in range(number_of_bars):
            bar_name = f"bar{i+1}"  # Dynamically create bar names (e.g., bar1, bar2, ...)
            
            if i == int(number_of_bars/2): #Zerobar
                bars_dict[bar_name] = rai.RectLW(zero_bar_ratio*length, height).proxy().move(-zero_bar_ratio*length/2,height/2)
                
            elif (i-int(number_of_bars/2))%indicator_number == 0: #Indicatorbar
                bars_dict[bar_name] = rai.RectLW(indicator_bar_ratio*length, height).proxy().move(-indicator_bar_ratio*length/2,height/2)
            else: #Intermediate bars
                bars_dict[bar_name] = rai.RectLW(length, height).proxy().move(-length/2,height/2)
            
            bars_dict[bar_name].move(0, (i- (number_of_bars-0.5)/2) * (gap+height))
            self.subcompos[bar_name] = bars_dict[bar_name]

        
        self.marks.zerobar_center = (0,0)
        self.marks.zerobar_tip = (-zero_bar_ratio*length,0)

class Vernier_marker(rai.Compo):
    """
    Requires: RAIText
    """
    
    def _make(self,
              pitch: float = 0.4,
              delta_pitch: float = 0.005,
              bar_length: float = 1.2,
              number_of_bars: int = 41,
              layer_list: list = ["layer 1","layer 2"],
              labels: bool = False,
             ):
        
        height = pitch/2
        length = bar_length
        gap = pitch/2
        
        Ruler_1 = Ruler_marker(height, length, gap, number_of_bars).proxy()
        Ruler_2 = Ruler_marker(height, length, gap+delta_pitch, number_of_bars).proxy().vflip()

        self.subcompos.Ruler_1 = Ruler_1.map(layer_list[0])
        self.subcompos.Ruler_2 = Ruler_2.map(layer_list[1])
        
        ### Label
        if labels == True:
                        
            label_scale_1 = self.bbox.width / RAIText(layer_list[0]).proxy().bbox.length * 0.6
            label_scale_2 = self.bbox.width / RAIText(layer_list[1]).proxy().bbox.length * 0.6
    
            Label_1 = RAIText(layer_list[0], scale = label_scale_1).proxy().rotate(np.pi/2)
            Label_2 = RAIText(layer_list[1], scale = label_scale_2).proxy().rotate(-np.pi/2)
            
            self.subcompos.Label_1 = Label_1.bbox.mid_right.to(Ruler_1.marks.zerobar_tip).movex(-2).map(layer_list[0])
            self.subcompos.Label_2 = Label_2.bbox.mid_left.to(Ruler_2.marks.zerobar_tip).movex(2).map(layer_list[1])


        # self.subcompos.circle = rai.Circle(0.3).proxy().bbox.mid.to(Ruler_1.marks.zerobar_tip)

