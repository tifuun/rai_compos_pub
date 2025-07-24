import raimad as rai
import numpy as np

from rai_compos_pub import RAIText

class Ruler_marker(rai.Compo):
    """
    A rudimentary ruler shape
    """
    
    class Options:
        width = rai.Option.Geometric(
            "width of the standard bars",
            browser_default = 10)
        length = rai.Option.Geometric(
            "length of the standard bar",
            browser_default = 50)
        gap = rai.Option.Geometric(
            "size of the gap between two bars",
            browser_default = 10)
        number_of_bars= rai.Option.Geometric(
            "total number of bars, needs to be odd (due to center bar)",
            browser_default = 11)
        zero_bar_ratio= rai.Option.Geometric(
            "ratio of the length of the center bar (zero-bar) and standard bar",
            browser_default = 1.4)
        indicator_bar_ratio = rai.Option.Geometric(
            "ratio of the length of the indicator bars and standard bar",
            browser_default = 1.2)
        indicator_number = rai.Option.Geometric(
            "occurrance of the indicator bar, every Nth bar is an indicator bar",
            browser_default = 5)

    class Marks:
        zerobar_center = rai.Mark("the center of the center bar (zero_bar)")
        zerobar_tip = rai.Mark("the center of the far end of the center bar (zero_bar)")
        pass
    
    def _make(self,
              width: float =10,
              length: float =50,
              gap: float = 10,
              number_of_bars: int = 11,
              zero_bar_ratio: float = 1.4,
              indicator_bar_ratio: float = 1.2,
              indicator_number: int = 5
             ):
        bar_dict= {}
        gap_dict = {}
        
        if number_of_bars %2 == 0:
            print("number of bars should be an odd integer")
            return

        ## Construct bars and gaps
        for i in range(number_of_bars):
            bar_name = f"bar{i}"

            # Construct bar
            if i == 0:
                if (i-int(number_of_bars/2))%indicator_number == 0:
                    bar_dict[f"bar{i}"] = (rai.RectLW(indicator_bar_ratio*length, width).proxy()
                                       .bbox.bot_right.to((0,0))
                                      )
                else:
                    bar_dict[f"bar{i}"] = (rai.RectLW(length,width).proxy()
                                       .bbox.bot_right.to((0,0))
                                      )
            elif i == int(number_of_bars/2):
                bar_dict[f"bar{i}"] = (rai.RectLW(zero_bar_ratio*length,width).proxy()
                                       .bbox.bot_right.to(gap_dict[f"gap{i-1}"].bbox.top_right)
                                      )
            elif (i-int(number_of_bars/2))%indicator_number == 0: #Indicatorbar
                bar_dict[f"bar{i}"] = (rai.RectLW(indicator_bar_ratio*length, width).proxy()
                                       .bbox.bot_right.to(gap_dict[f"gap{i-1}"].bbox.top_right)
                                      )
            else:
                bar_dict[f"bar{i}"] = (rai.RectLW(length,width).proxy()
                                       .bbox.bot_right.to(gap_dict[f"gap{i-1}"].bbox.top_right)
                                      )
            # Construct Gap
            gap_dict[f"gap{i}"] = (rai.RectLW(length,gap).proxy()
                                   .snap_above(bar_dict[bar_name])
                                   .bbox.bot_right.to(bar_dict[f"bar{i}"].bbox.top_right)
                                  )
            
            self.subcompos[bar_name] = bar_dict[bar_name]

        ### Marks
        zero_bar_id = f"bar{int(number_of_bars/2)}"
        self.marks.zerobar_center = bar_dict[zero_bar_id].bbox.mid_right
        self.marks.zerobar_tip = bar_dict[zero_bar_id].bbox.mid_left

class Vernier_marker(rai.Compo):
    """
    Requires: RAIText
    """
    
    class Options:
        pitch = rai.Option.Geometric(
            "the distance between the heart of two bars in the first ruler",
            browser_default = 0.4)
        delta_pitch = rai.Option.Geometric(
            "the pitch difference between the two rulers",
            browser_default = 0.005)
        bar_length= rai.Option.Geometric(
            "length of the bar",
            browser_default = 1.2)        
        number_of_bars = rai.Option.Geometric(
            "total number of bars in one ruler, needs to be odd due to center bar",
            browser_default = 41)        
        layer_list = rai.Option.Geometric(
            "list of layer names used for label",
            browser_default = ["Vernier_1","Vernier_2"])        
        labels = rai.Option.Geometric(
            "states whether to make labels or not",
            browser_default = True)        

    class Marks:
        pass
    
    def _make(self,
              pitch: float = 0.4,
              delta_pitch: float = 0.005,
              bar_length: float = 1.2,
              number_of_bars: int = 41,
              layer_list: list = ["Vernier_1","Vernier_2"],
              labels: bool = True
             ):
        
        width = pitch/2
        length = bar_length
        gap = pitch/2
        
        Ruler_1 = Ruler_marker_v2(width, length, gap, number_of_bars).proxy()
        Ruler_2 = (Ruler_marker_v2(width, length, gap+delta_pitch, number_of_bars)
                   .proxy()
                   .vflip()
                   .marks.zerobar_center.to(Ruler_1.marks.zerobar_center)
                  )

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

class Vernier_marker_ebeam(rai.Compo):
    """
    Standard marker used to check for ebeam misalignments
    """
    
    def _make(self,
             layer_list: list = ['layer1','layer2'],
             ):

        Vernier_1 = Vernier_marker(layer_list = layer_list,labels = True).proxy()
        Vernier_2 = Vernier_1.proxy().rotate(np.pi/2).snap_above(Vernier_1).movey(5)
        
        self.subcompos['Vernier_1'] = Vernier_1
        self.subcompos['Vernier_2']  = Vernier_2
