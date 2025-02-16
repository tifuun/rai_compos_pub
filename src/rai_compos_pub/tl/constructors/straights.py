import raimad as rai
from typing import Iterable

from rai_compos_pub import tl

def construct_straights(path):
    specs = []
    for seg, after in rai.duplets(path):
        if not isinstance(after, tl.StraightTo):
            continue

        specs.append(tl.StraightSpec(
            start=seg.to,
            angle=rai.angle_between(seg.to, after.to),
            length=rai.distance_between(seg.to, after.to)
            ))

    return path, specs

def make_straight_component(spec: tl.StraightSpec, Compo: rai.t.CompoType):
    return (
        Compo(length=spec.length)
        .proxy()
        .marks.tl_enter.to(spec.start)
        .marks.tl_enter.rotate(spec.angle)
        )

def make_straight_components(
        specs: Iterable[tl.StraightSpec],
        Compo: rai.t.CompoType,
        ):
    return [
        make_straight_component(spec, Compo)
        for spec in specs
        ]


