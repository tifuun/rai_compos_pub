"""filtermkid.py -- contains FilterMKID component for toydeshima2"""

import raimad as rai

from rai_compos_pub.toydeshima2.models import FilterMKIDSpec
from rai_compos_pub.toydeshima2.mkid import MKID
from rai_compos_pub.toydeshima2.filter import Filter

class FilterMKID(rai.Compo):
    def _make(
            self,
            spec: FilterMKIDSpec,
            filter_compo: rai.t.CompoTypeLike = Filter,
            mkid_compo: rai.t.CompoTypeLike = MKID,
            ):

        filt = filter_compo(
            res_l = spec.l_coup_um * 1e-1,
            ).proxy().hflip()
        mkid = mkid_compo(
            l1=spec.l_al_mm * 1e2,
            l2=spec.l_wide_mm * 1e2,
            ).proxy()

        mkid.marks.filter_connection.to(
            filt.marks.mkid_connection)

        self.subcompos.filt = filt
        self.subcompos.mkid = mkid

        self.marks.thz_connection = filt.marks.thz_connection
        self.marks.readout_connection = mkid.marks.readout_connection

