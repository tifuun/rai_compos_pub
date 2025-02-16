"""tl.py -- transmission line builder"""

import math
from dataclasses import dataclass
from enum import Enum
from sys import stderr
from typing import Sequence

import raimad as rai

from rai_compos_pub import tl

class log:
    """placeholder until we get actual logging"""
    def debug(test, *fmt):
        print(test % fmt, file=stderr)

class TL():

    path: tuple[tl.Segment]

    bends_: Sequence[rai.t.Compo]
    bridges_: Sequence[rai.t.Compo]
    straights_: Sequence[rai.t.Compo]

    bendspecs_: Sequence[tl.BendSpec]
    bridgespecs_: Sequence[tl.BridgeSpec]
    straightspecs_: Sequence[tl.StraightSpec]

    def __init__(self, path):
        self.path = path
        self.straight_compo = None

        # FIXME this
        self.bend_radius=5

        self.straights_ = []
        self.bends_ = []

    #def to(self, seg: TLSegment):

    #    if seg.straight_compo is None:
    #        raise Exception()
    #    
    #    # TODO some sort of "default" template TLSegment?
    #    # TODO make sure first path seg is always START_AT

    #    self.path.append(seg)

    #def straight_to(self, point: rai.t.Point):
    #    self.to(
    #        TLSegment(
    #            path=TLSegType.STRAIGHT,
    #            point=point,
    #            straight_compo=self.straight_compo
    #            )
    #        )

    #def start_at(self, point: rai.t.Point):
    #    self.to(
    #        TLSegment(
    #            path=TLSegType.START_AT,
    #            point=point,
    #            straight_compo=self.straight_compo
    #            )
    #        )

    #def make_bends(self):
    #    for before, point, after in rai.triplets(self.path):

    #        spec = construct_bend(before.point, point.point, after.point, 5)
    #        # TODO standardize on option names

    #        log.debug(
    #            "Bend: %s %s %s",
    #            spec.angle_start / math.pi,
    #            spec.angle_end / math.pi,
    #            spec.orientation
    #            )
    #        dtheta = spec.angle_end - spec.angle_start

    #        #match spec.orientation:
    #        #    case Orientation.CLOCKWISE:
    #        #        dtheta = rai.fullcircle + dtheta
    #        #    case Orientation.COUNTERCLOCKWISE:
    #        #        pass
    #        #    case _:
    #        #        assert False

    #        bend = self.bend_compo(
    #            dtheta=dtheta,
    #            bend_radius=5
    #            ).proxy()

    #        bend.rotate(spec.angle_start)
    #        bend.marks.center.to(spec.point_center)

    #        self.bends_.append(bend)

    #def make_straights(self):
    #    for before, after in rai.duplets(self.bends_):
    #        length = rai.distance_between(
    #            before.marks.tl_exit,
    #            after.marks.tl_enter
    #            )
    #        angle = rai.angle_between(
    #            before.marks.tl_exit,
    #            after.marks.tl_enter
    #            )

    #        straight = self.straight_compo(length=length).proxy()
    #        straight.rotate(angle)
    #        straight.marks.tl_enter.to(before.marks.tl_exit)

    #        self.straights_.append(straight)


    def make_specs(self):
        log.debug('====== Original path ======')
        log.debug(tl.format_path(self.path))

        path1 = tl.resolve_elbows(self.path)
        log.debug('====== Step 1: resolve elbows ======')
        log.debug(tl.format_path(path1))

        path2 = path1
        #path2 = pc.tl.reduce_straights(path1)
        #log.debug('====== Step 2: reduce straights ======')
        #log.debug(format_path(path2))

        path3, self.bendspecs_ = tl.construct_bends(
            path2,
            radius=self.bend_radius,
            )
        log.debug('====== Step 3: construct bends ======')
        log.debug(tl.format_path(path3))

        #path4, self.bridgespecs_ = rai.tl.construct_bridges(
        #    path3,
        #    do_bridges=self.do_bridges,
        #    spacing=self.bridge_spacing,
        #    scramble=self.bridge_scramble,
        #    bridge_length=self.bridge_length,
        #    )
        #log.debug('====== Step 4: construct bridges ======')
        #log.debug(format_path(path4))
        path4 = path3[:]

        _, self.straightspecs_ = tl.construct_straights(path4)

        self._resolved_path = path4
        # TODO type for path

    def make_bends(self, bend_compo):
        self.bends_ = tl.make_bend_components(
            self.bendspecs_,
            bend_compo
            )
        return self.bends_

    def make_bridges(self, bridge_compo):
        self.bridges_ = tl.make_bridge_components(
            self.bridgespecs_,
            bridge_compo
            )
        return self.bridges_

    def make_straights(self):
        self.straights_ = tl.make_straight_components(
            self.straightspecs_
            )
        return self.straights_



class TLTest(rai.Compo):
    """Sample component to play around with the TL class"""
    def _make(self):

        from rai_compos_pub import CPWStraight, CPWBend
        # Note: import inside a function is
        # usually an absolutely insane way of writing Python code.
        # This is just for experimentation purposes tho.

        StraightA = CPWStraight.partial(
            signal_width=1,
            gap_width=1,
            gnd_width=1,
            resist_margin=2,
            )

        StraightB = CPWStraight.partial(
            signal_width=2,
            gap_width=2,
            gnd_width=2,
            resist_margin=2,
            )

        Bend = CPWBend.partial(
            signal_width=1,
            gap_width=1,
            gnd_width=1,
            resist_margin=2,
            )

        path = (
            tl.StartAt(
                (-10, -10),
                straight=StraightA,
                bend=Bend,
                radius=20
                ),
            tl.StraightTo(
                (10, 10),
                radius=5
                ),
            tl.StraightTo((30, 10)),
            tl.StraightTo((50, -10)),
            tl.StraightTo((50, 20)),
            tl.StraightTo(
                (0, 22),
                straight=StraightB
                ),
            tl.StraightTo(
                (60, 40)
                ),
            tl.StraightTo((60, 0))
            )

        #path = (
        #    tl.StartAt((-10, -10)),
        #    tl.StraightTo((10, 10)),
        #    tl.StraightTo((30, 10)),
        #    tl.StraightTo((50, -10)),
        #    tl.StraightTo((50, 20)),
        #    tl.StraightTo((0, 22)),
        #    tl.StraightTo((60, 40)),
        #    tl.StraightTo((60, 0))
        #    )

        my_tl = TL(path=path)
        my_tl.straight_compo = StraightA
        my_tl.bend_compo = Bend

        my_tl.make_specs()

        my_tl.make_straights()
        my_tl.make_bends(Bend)

        self.subcompos.extend(my_tl.straights_)
        self.subcompos.extend(my_tl.bends_)

