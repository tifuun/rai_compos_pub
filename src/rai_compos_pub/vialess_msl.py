import raimad as rai

from rai_compos_pub import CPWTaperMetal

class Pgram(rai.Compo):
    r"""
    Parallelogram.

    |-- l --|
             _
           /|
          / |
         /  |   h1
        /   |    
       /    |  
      /     |
     /______|_   
    |       |    
    |       |    
    x       +   w
    |       |    
    |_______|_   
     \      |    
       \    |    
         \  |   h2
           \|_   

    Marks:
        `x`: marks.tl_enter
        `+`: marks.tl_exit

    """

    def _make(self, l: float, w: float, h1: float, h2: float):
        self.geoms.update({
            'root': [
                [
                    (0, 0),
                    (0, w),
                    (l, w + h1),
                    (l, -h2),
                    ]
                ]
            })

        self.marks.tl_enter = (0, w / 2)
        self.marks.tl_exit = (l, w / 2)

class CPWMetal(rai.Compo):
    """
    CPW (positive image).
    Adapted from cpw:CPWSegment
    """
    class Options:
        length = rai.Option.Geometric(
            "length of segment",
            browser_default=10
            )
        sig = rai.Option.Geometric(
            "width of signal line",
            browser_default=3
            )
        gap = rai.Option.Geometric(
            "width of gaps between signal line and gnd lines",
            browser_default=1
            )
        gnd = rai.Option.Geometric(
            "width of gnd lines",
            browser_default=2
            )

    class Marks:
        tl_enter = rai.Mark("Start of CPW segment")
        tl_exit = rai.Mark("End of CPW segment")

    def _make(
            self,
            length: float,
            signal_width: float,
            gap_width: float,
            gnd_width: float,
            ):

        signal = rai.RectLW(length, signal_width).proxy()
        gnd1 = rai.RectLW(length, gnd_width).proxy()
        gnd2 = gnd1.shallow_copy()

        # gnd1 goes above signal
        gnd1.snap_above(signal)
        gnd1.move(0, gap_width)

        # gnd2 goes below signal
        gnd2.snap_below(signal)
        gnd2.move(0, -gap_width)

        # Register subcompos
        self.subcompos.signal = signal
        self.subcompos.gnd1 = gnd1
        self.subcompos.gnd2 = gnd2

        # Register marks
        self.marks.tl_enter = signal.bbox.mid_left
        self.marks.tl_exit = signal.bbox.mid_right

class MSLHalf(rai.Compo):
    def _make(self):
        """Left half of the MSL structure."""

        sizes = (
            # ( 0, GND left, GAP left, SIG left),
            # ( Length, GND right, GAP right, SIG right),

            (0     , 0    , 0    , 60),
            (10    , 0    , 0    , 60),

            (0     , 5    , 25   , 0 ),
            (10    , 5    , 25   , 0 ),

            # straight
            (0     , 5    , 5    , 40),
            (40    , 5    , 5    , 40),

            # taper
            (0     , 5    , 5    , 40),
            (30    , 15   , 5    , 20),

            # straight
            (0     , 15   , 5    , 20),
            (10    , 15   , 5    , 20),

            # taper
            (0     , 15   , 5    , 20),
            (10    , 20   , 5    , 10),

            # straight
            (0     , 20   , 5    , 10),
            (10    , 20   , 5    , 10),

            # taper
            (0     , 20   , 5    , 10),
            (20    , 22.5 , 5    , 5 ),

            # straight line, taper gap
            (0     , 22.5 , 5    , 5 ),
            (20    , 17.5 , 10   , 5 ),

            # continue line with no gnd
            (0     , 0    , 27.5 , 5 ),
            (30    , 0    , 27.5 , 5 ),
            )

        parts = tuple(
            CPWTaperMetal(
                l=r[0],
                gl1=l[1], wl1=l[2], sl=l[3],# wl2=l[4], gl2=l[5],
                gr1=r[1], wr1=r[2], sr=r[3],# wr2=r[4], gr2=r[5],
                ).proxy()
            for l, r in rai.couples(sizes)
            )
        
        for left, right in rai.duplets(parts):
            right.snap_right(left)

        self.subcompos.extend(parts)


