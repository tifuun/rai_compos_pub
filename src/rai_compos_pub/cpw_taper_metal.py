"""cpw_taper_metal.py: contains CPWTaperMetal component."""

import raimad as rai

class CPWTaperMetal(rai.Compo):
    """
    Tapered CPW (positive image).
    Adapted from cpw:CPWSegment

            |----- l ------|
                         __    _
                     __--  |  |
                 __--      |  |  gr1
        _    __--        __|  |_
    gl1  |  |      ___---     |  wr1
        _|  |___---    ____   |_ 
    wl1 _|   _____-----    |  |
    sl   |  |              |  |
        _|  |_____         |  |  sr
    wl2 _|   ___  -----____|  |_
    sl2  |  |   ---___        |  wr2
        _|  |__       ---__   |_
               --__        |  |
                   --__    |  |  gr2
                       --__|  |_
    """
    class Options:
        l = rai.Option.Geometric(
            "length of segment",
            )
        sl = rai.Option.Geometric(
            "width of signal line on the left",
            )
        sr = rai.Option.Geometric(
            "width of signal line on the right",
            )

        wl1 = rai.Option.Geometric(
            "width of top gap on the left",
            )
        wr1 = rai.Option.Geometric(
            "width of top gap on the right",
            )
        gl1 = rai.Option.Geometric(
            "width of top ground line on the left",
            )
        gr1 = rai.Option.Geometric(
            "width of top ground line on the right",
            )

        wl2 = rai.Option.Geometric(
            "width of bottom gap on the left (None to use wl1)",
            )
        wr2 = rai.Option.Geometric(
            "width of bottom gap on the right (None to use wr1)",
            )
        gl2 = rai.Option.Geometric(
            "width of bottom ground line on the left (None to use gl1)",
            )
        gr2 = rai.Option.Geometric(
            "width of bottom ground line on the right (None to use gr1)",
            )

    class Marks:
        tl_enter = rai.Mark("Start of CPW segment")
        tl_exit = rai.Mark("End of CPW segment")

    def _make(
            self,
            l: float = 50,
            sl: float = 10,
            sr: float = 12,
            wl1: float = 10,
            wr1: float = 12,
            gl1: float = 10,
            gr1: float = 12,
            wl2: float | None = None,
            wr2: float | None = None,
            gl2: float | None = None,
            gr2: float | None = None,
            ):
        
        if wl2 is None: wl2 = wl1
        if wr2 is None: wr2 = wr1
        if gl2 is None: gl2 = gl1
        if gr2 is None: gr2 = gr1

        self.geoms.update({
            'root': [
                [  # Signal
                    (0, sl / 2),
                    (l, sr / 2),
                    (l, - sr / 2),
                    (0, - sl / 2),
                    ],
                [  # GND top
                    (0, (sl / 2 + wl1) + gl1 ),
                    (l, (sr / 2 + wr1) + gr1 ),
                    (l, (sr / 2 + wr1)       ),
                    (0, (sl / 2 + wl1)       ),
                    ],
                [  # GND bottom
                    (0, - ( (sl / 2 + wl2) + gl2 )),
                    (l, - ( (sr / 2 + wr2) + gr2 )),
                    (l, - ( (sr / 2 + wr2)       )),
                    (0, - ( (sl / 2 + wl2)       )),
                    ],
                ]
            })

        # Register marks
        self.marks.tl_enter = (0, 0)
        self.marks.tl_exit = (l, 0)


