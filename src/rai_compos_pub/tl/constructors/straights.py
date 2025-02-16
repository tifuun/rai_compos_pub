import raimad as rai
from typing import Iterable

from rai_compos_pub import tl

def construct_straights(path):

    specs = []

    # FIXME line below not needed?
    straight_compo = path[0].straight
    if straight_compo is None:
        raise Exception("IDK what compo to use!!")

    for seg, after in rai.duplets(path):
        if not isinstance(after, tl.StraightTo):
            continue

        # FIXME before or after isinstance check?
        # TODO propagate or one-off
        if seg.straight is not None:
            straight_compo = seg.straight
            print("CCCC ", seg)

        specs.append(tl.StraightSpec(
            start=seg.to,
            angle=rai.angle_between(seg.to, after.to),
            length=rai.distance_between(seg.to, after.to),
            compo=straight_compo
            ))

    return path, specs

def make_straight_component(spec: tl.StraightSpec):
    return (
        spec.compo(length=spec.length)
        .proxy()
        .marks.tl_enter.to(spec.start)
        .marks.tl_enter.rotate(spec.angle)
        )

def make_straight_components(
        specs: Iterable[tl.StraightSpec],
        ):
    return [
        make_straight_component(spec)
        for spec in specs
        ]


