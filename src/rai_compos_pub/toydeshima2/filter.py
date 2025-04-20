"""filter.py: contains Filter compo for toydeshima2"""

import raimad as rai

class GNDGap(rai.Compo):
    """
    Ground plane for toydeshima2 filter with gap.

          gap_dist                 
      |-----------|                
               |--|--| gap_length       
                                    
       ________   b   ____   ___  ___
      |########|     |####|   |    |    
      |########|  a  |####|   |    | gap_width
      |########|_____|####|   |   _|_   
      |###################|   |         
      |###################|   |         
      |###################|   | width   
      |###################|   |      
       ~~~~~~~~~~~~~~~~~~~   ---
      |-------------------|             
            length                      
                                        
    """

    tags = ["toydeshima2", "example"]

    class Marks:
        gap_mid = rai.Mark("Middle of gap (whows as 'a' on the diagram)")
        gap_enter = rai.Mark("Top middle of gap (whows as 'b' on the diagram)")

    class Options:
        length = rai.Option("Length of ground plane")
        width = rai.Option("Width of ground plane")
        gap_dist = rai.Option(
            "Distance from left of ground play to middle of gap"
            )
        gap_length = rai.Option("Length of gap")
        gap_width = rai.Option("Width of gap")

    def _make(
            self,
            length: float = 10,
            width: float = 10,
            gap_dist: float = 7,
            gap_length: float = 3,
            gap_width: float = 3
            ):

        gap_left = gap_dist - gap_length / 2
        gap_right = gap_dist + gap_length / 2

        self.geoms.update({
            'root': [
                [
                    (0, 0),
                    (gap_left, 0),
                    (gap_left, -gap_width),
                    (gap_right, -gap_width),
                    (gap_right, 0),
                    (length, 0),
                    (length, -width),
                    (0, -width),
                    ]
                ]
            })

def _bbox_of_group(compos: tuple[rai.t.CompoLike]) -> rai.BBox:
    """Calculate BBox encompassing multiple compos"""
    bbox = rai.BBox()
    for compo in compos:
        for polys in compo.steamroll().values():
            for poly in polys:
                bbox.add_poly(poly)
    return bbox

class Filter(rai.Compo):
    r"""
    I-Shaped filter for toydeshima2.


          |--| gnd_top_pad
        |----| gnd_bot_pad

                  |-| res_w
             |-----------| coup_top_l
            ________________     ___         
           |  ___________   |     | gnd_split    ___
           | |____   ____|  |     | ___          _|_ coup_top_w
           |      | |       |     |  |
          _|______| |_______|__  _|_ | res_l
         |        | |          |     |
         |     ___| |___       |    _|_          ___ 
         |    |_________|      |    ___          _|_ coup_bot_w
         |   _____________     |    _|_ gap
         |  /  __________ \    |          
         |  | |          | |   |              
         |  | |         _| |_  |   ___        
         |  | |        | | | | |    |  gap_w  
     ___ |__| |________| |_| |_|   _|_        
     _|_    |_|                               
    short_l                                       
              |---------| coup_bot_l      

                       |-----| gap_l
                                          
    """

    tags = ["toydeshima2", "example"]

    def _make(
            self,
            res_l: float = 100,
            res_w: float = 20,
            coup_top_l: float = 100,
            coup_top_w: float = 20,
            coup_bot_l: float = 80,
            coup_bot_w: float = 20,
            short_l: float = 40,
            gap_w: float = 50,
            gap_l: float = 60,
            gnd_split: float = 70,
            gap: float = 10,
            gnd_top_pad: float = 20,
            gnd_bot_pad: float = 50,
            ):

        ### Make I-Shape and gnd-top ###

        res = rai.RectLW(res_w, res_l).proxy()
        coup_top = rai.RectLW(coup_top_l, coup_top_w).proxy()
        coup_bot = rai.RectLW(coup_bot_l, coup_bot_w).proxy()

        coup_top.snap_above(res)
        coup_bot.snap_below(res)

        gnd_top = rai.RectLW(
            coup_top.bbox.length + 2 * gnd_top_pad,
            gnd_split
            ).proxy()

        gnd_top.bbox.top_left.to(coup_top.bbox.top_left)
        gnd_top.move(-gnd_top_pad, gnd_top_pad)

        ### Make line ###

        line_top = rai.RectLW(coup_bot_l, coup_bot_w).proxy()
        line_left = rai.RectLW(coup_bot_w, res_l + short_l).proxy()
        line_right = rai.RectLW(coup_bot_w, res_l).proxy()
        corner_l = rai.CustomPoly((
            (0, 0),
            (coup_bot_w, coup_bot_w),
            (coup_bot_w, 0)
            )).proxy()
        corner_r = corner_l.shallow_copy().vflip()

        line_top.snap_below(coup_bot)
        line_top.movey(-gap)
        corner_l.snap_left(line_top)
        corner_r.snap_right(line_top)
        line_left.snap_below(corner_l)
        line_right.snap_below(corner_r)

        ### Make gnd_bot ###

        gnd_bot_w = (
            (coup_top.bbox.top + gnd_top_pad)
            - line_right.bbox.bottom
            - gnd_split
            )
        gnd_bot_l = coup_top_l + 2 * gnd_bot_pad

        gnd_bot = GNDGap(
            length=gnd_bot_l,
            width=gnd_bot_w,
            gap_width=gap_w,
            gap_length=gap_l,
            gap_dist = (gnd_bot_l + coup_bot_l + coup_bot_w) / 2,
            ).proxy().hflip()

        gnd_bot.snap_below(gnd_top)

        ### Register subcompos and assign layers ###

        self.subcompos.res = res.map('metal')
        self.subcompos.coup_bot = coup_bot.map('metal')
        self.subcompos.coup_top = coup_top.map('metal')
        self.subcompos.gnd_top = gnd_top.map('gnd')
        self.subcompos.line_top = line_top.map('metal')
        self.subcompos.line_left = line_left.map('metal')
        self.subcompos.line_right = line_right.map('metal')
        self.subcompos.corner_l = corner_l.map('metal')
        self.subcompos.corner_r = corner_r.map('metal')
        self.subcompos.gnd_bot = gnd_bot.map('gnd')


