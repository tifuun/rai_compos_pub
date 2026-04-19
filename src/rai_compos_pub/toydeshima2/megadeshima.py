"""megadeshima.py: contain MegaDESHIMA component""" 

import raimad as rai

from rai_compos_pub import RAIText
from rai_compos_pub import BetterPartial
from rai_compos_pub import tl
from rai_compos_pub import CPWStraight
from rai_compos_pub import CPWBend
from rai_compos_pub import CPWTaperMetal
from rai_compos_pub.toydeshima2.util import get_kid_params
from rai_compos_pub.toydeshima2.mesh import Mesh
from rai_compos_pub.toydeshima2.leaky_antenna import LeakyAntenna
from rai_compos_pub.toydeshima2.filter import Filter
from rai_compos_pub.toydeshima2.mkid import MKID
from rai_compos_pub.toydeshima2.filterbank import FilterBank
from rai_compos_pub.toydeshima2.microstrip import MSStraight
from rai_compos_pub.toydeshima2.microstrip import MSBend

class MegaDESHIMA(rai.Compo):
    """
    MegaDESHIMA: A very large nonsense component for use in benchamrking

    This is a variation of the ToyDESHIMA2 component with 4 filterbanks.
    This results in a VERY COMPLEX component that's good
    for benchmarking RAIMAD and hunting down bottlenecks.
    """
    def _make(self):

        kid_params = get_kid_params()


        antenna = LeakyAntenna(
            box_length=115.2,
            box_width=115.2,
            radius=1000,
            butterfly_length=36.0,
            butterfly_width=24.0,
            circle_compo=rai.Circle.partial(num_points=20),
            ).proxy()

        filter_compo = Filter.partial(
            coup_top_w=0.4,
            coup_bot_w=0.4,
            res_w=0.4,
            coup_top_l=2.5,
            coup_bot_l=2,
            short_l=2.3,
            gap=0.5,
            gnd_top_pad=0.3,
            gnd_bot_pad=1,
            gap_w=0.7,
            gap_l=0.7,
            gnd_split=4.7,
            )
        mkid_compo = MKID.partial(
            wl1=1,
            wl2=1,
            wl3=1,
            ltaper=10,

            lfinger1=5,
            lfinger2=7,
            wfinger=0.9,
            wfingers=3.5,
            wcoup=1.5,
            lcoup=4,
            lstub=0.7,
            wstub=0.9,
            lpatch=3,
            wp1=1,
            wp2=1,
            wp3=1.7,
            )
        bank = FilterBank(
            kid_params,
            mkid_spacing=5,
            filter_compo=filter_compo,
            mkid_compo=mkid_compo,
            ).proxy().map({
            'gnd': 'l7',
            'metal': 'l6',
            'leek': 'l5',
            'fingers': 'l14',
            'coup': 'l14',
            'patch': 'l14',
            'text': 'l3',
            })

        bank1 = bank.proxy().hflip()
        bank2 = bank.proxy().rotate(rai.quartercircle)
        bank3 = bank.proxy()
        bank4 = bank.proxy().rotate(-rai.quartercircle)

        bank1.snap_left(antenna)
        bank2.snap_above(antenna)
        bank3.snap_right(antenna)
        bank4.snap_below(antenna)

        fmkids = [
            fmkid
            for thisbank in [bank1, bank2, bank3, bank4]
            for name, fmkid in thisbank.subcompos.items()
            if name.startswith('fmkid')
            ]

        rout_opts = dict(
            signal_width=0.2,
            gap_width=0.2,
            gnd_width=0.4,
            resist_margin=0.2,
            )

        rout_straight = CPWStraight.partial(**rout_opts)
        rout_bend = CPWBend.partial(**rout_opts)

        tl_rout = tl.TL(path=(
            tl.StartAt(
                (-1000, 0),
                straight=rout_straight,
                bend=rout_bend,
                radius=1,
                ),
            *(
                tl.ElbowTo(
                    fmkid.marks.readout_connection,
                    )
                for fmkid in fmkids[1::2]
                ),
            *(
                tl.ElbowTo(
                    fmkid.marks.readout_connection,
                    )
                for fmkid in fmkids[0::2][::-1]
                ),
            ))

        tl_rout.make_specs()
        tl_rout.make_straights()
        tl_rout.make_bends()

        lmap_cpw = {
            'root': 'l1',
            'conductor': 'l1',
            'resist': None
            }

        for straight in tl_rout.straights_:
            self.subcompos.append(straight.map(lmap_cpw))
        for bend in tl_rout.bends_:
            self.subcompos.append(bend.map(lmap_cpw))

        thz_opts = dict(
            width=0.4
            )

        thz_straight = MSStraight.partial(**thz_opts)
        thz_bend = MSBend.partial(**thz_opts)

        lmap_ms = 'l5'
        for thisbank in [bank1, bank2, bank3, bank4]:
            tl_thz = tl.TL(path=(
                tl.StartAt(
                    antenna.marks.center,
                    straight=thz_straight,
                    bend=thz_bend,
                    radius=50,
                    ),
                tl.ElbowTo(
                    thisbank.marks.thz_enter,
                    ),
                tl.StraightTo(
                    thisbank.marks.thz_exit,
                    ),
                ))

            tl_thz.make_specs()
            tl_thz.make_straights()
            tl_thz.make_bends()

            for straight in tl_thz.straights_:
                self.subcompos.append(straight.map(lmap_ms))
            for bend in tl_thz.bends_:
                self.subcompos.append(bend.map(lmap_ms))


        self.subcompos.bank1 = bank1
        self.subcompos.bank2 = bank2
        self.subcompos.bank3 = bank3
        self.subcompos.bank4 = bank4
        self.subcompos.antenna = antenna.map({
            'diel': 'l0',
            'gnd': 'l7',
            'conductor': 'l14',
            })

