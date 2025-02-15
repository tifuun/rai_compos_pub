from math import radians

import raimad as rai

class CPWLayers:
    resist = rai.Layer('Resist layer above signal line')
    insl = rai.Layer('Insulator between CPW and bridge')
    bridge = rai.Layer('Conducting part of bridge')
    conductor = rai.Layer('Conducting layer for signal and ground lines')

class CPWStraight(rai.Compo):
    class Layers(CPWLayers):
        pass

    class Options:
        length = rai.Option.Geometric(
            "length of segment",
            browser_default=10
            )
        signal_width = rai.Option.Geometric(
            "width of signal line",
            browser_default=3
            )
        gap_width = rai.Option.Geometric(
            "width of gaps between signal line and gnd lines",
            browser_default=1
            )
        gnd_width = rai.Option.Geometric(
            "width of gnd lines",
            browser_default=2
            )
        resist_margin = rai.Option.Geometric(
            "shrink width of resist on either side of segment by this much",
            browser_default=1
            )

    class Marks:
        tl_enter = rai.Mark("Start of CPW straight segment")
        tl_exit = rai.Mark("End of CPW straight segment")

    def _make(
            self,
            length: float,
            signal_width: float,
            gap_width: float,
            gnd_width: float,
            resist_margin: float,
            ):

        signal = rai.RectLW(length, signal_width).proxy().map('conductor')
        gnd1 = rai.RectLW(length, gnd_width).proxy().map('conductor')
        gnd2 = gnd1.proxy()
        resist = rai.RectLW(
            length,
            (
                + signal_width
                + gap_width * 2
                + gnd_width * 2
                - resist_margin * 2
                )
            ).proxy().map('resist')

        # gnd1 goes above signal
        gnd1.snap_above(signal)
        gnd1.move(0, gap_width)

        # gnd2 goes below signal
        gnd2.snap_below(signal)
        gnd2.move(0, -gap_width)

        # resist goes directly ontop of signal
        resist.bbox.mid.to(signal.bbox.mid)

        # Register subcompos
        self.subcompos.signal = signal
        self.subcompos.gnd1 = gnd1
        self.subcompos.gnd2 = gnd2
        self.subcompos.resist = resist

        # Register marks
        self.marks.tl_enter = signal.bbox.mid_left
        self.marks.tl_exit = signal.bbox.mid_right

class CPWBend(rai.Compo):
    class Layers(CPWLayers):
        pass

    class Options:
        signal_width = rai.Option.Geometric(
            "width of signal line",
            browser_default=3
            )
        gap_width = rai.Option.Geometric(
            "width of gaps between signal line and gnd lines",
            browser_default=1
            )
        gnd_width = rai.Option.Geometric(
            "width of gnd lines",
            browser_default=2
            )
        resist_margin = rai.Option.Geometric(
            "shrink width of resist on either side of segment by this much",
            browser_default=1
            )
        bend_radius = rai.Option.Geometric(
            "Radius from bend center to middle of signal line",
            browser_default=10
            )
        dtheta = rai.Option.Geometric(
            "Arc length of bend (radians)",
            browser_default=radians(45)
            )

    class Marks:
        center = rai.Mark("Center of the bend")
        tl_enter = rai.Mark("Start of CPW segment")
        tl_exit = rai.Mark("End of CPW segment")

    def _make(
            self,
            signal_width: float,
            gap_width: float,
            gnd_width: float,
            resist_margin: float,
            bend_radius: float,
            dtheta: float,
            ):

        # Inner (closest to center) GND line
        inner = rai.AnSec.from_auto(
            r2=bend_radius - signal_width / 2 - gap_width,
            dr=gnd_width,
            theta1=0,
            dtheta=dtheta,
            ).proxy().map('conductor')

        # Signal line
        signal = rai.AnSec.from_auto(
            rmid=bend_radius,
            dr=signal_width,
            theta1=0,
            dtheta=dtheta,
            ).proxy().map('conductor')

        # Outter (furthest from center) GND line
        outter = rai.AnSec.from_auto(
            r1=bend_radius + signal_width / 2 + gap_width,
            dr=gnd_width,
            theta1=0,
            dtheta=dtheta,
            ).proxy().map('conductor')

        resist = rai.AnSec.from_auto(
            rmid=bend_radius,
            dr=(
                + signal_width
                + gap_width * 2
                + gnd_width * 2
                - resist_margin * 2  # TODO double-check
                ),  # TODO make it so double-checking is not necessary
            # FIXME no clue what the two TODO's above me are about
            theta1=0,
            dtheta=dtheta,
            ).proxy().map('resist')

        # Register subcompos
        self.subcompos.inner = inner
        self.subcompos.outter = outter
        self.subcompos.signal = signal
        self.subcompos.resist = resist

        # Register marks
        #self.marks.center = signal.marks.center
        #self.marks.start_mid = signal.marks.start_mid
        #self.marks.tl_exit = signal.marks.end_mid

        # TODO ansec marks??
        # YES definitely TODO ansec marks!
        self.marks.center = (0, 0)



