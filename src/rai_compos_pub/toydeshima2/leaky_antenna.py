"""leaky_antenna.py: contains LeakyAntenna and supporting compos"""

import raimad as rai

class LeakyButterfly(rai.Compo):
    r"""
    Butterfly shape for Leaky Antenna
                                                   
                   length                          
               |------------|                      
                                                   
            -  +._                     _.+       
            |  |  '-._             _.-'  |       
            |  |      '-._     _.-'      |       
      width |  |          '-.-'          |       
            |  |         _.-'-._         |       
            |  |     _.-'       '-._     |       
            |  | _.-'               '-._ |       
            -  +'                       '+       
                                                   
    """
    class Marks:
        center = rai.Mark("Center of butterfly shape -- CPW goes here.")

    class Options:
        length = rai.Option("Length of half-butterfly shape")
        width = rai.Option("Width of butterfly shape")

    def _make(self, length: float = 10, width: float = 10):
        self.geoms.update({
            'root': [
                [
                    (-length, width),
                    (0, 0),
                    (-length, -width),
                    ],
                [
                    (length, width),
                    (0, 0),
                    (length, -width),
                    ],
                ],
            })

        self.marks.center = (0, 0)

class LeakyAntenna(rai.Compo):
    r"""
    Leaky antenna for toydeshima2.
                                                       
                                         radius        
                                     |-------------|   
                                 
                               , - ~ ~ ~ - ,
                           , '               ' ,     
                         ,    +-------------+    ,   - 
                   _    ,     |  _       _  |     ,  | 
      butterfly_  |    ,      | | \_   _/ | |      , |  
         width    |    ,      | |   \_/   | |      , | box_width
                  |    ,      | |  _/ \_  | |      , |   
                  |_    ,     | |_/     \_| |     ,  | 
                         ,    |             |    ,   |    
                           ,  +-------------+ , '    -   
                             ' - , _ _ _ ,  '
                                                       
                                |----| butterfly_length
                                                       
                              |-------------|
                                 box_length

    """
    class Layers:
        conductor = rai.Layer("Conductor layer with butterfly shape")
        diel = rai.Layer("Dielectric layer")
        gnd = rai.Layer("Ground layer")

    class Marks:
        center = rai.Mark("Center of butterfly shape -- CPW goes here.")

    class Options:
        butterfly_length = rai.Option("Length of half-butterfly shape")
        butterfly_width = rai.Option("Width of butterfly shape")
        box_length = rai.Option("Length of box")
        box_width = rai.Option("Width of box")
        radius = rai.Option("Radius of island")
        circle_compo = rai.Option("Use this component for the circle")

    def _make(
            self,
            butterfly_length: float = 10,
            butterfly_width: float = 10,
            box_length: float = 30,
            box_width: float = 30,
            radius: float = 40,
            circle_compo: rai.t.CompoTypeLike = rai.Circle,
            ):
        bfly = LeakyButterfly(
                length=butterfly_length,
                width=butterfly_width
                ).proxy().map('conductor')

        box = rai.RectLW(
                box_length,
                box_width
                ).proxy().map('diel')

        circle = circle_compo(radius=radius).proxy().map('gnd')
        #FIXME in raimad: Partial doesn't work with positional args
        # Either make it work or say explicitly that only kwargs

        box.bbox.mid.to(bfly.marks.center)
        circle.bbox.mid.to(bfly.marks.center)

        self.subcompos.butterfly = bfly
        self.subcompos.box = box
        self.subcompos.circle = circle

        self.marks.center = bfly.marks.center



