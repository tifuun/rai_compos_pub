"""
reducers.py -- remove unnecessary TL elements

The purpose of the functions in this module are to remove
unnecessary elements in a TL path.
"""

# UNUSED!!!

# FIXME we hope this becomes a part of raimad.helpers
def are_colinear(*points):
    for prev, point, next_ in pc.iter.triples(points):
        if (
                pc.angle_between(prev, point)
                !=
                pc.angle_between(point, next_)
                ):
            return False
    # FIXME the following TODOs are copy-pasted directly
    # from v0.0.4 code. Need to be fixed.

    # TODO not optimal
    # TODO what if points in wrong order?
    # Definition of colinear?
    return True

def reduce_straights(path):
    """
    reduce_straight -- remove TL nodes that lie on a straight line.

    If a TL has nodes that lie in a straight line -- 
    for example (0, 0), (10, 10), (20, 20) --
    the nodes in the middle can be removed.
    This is the purpose of this function.
    """
    newpath = []
    newpath.append(path[0])

    if len(path) < 3:
        newpath.append(path[1])
        return newpath

    for before, conn, after in pc.iter.triplets(path):
        if isinstance(conn, tl.StraightTo):
            if isinstance(after, tl.StraightTo):
                if are_colinear(before.to, conn.to, after.to):
                    continue

        newpath.append(conn)

    newpath.append(after)
    return newpath

# FIXME tests: reduces more than three colinear nodes in a row?

