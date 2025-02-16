"""tl/segment.py -- TL Segment types"""

from typing import Self, ClassVar

import raimad as rai

# Might be able to include other things in the future
# (Advances?) so best to keep an alias for now
# TODO move to pc.typing?
SegmentTarget = rai.typing.Point

class Segment:
    """
    Segment: a target point and a path type

    Segments are the building block of a TL Path specification.
    Each segment defines a target point,
    and how to get there.
    """
    to: SegmentTarget

    straight: rai.t.CompoType | None
    bend: rai.t.CompoType | None
    radius: float | None
    #do_bridges: bool | None
    #bridge_spacing: float | None
    #bridge_scramble: float | None
    #bridge_length: float | None

    pretty_name: ClassVar[str] = 'Connect to'

    def __init__(
            self,
            to: SegmentTarget,
            straight: rai.t.CompoType | None = None,
            bend: rai.t.CompoType | None = None,
            radius: float | None = None,
            #do_bridges: bool | None = None,
            #bridge_spacing: float | None = None,
            #bridge_scramble: float | None = None,
            #bridge_length: float | None = None,
            #clone_from: Self | None = None,
            ):
        if type(self) is Segment:
            raise Exception("Cannot create abstract Segment")

        #if clone_from is not None:
        #    to = to or clone_from.to
        #    radius = radius or clone_from.radius
        #    do_bridges = do_bridges or clone_from.do_bridges
        #    bridge_spacing = bridge_spacing or clone_from.bridge_spacing
        #    bridge_scramble = bridge_scramble or clone_from.bridge_scramble
        #    bridge_length = bridge_length or clone_from.bridge_length

        self.to = to

        self.straight = straight
        self.bend = bend
        #if isinstance(to, pc.Point):
        #    self.to = to
        #else:
        #    self.to = pc.Point(*to)  # TODO

        self.radius = radius
        #self.do_bridges = do_bridges
        #self.bridge_spacing = bridge_spacing
        #self.bridge_scramble = bridge_scramble
        #self.bridge_length = bridge_length

    def __repr__(self):
        #return f'{self.pretty_name} {self.to}: r={self.radius}'
        return f'{self.pretty_name} {self.to}'

class StartAt(Segment):
    """
    StartAt: the first Segment of a TL Path

    This Segment type specifies a starting point of
    a TL Path, with no path before it.
    """
    pretty_name: ClassVar[str] = 'Start at'

class JumpTo(Segment):
    """JumpTo: discontinuous jump between nodes"""
    pretty_name: ClassVar[str] = 'Jump to'

class StraightTo(Segment):
    """Straight line segment between nodes"""
    pretty_name: ClassVar[str] = 'Straight to'

class ElbowTo(Segment):
    """An elbow with two 90 degree turns connecting two TL Nodes"""
    pretty_name: ClassVar[str] = 'Elbow to'

class MeanderTo(Segment):
    """Meander between two TL nodes"""
    pretty_name: ClassVar[str] = 'Meander to'

    def __init__(*args, **kwargs):
        raise NotImplementedError