class MSLHalves(rai.Compo):
    """Two halves of the MSL structure joined together with a signal line"""
    def _make(self):
        left = MSLHalf().proxy()
        right = MSLHalf().proxy()

        right.vflip()

        right.snap_right(left)

        # Register subcompos
        self.subcompos.left = left
        self.subcompos.right = right

class Headphones(rai.Compo):
    def _make(self):
        band = rai.RectLW(10, 2).proxy()
        stem_l = rai.RectLW(2, 10).proxy()
        stem_r = rai.RectLW(2, 10).proxy()
        cup_l = rai.RectLW(4, 4).proxy()
        cup_r = rai.RectLW(4, 4).proxy()

        stem_l.bbox.top_right.to(band.bbox.top_left)
        stem_r.bbox.top_left.to(band.bbox.top_right)

        cup_l.snap_below(stem_l)
        cup_r.snap_below(stem_r)

        self.subcompos.band = band
        self.subcompos.cup_l = cup_l
        self.subcompos.cup_r = cup_r
        self.subcompos.stem_l = stem_l
        self.subcompos.stem_r = stem_r

class Snake(rai.Compo):
    """
    Meander at the top middle of the VialessMSL chip.

    Once raimad.path / raimad.tl get reimplemented,
    we will be able to construct transmission lines
    just by passing points and parameters.
    But for now we just build it by hand like a toy railroad.
    """
    def _make(self):
        straight1 = rai.RectLW(5, 2).proxy()
        straight2 = straight1.shallow_copy()
        straight3 = straight1.shallow_copy()
        straight4 = straight1.shallow_copy()

        bend1 = rai.AnSec.from_auto(
            rmid=4,
            dr=2,
            thetamid=0,
            dtheta=rai.semicircle,
            ).proxy()
        bend2 = bend1.shallow_copy().vflip()
        bend3 = bend1.shallow_copy()

        bend1.bbox.bot_left.to(straight1.bbox.bot_right)
        straight2.bbox.top_right.to(bend1.bbox.top_left)
        bend2.bbox.bot_right.to(straight2.bbox.bot_left)
        straight3.bbox.top_left.to(bend2.bbox.top_right)
        bend3.bbox.bot_left.to(straight3.bbox.bot_right)
        straight4.bbox.top_right.to(bend3.bbox.top_left)

        self.subcompos.bend1 = bend1
        self.subcompos.bend2 = bend2
        self.subcompos.bend3 = bend3
        self.subcompos.straight1 = straight1
        self.subcompos.straight2 = straight2
        self.subcompos.straight3 = straight3
        self.subcompos.straight4 = straight4

        # There will be a small gap between the bends and straight segments.
        # RAIMAD bug, will fix!!

class Cover(rai.Compo):
    def _make(self):
        rect = rai.RectLW(100, 100).proxy()
        pgram = Pgram(20, 20, -8, -8).proxy()
        tri = Pgram(30, 4, -2, -2).proxy()

        pgram.snap_right(rect)
        tri.snap_right(pgram)

        self.subcompos.rect = rect
        self.subcompos.pgram = pgram
        self.subcompos.tri = tri


class VialessMSL(rai.Compo):
    """via-less MSL test chip draft."""
    def _make(self):
        halves = MSLHalves().proxy()
        headphones = Headphones().proxy()
        snake = Snake().proxy()

        cover_l = Cover().proxy()
        cover_r = cover_l.shallow_copy()

        cover_r.vflip()

        headphones.bbox.top_mid.to(halves.bbox.mid).movey(-10)
        snake.bbox.bot_mid.to(halves.bbox.mid).movey(10)

        cover_l.bbox.mid_left.to(halves.bbox.mid_left)
        cover_r.bbox.mid_right.to(halves.bbox.mid_right)

        halves.map('al')
        headphones.map('al')
        snake.map('al')
        cover_l.map('nbtin_hole')
        cover_r.map('nbtin_hole')

        self.subcompos.snake = snake
        self.subcompos.halves = halves
        self.subcompos.headphones = headphones
        self.subcompos.cover_l = cover_l
        self.subcompos.cover_r = cover_r
        

