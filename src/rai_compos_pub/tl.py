"""tl.py -- transmission line builder"""

import math
from dataclasses import dataclass
from enum import Enum
from sys import stderr

import raimad as rai

class log:
    """placeholder until we get actual logging"""
    def debug(test, *fmt):
        print(test % fmt, file=stderr)

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
        self.bends_ = []

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

    def make_bends(self):
        for before, point, after in rai.triplets(self.path):

            spec = construct_bend(before.point, point.point, after.point, 5)
            # TODO standardize on option names

            log.debug(
                "Bend: %s %s %s",
                spec.angle_start / math.pi,
                spec.angle_end / math.pi,
                spec.orientation
                )
            dtheta = spec.angle_end - spec.angle_start

            #match spec.orientation:
            #    case Orientation.CLOCKWISE:
            #        dtheta = rai.fullcircle + dtheta
            #    case Orientation.COUNTERCLOCKWISE:
            #        pass
            #    case _:
            #        assert False

            bend = self.bend_compo(
                dtheta=dtheta,
                bend_radius=5
                ).proxy()

            bend.rotate(spec.angle_start)
            bend.marks.center.to(spec.point_center)

            self.bends_.append(bend)

    def make_straights(self):
        for before, after in rai.duplets(self.bends_):
            length = rai.distance_between(
                before.marks.tl_exit,
                after.marks.tl_enter
                )
            angle = rai.angle_between(
                before.marks.tl_exit,
                after.marks.tl_enter
                )

            straight = self.straight_compo(length=length).proxy()
            straight.rotate(angle)
            straight.marks.tl_enter.to(before.marks.tl_exit)

            self.straights_.append(straight)



    def build(self):
        self.make_bends()
        self.make_straights()



class TurnDirection(Enum):
    AROUND = -1
    STRAIGHT = 0
    LEFT = 1
    RIGHT = 2

class Orientation(Enum):
    CLOCKWISE = -1
    COUNTERCLOCKWISE = 1

@dataclass
class BendSpec:
    angle_start: float
    angle_end: float
    radius: float
    orientation: Orientation
    point_enter: rai.t.Point
    point_exit: rai.t.Point
    point_center: rai.t.Point

def cross2d(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

def classify_turn(before, point, after):
    # Thank you ChatGPT for this one,
    # it seems the day has come when AI
    # understands linear algebra better than I do
    prod = cross2d(
        rai.sub(point, before),
        rai.sub(after, point)
        )
    # TODO some way to flatten this?

    if abs(prod) < 0.01:  # TODO epsilon
        return TurnDirection.STRAIGHT
    if prod > 0:
        return TurnDirection.LEFT
    elif prod < 0:
        return TurnDirection.RIGHT

    # TODO turns around

def construct_bend(
        before: rai.t.Point,
        point: rai.t.Point,
        after: rai.t.Point,
        radius: float
        ):
    angle_incoming = rai.angle_between(before, point)# % rai.fullcircle
    angle_outgoing = rai.angle_between(point, after)# % rai.fullcircle

    log.debug(
        "New turn, in: %.3f, out: %.3f",
        angle_incoming / math.pi,
        angle_outgoing / math.pi,
        )

    turn = angle_outgoing - angle_incoming

    # corner_angle is the inner angle made by the incoming and
    # outgoing straight measures. We calculate it by taking the
    # supplement of the turn angle
    corner_angle = rai.semicircle - abs(turn)

    match classify_turn(before, point, after):
        case TurnDirection.STRAIGHT:
            # Straight turn
            # TODO print warning here?
            log.debug("Straight.")
            return None

        case TurnDirection.LEFT:
            # Left turn
            log.debug("Left.")

            angle_turn_center = (
                angle_outgoing + angle_incoming + rai.semicircle
                ) / 2

            orientation = Orientation.COUNTERCLOCKWISE

            angle_turn_start = angle_incoming - rai.quartercircle
            angle_turn_end = angle_outgoing - rai.quartercircle

        case TurnDirection.RIGHT:
            # Right turn
            log.debug("Right.")

            angle_turn_center = (
                angle_outgoing + angle_incoming - rai.semicircle
                ) / 2

            orientation = Orientation.CLOCKWISE

            angle_turn_start = angle_incoming + 1 * rai.quartercircle
            angle_turn_end = angle_outgoing + 1 * rai.quartercircle

        case _:
            assert False

    offset_turn_center = radius / math.sin(corner_angle / 2)

    point_turn_center = rai.add(
        point,
        rai.polar(arg=angle_turn_center, mod=offset_turn_center)
        )

    point_enter = rai.add(
        point_turn_center,
        rai.polar(arg=angle_turn_start, mod=radius)
        )

    point_exit = rai.add(
        point_turn_center,
        rai.polar(arg=angle_turn_end, mod=radius)
        )

    return BendSpec(
        angle_start=angle_turn_start,
        angle_end=angle_turn_end,
        radius=radius,
        orientation=orientation,
        point_enter=point_enter,
        point_exit=point_exit,
        point_center=point_turn_center,
        )

class TLTest(rai.Compo):
    """Sample component to play around with the TL class"""
    def _make(self):

        from rai_compos_pub import CPWStraight, CPWBend
        # Note: import inside a function is
        # usually an absolutely insane way of writing Python code.
        # This is just for experimentation purposes tho.

        Straight = CPWStraight.partial(
            signal_width=1,
            gap_width=1,
            gnd_width=1,
            resist_margin=2,
            )

        Bend = CPWBend.partial(
            signal_width=1,
            gap_width=1,
            gnd_width=1,
            resist_margin=2,
            )

        tl = TL()
        tl.straight_compo = Straight
        tl.bend_compo = Bend

        tl.start_at((0, 0))
        tl.straight_to((10, 10))
        tl.straight_to((30, 10))
        tl.straight_to((50, -10))
        tl.straight_to((50, 20))
        tl.straight_to((0, 22))
        tl.straight_to((60, 40))
        tl.straight_to((60, 0))

        tl.build()

        self.subcompos.extend(tl.straights_)
        self.subcompos.extend(tl.bends_)

