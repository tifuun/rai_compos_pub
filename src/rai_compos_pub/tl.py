"""tl.py -- transmission line builder"""

import raimad as rai

from dataclasses import dataclass
from enum import Enum

class TLSegType(Enum):
    START_AT = 0
    STRAIGHT = 1
    ELBOW = 2  # not implemented
    MEANDER = 3  # not implemented

@dataclass
class TLSegment():
    path: TLSegType
    point: rai.t.Point

    straight_compo: rai.t.CompoType

    do_bridges: bool | None = None # not implemented
    bridge_spacing: float | None = None  # not implemented
    bridge_spread: float | None = None # not implemented


class TL():
    def __init__(self):
        self.path = []
        self.straight_compo = None

        self.straights_ = []

    def to(self, seg: TLSegment):

        if seg.straight_compo is None:
            raise Exception()
        
        # TODO some sort of "default" template TLSegment?
        # TODO make sure first path seg is always START_AT

        self.path.append(seg)

    def straight_to(self, point: rai.t.Point):
        self.to(
            TLSegment(
                path=TLSegType.STRAIGHT,
                point=point,
                straight_compo=self.straight_compo
                )
            )

    def start_at(self, point: rai.t.Point):
        self.to(
            TLSegment(
                path=TLSegType.START_AT,
                point=point,
                straight_compo=self.straight_compo
                )
            )

    def build(self):
        for one, two in rai.duplets(self.path):

            length = rai.distance_between(one.point, two.point)
            angle = rai.angle_between(one.point, two.point)

            straight = one.straight_compo(length=length).proxy()
            straight.rotate(angle)
            straight.marks.tl_enter.to(one.point)

            self.straights_.append(straight)

class TLTest(rai.Compo):
    """Sample component to play around with the TL class"""
    def _make(self):

        from rai_compos_pub import CPWStraight
        # Note: import inside a function is
        # usually an absolutely insane way of writing Python code.
        # This is just for experimentation purposes tho.

        Straight = CPWStraight.partial(
            signal_width=2,
            gap_width=2,
            gnd_width=2,
            resist_margin=3,
            )

        tl = TL()
        tl.straight_compo = Straight

        tl.start_at((0, 0))
        tl.straight_to((10, 10))
        tl.straight_to((30, 10))
        tl.straight_to((40, 0))

        tl.build()

        self.subcompos.extend(tl.straights_)

