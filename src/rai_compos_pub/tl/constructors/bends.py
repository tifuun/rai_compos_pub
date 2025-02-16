"""tl/constructors/bends.py -- constructor for bends"""

import math
from typing import Iterable

import raimad as rai

from rai_compos_pub import tl

def construct_bends(path, radius, striped=False):
    """given a path, produce bendspecs and new path"""
    newpath = []
    bendspecs = []

    newpath.append(path[0])

    if len(path) < 3:
        newpath.append(path[1])
        return newpath, []

    default_radius = radius

    for before, seg, after in rai.triplets(path):

        #radius = seg.radius or (radius if striped else default_radius)
        # FIXME
        radius = 5

        bendspec = construct_bend(
            before.to, seg.to, after.to, radius)

        if bendspec is None:
            newpath.append(seg)
            continue

        newpath.append(
            tl.StraightTo(
                bendspec.point_enter
                )
            )
        newpath.append(
            tl.JumpTo(
                bendspec.point_exit
                )
            )
        bendspecs.append(bendspec)

    newpath.append(after)
    return newpath, bendspecs

def construct_bend(before, point, after, radius):
    angle_incoming = rai.angle_between(before, point)# % rai.fullcircle
    angle_outgoing = rai.angle_between(point, after)# % rai.fullcircle

    #log.debug(
    #    "New turn, in: %.3f, out: %.3f",
    #    angle_incoming / rai.pi,
    #    angle_outgoing / rai.pi,
    #    )

    turn = angle_outgoing - angle_incoming

    # corner_angle is the inner angle made by the incoming and
    # outgoing straight measures. We calculate it by taking the
    # supplement of the turn angle
    corner_angle = rai.semicircle - abs(turn)

    match tl.classify_turn(before, point, after):
        case tl.TurnDirection.STRAIGHT:
            # Straight turn
            # TODO print warning here?
            #log.debug("Straight.")
            return None

        case tl.TurnDirection.LEFT:
            # Left turn
            #log.debug("Left.")

            angle_turn_center = (
                angle_outgoing + angle_incoming + rai.semicircle
                ) / 2

            orientation = tl.Orientation.COUNTERCLOCKWISE

            angle_turn_start = angle_incoming - rai.quartercircle
            angle_turn_end = angle_outgoing - rai.quartercircle

        case tl.TurnDirection.RIGHT:
            # Right turn
            #log.debug("Right.")

            angle_turn_center = (
                angle_outgoing + angle_incoming - rai.semicircle
                ) / 2

            orientation = tl.Orientation.CLOCKWISE

            angle_turn_start = angle_incoming + rai.quartercircle
            angle_turn_end = angle_outgoing + rai.quartercircle

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

    print("AAA", point_enter, point_exit)

    return tl.BendSpec(
        angle_start=angle_turn_start,
        angle_end=angle_turn_end,
        radius=radius,
        orientation=orientation,
        point_enter=point_enter,
        point_exit=point_exit,
        point_center=point_turn_center,
        )

def make_bend_component(spec: tl.BendSpec, Compo: rai.t.CompoType):
    # FIXME angle start-end to dtheta here or change spec to have?

    dtheta = spec.angle_end - spec.angle_start
    
    return (
        Compo(
            dtheta=dtheta,
            bend_radius=spec.radius,
            )
        .proxy()
        .rotate(spec.angle_start)
        .marks.center.to(spec.point_center)
        )
    #return (
    #    Compo(
    #        angle_start=spec.angle_start,
    #        angle_end=spec.angle_end,
    #        orientation=spec.orientation,
    #        bend_radius=spec.radius,
    #        )
    #    .proxy()
    #    .marks.center.to(spec.point_center)
    #    )

def make_bend_components(
        specs: Iterable[tl.BendSpec],
        Compo: rai.t.CompoType
        ):
    return [
        make_bend_component(spec, Compo)
        for spec in specs
        ]


