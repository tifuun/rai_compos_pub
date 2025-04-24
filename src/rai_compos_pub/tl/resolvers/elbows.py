"""resolvers/elbows.py -- reduce TL.elbow_to() into straights and turns"""

import raimad as rai

from rai_compos_pub import tl

def resolve_elbows(path):
    """
    Given a TL path, replace ElbowTo segments with
    straights and turns
    """
    newpath = list(path[0:1])  # FIXME typing list vs tuple
    for before_seg, seg in rai.duplets(path):
        if isinstance(seg, tl.ElbowTo):
            newpath.extend(
                resolve_elbow(
                    before_seg.to,
                    seg,
                    ),
                )
        else:
            newpath.append(seg)

    return newpath


def resolve_elbow(before: rai.t.Point, elbow: tl.ElbowTo):
    if before[0] == elbow.to[0] or before[1] == elbow.to[1]:
        return [
            tl.StraightTo(elbow.to),
            ]

    mid = rai.midpoint(before, elbow.to)
    p1 = (mid[0], before[1])
    p2 = (mid[0], elbow.to[1])
    return [
        tl.StraightTo(p1),#, clone_from=elbow),
        tl.StraightTo(p2),#, clone_from=elbow),
        tl.StraightTo(elbow.to)#, clone_from=elbow),
        ]

