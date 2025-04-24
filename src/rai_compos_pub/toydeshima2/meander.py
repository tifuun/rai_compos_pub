"""meander.py -- contains Meander compo"""

import raimad as rai

class Meander(rai.Compo):
    """
    Meander helper.

    This will not be necessary once TL class gets meander support.
    """
    def _make(
            self,
            rung_length: float,
            rung_width: float,
            bend_radius: float,
            num_rungs: int,
            straight_compo: rai.t.CompoTypeLike,
            bend_compo: rai.t.CompoTypeLike,
            ):
        pass

