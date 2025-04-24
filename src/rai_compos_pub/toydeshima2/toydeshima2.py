"""toydeshima2.py: contains ToyDESHIMA2 compo"""

import raimad as rai

from rai_compos_pub import BetterPartial
from rai_compos_pub import tl
from rai_compos_pub import CPWStraight
from rai_compos_pub import CPWBend
from rai_compos_pub import CPWTaperMetal
from rai_compos_pub.toydeshima2.util import get_kid_params
from rai_compos_pub.toydeshima2.leaky_antenna import LeakyAntenna
from rai_compos_pub.toydeshima2.filter import Filter
from rai_compos_pub.toydeshima2.mkid import MKID
from rai_compos_pub.toydeshima2.filterbank import FilterBank
from rai_compos_pub.toydeshima2.microstrip import MSStraight
from rai_compos_pub.toydeshima2.microstrip import MSBend

class Corner(rai.Compo):
    def _make(self, size: float = 100, frac: float = 4):
        self.geoms.update({
            'root': [
                [
                    (0, 0),
                    (size, 0),
                    (size, size / frac),
                    (size / frac, size / frac),
                    (size / frac, size),
                    (0, size),
                    ]
                ]
            })
        self.marks.point = (0, 0)


class BBoxCorners(rai.Compo):
    def _make(
            self,
            bbox: rai.AbstractBBox,
            cornercompo: rai.t.CompoTypeLike,
            ):
        self.subcompos.top_left = (
            cornercompo().proxy()
            .rotate(-rai.quartercircle)
            .marks.point.to(bbox.top_left)
            )
        self.subcompos.top_right = (
            cornercompo().proxy()
            .rotate(rai.semicircle)
            .marks.point.to(bbox.top_right)
            )
        self.subcompos.bot_left = (
            cornercompo().proxy()
            .marks.point.to(bbox.bot_left)
            )
        self.subcompos.bot_right = (
            cornercompo().proxy()
            .rotate(rai.quartercircle)
            .marks.point.to(bbox.bot_right)
            )

class ToyDESHIMA2(rai.Compo):
    r"""
    """
    def _make(self):

        kid_params = get_kid_params()

        bbox = rai.BBox([(0, 0), (6200, 2400)])
        pos_antenna = bbox.interpolate(0.2, 0.5)
        pos_bank = bbox.interpolate(0.5, 0.5)

        corner_compo = Corner.partial(size=100, frac=3)
        corners = BBoxCorners(bbox, corner_compo).proxy()

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
            ).proxy()

        antenna.marks.center.to(pos_antenna)
        bank.marks.thz_enter.to(pos_bank)

        ### THZ line ###

        thz_opts = dict(
            width=0.4
            )

        thz_straight = MSStraight.partial(**thz_opts)
        thz_bend = MSBend.partial(**thz_opts)

        tl_thz = tl.TL(path=(
            tl.StartAt(
                antenna.marks.center,
                straight=thz_straight,
                bend=thz_bend,
                radius=50,
                ),
            tl.StraightTo(
                bbox.interpolate(0.2, 0.2),
                ),
            tl.StraightTo(
                bbox.interpolate(0.4, 0.2),
                ),
            tl.ElbowTo(
                bank.marks.thz_enter,
                ),
            tl.StraightTo(
                bank.marks.thz_exit,
                ),
            # TODO ElbowTo is broken
            ))

        tl_thz.make_specs()
        tl_thz.make_straights()
        tl_thz.make_bends()

        ### Readout CPW ###

        rout_opts = dict(
            signal_width=0.2,
            gap_width=0.2,
            gnd_width=0.4,
            resist_margin=0.2,
            )

        rout_straight = CPWStraight.partial(**rout_opts)
        rout_straight_wide = CPWStraight.partial(
            signal_width=10,
            gap_width=4,
            gnd_width=4,
            resist_margin=4.5,
            )
        rout_bend = CPWBend.partial(**rout_opts)
        rout_taper_in = BetterPartial(CPWTaperMetal,
            l=BetterPartial.Mapped('length'),
            sl=10,
            wl1=4,
            gl1=4,
            sr=rout_opts['signal_width'],
            wr1=rout_opts['gap_width'],
            gr1=rout_opts['gnd_width'],
            )
        rout_taper_out = BetterPartial(CPWTaperMetal,
            l=BetterPartial.Mapped('length'),
            sr=10,
            wr1=4,
            gr1=4,
            sl=rout_opts['signal_width'],
            wl1=rout_opts['gap_width'],
            gl1=rout_opts['gnd_width'],
            )

        fmkids = [
            fmkid
            for name, fmkid in bank.subcompos.items()
            if name.startswith('fmkid')
            ]
        
        tl_rout = tl.TL(path=(
            tl.StartAt(
                bbox.interpolate(0.6, 0.95),
                straight=rout_straight_wide,
                bend=rout_bend,
                radius=1,
                ),
            tl.StraightTo(
                bbox.interpolate(0.6, 0.94),
                straight=rout_taper_in,
                ),
            tl.StraightTo(
                bbox.interpolate(0.6, 0.92),
                straight=rout_straight,
                ),
            tl.StraightTo(
                bbox.interpolate(0.6, 0.9),
                straight=rout_straight,
                ),
            tl.StraightTo(
                bbox.interpolate(0.45, 0.9),
                ),
            tl.StraightTo(
                bbox.interpolate(0.45, 0.8),
                ),
            *(
                tl.ElbowTo(
                    fmkid.marks.readout_connection,
                    )
                for fmkid in fmkids[1::2]
                ),
            # TODO would be great to have relative path points
            tl.ElbowTo(
                bbox.interpolate(0.9, 0.55),
                ),
            tl.ElbowTo(
                bbox.interpolate(0.9, 0.45),
                ),
            *(
                tl.ElbowTo(
                    fmkid.marks.readout_connection,
                    )
                for fmkid in fmkids[0::2][::-1]
                ),
            tl.ElbowTo(
                bbox.interpolate(0.46, 0.3),
                ),
            tl.StraightTo(
                bbox.interpolate(0.46, 0.05),
                straight=rout_taper_out
                ),
            tl.StraightTo(
                bbox.interpolate(0.46, 0.03),
                straight=rout_straight_wide
                ),
            tl.StraightTo(
                bbox.interpolate(0.46, 0.02),
                ),
            ))

        tl_rout.make_specs()
        tl_rout.make_straights()
        tl_rout.make_bends()

        self.subcompos.extend(tl_thz.straights_)
        self.subcompos.extend(tl_thz.bends_)

        self.subcompos.extend(tl_rout.straights_)
        self.subcompos.extend(tl_rout.bends_)

        self.subcompos.antenna = antenna
        self.subcompos.corners = corners
        self.subcompos.bank = bank
