import raimad as rai
import numpy as np
from rai_compos_pub import RAIText

### Optical allignment marker

#### Large marker
class Opt_align_large_mark(rai.Compo):
    def _make(self,
              height: int = 390/2, #bar height
              width: int = 108, # default bar width
              gap: int = 40, # gap between bars equal to circle width
              number_steps: int = 2, # number of steps in bar / 2
              step_depth :int = 3, #depth of step
              squeeze :int = -2, #overlap between bar and center circles
              layer_list :list= ['layer1','layer2']
             ):
        
        bar_list = [(0,0)]
        
        for m in range(0, number_steps+1):
            bar_list.append((
                width-m*step_depth,
                height*m/(number_steps+1)
            ))
            bar_list.append((
                width-m*step_depth,
                height*(m+1)/(number_steps+1)
            ))

        bar_list.append( (0,height) )
        bar = rai.CustomPoly(bar_list).proxy().move((-width-gap/2+squeeze),0).map(layer_list[0])

        self.subcompos['bar_1'] = bar.proxy()
        self.subcompos['bar_2'] = bar.proxy().hflip()
        self.subcompos['bar_3'] = bar.proxy().vflip()
        self.subcompos['bar_4'] = bar.proxy().hflip().vflip()

        bol = rai.Circle(gap/2).proxy().map(layer_list[1])

        for m in range(-number_steps-1,number_steps+1):
            self.subcompos[f'bol_{m}'] = bol.proxy().move(0,(m+0.5)*height/(number_steps+1))

        self.marks.test = (50,100)

#### Minor marker

class Opt_align_mark_minor(rai.Compo):
    """
    Requires: [RAIMAD]
    """

    def _make(self,
              inner_box_size: tuple = (8,16), # widht / height of inner box
              outer_box_size : tuple = (15,26), # widht / height of outer box
              gap_inner : float = 4, # gap of inner box
              gap_outer : float = 8, # gap of inner box
              radius_circle : float = 2.5, # radius of circle
              circle_seperation : float = 10, # separation of two adjacent circles
              layer_list: list = ['layer1','layer2']
             ):

        inner_box_l = rai.RectLW(inner_box_size[0], inner_box_size[1]).proxy().move(inner_box_size[0]/2+gap_inner/2,inner_box_size[1]/2).map(layer_list[0])
        outer_box_l = rai.RectLW(outer_box_size[0], outer_box_size[1]).proxy().move(outer_box_size[0]/2+gap_outer/2,outer_box_size[1]/2 + 2*inner_box_size[1]).map(layer_list[0])
        
        yi = 0
        circles_inner = 0
        while yi+2*radius_circle <= inner_box_size[1]:
            yi += 2*radius_circle
            circles_inner += 1
            if yi+circle_seperation-2*radius_circle <= inner_box_size[1]:
                yi += circle_seperation-2*radius_circle

        yo = 0
        circles_outer = 0
        while yo+2*radius_circle <= outer_box_size[1]:
            yo += 2*radius_circle
            circles_outer += 1
            if yo+circle_seperation-2*radius_circle <= outer_box_size[1]:
                yo += circle_seperation-2*radius_circle
            
        # circles_inner = int((self.options.inner_box_size[1]-2*self.options.radius_circle)/(4*self.options.radius_circle)+1)
        pos_correction_inner = (inner_box_size[1] - yi)/2
        
        # circles_outer = int((self.options.outer_box_size[1]-2*self.options.radius_circle)/(4*self.options.radius_circle)+1)
        pos_correction_outer = (outer_box_size[1] - yo)/2
        
        self.subcompos['inner_box_l'] = inner_box_l
        self.subcompos['inner_box_2'] = inner_box_l.proxy().vflip()
        self.subcompos['outer_box_l'] = outer_box_l
        self.subcompos['outer_box_2'] = outer_box_l.proxy().vflip()

        
        for i in range(0,circles_inner):
            self.subcompos[f'circle_inner_{i}'] = rai.Circle(radius_circle).proxy().move(0,i*(circle_seperation)+pos_correction_inner+radius_circle).map(layer_list[1])

        for i in range(0,circles_outer):
            self.subcompos[f'circle_outer_{i}'] = rai.Circle(radius_circle).proxy().move(0,i*(circle_seperation)+pos_correction_outer+radius_circle+2*inner_box_size[1]).map(layer_list[1])

        self.marks.max_X = (outer_box_size[1]+gap_outer/2,0)
        self.marks.max_Y = (0,2*inner_box_size[1]+outer_box_size[1])

#### Assembly minor and major

class Opt_align_major_assembly(rai.Compo):
    """
    Requires [pycif,pc_text]
    """        
    def _make(self,
             layer_list = ['layer01','layer02']
             ):   
        "Object creation and manipulation"
        object = Opt_align_large_mark(
            height = 390/2,
            width = 108,
            gap = 40,
            number_steps = 2,
            step_depth = 3,
            squeeze = -2,
            layer_list = layer_list,
        ).proxy()

        North = object.bbox.bot_mid.to(object.bbox.top_mid).move(0,400)
        
        " Place objects "
        self.subcompos['North'] = North
        self.subcompos['East'] = North.proxy().rotate(np.pi/2)
        self.subcompos['West'] = North.proxy().rotate(-np.pi/2)
        self.subcompos['South'] = North.proxy().rotate(np.pi)

class Opt_align_minor_assembly(rai.Compo):
    """
    Requires [pycif,pc_text]
    """

    def _make(self,
             layer_list = ['layer1','layer2']):
        "Object creation and manipulation"
        object = Opt_align_mark_minor(
            inner_box_size =(8,16),
            outer_box_size =(15,26),
            gap_inner =4,
            gap_outer =8,
            radius_circle = 2.5,
            circle_seperation = 10,
        ).proxy()

        North = object.bbox.mid.to(object.bbox.top_mid)

        self.subcompos['North'] = North
        self.subcompos['East'] = North.proxy().rotate(np.pi/2)
        self.subcompos['West'] = North.proxy().rotate(-np.pi/2)
        self.subcompos['South'] = North.proxy().rotate(np.pi)
        
        self.subcompos['circle'] = rai.Circle(2).proxy().map('layer2') #This is for the development stage as it shows the origin

#### Full marker assembly
class Opt_align_mark(rai.Compo):
    """ 
    
    Dependencies; RAIText
    """
            
    def _make(self,
             layer_list = ['layer1','layer2'],
             label = '1',
             ):
        "Object creation and manipulation"
        main_alligner = Opt_align_major_assembly(
            layer_list = layer_list,
        )

        minor_alligner = Opt_align_minor_assembly().proxy().move(-140,210)

        label_1  = RAIText(label).proxy().scale(4).bbox.mid.to((700,700)).map(layer_list[0])
        label_2 = label_1.proxy()
        
        "Placing the objects"
        self.subcompos['main'] = main_alligner.proxy()
        self.subcompos['minor_1'] = minor_alligner.proxy()
        self.subcompos['minor_2'] = minor_alligner.proxy().rotate(np.pi/2)
        self.subcompos['minor_3'] = minor_alligner.proxy().rotate(np.pi)
        self.subcompos['minor_4'] = minor_alligner.proxy().rotate(-np.pi/2)

        "Placing the labels"
        self.subcompos['label_1'] = label_1
        self.subcompos['label_2'] = label_1.proxy().map(layer_list[1])
