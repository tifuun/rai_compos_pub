"""microstrip.py: contains microstrip segments for toydeshima2"""

import raimad as rai

class MSStraight(rai.Compo):
    def _make(
            self,
            length: float,
            width: float
            ):
        self.geoms.update({
            'root': [
                [
                    (0, - width / 2),
                    (length, - width / 2),
                    (length, width / 2),
                    (0, width / 2),
                    ]
                ]
            })
        self.marks.tl_enter = (0, 0)
        self.marks.tl_exit = (length, 0)

class MSBend(rai.Compo):
    def _make(
            self,
            bend_radius: float,
            width: float,
            dtheta: float
            ):
        ansec = rai.AnSec.from_auto(
            rmid=bend_radius,
            dr=width,
            theta1=0,
            dtheta=dtheta,
            ).proxy()
        self.subcompos.ansec = ansec

        self.marks.tl_enter = (bend_radius, 0)
        self.marks.tl_exit = rai.polar(arg=dtheta, mod=bend_radius)
        self.marks.center = (0, 0)

