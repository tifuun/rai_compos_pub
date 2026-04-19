"""
tl/specs.py -- specs for TL parts

To allow more customization in the transmission line
creating process,
the TL class does not immediately create components that
make up the transmission line.
It first generates specs for straights, bends, and bridges.
Specs are just dataclasses that hold all the relevant information
for creating the components.
The user can edit the generated specs before they are used
to create components.
This can allow for things like not generating
bridges around areas where the transmission line
couples with other devices
"""

from dataclasses import dataclass

import raimad as rai

from rai_compos_pub import tl

@dataclass
class BendSpec:
    theta1: float
    dtheta: float
    radius: float
    point_enter: rai.types.Vec2
    point_exit: rai.types.Vec2
    point_center: rai.types.Vec2

    compo: rai.t.CompoType

@dataclass
class StraightSpec:
    start: rai.types.Vec2
    angle: float
    length: float

    compo: rai.t.CompoType

## UNUSED ##
@dataclass
class BridgeSpec:
    start: rai.types.Vec2
    angle: float
    length: float

    compo: rai.t.CompoType

