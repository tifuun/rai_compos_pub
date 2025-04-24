"""filterbank.py: contains FilterBank component for toydeshima2"""

from collections.abc import Sequence

import raimad as rai

from rai_compos_pub.toydeshima2.filtermkid import FilterMKID
from rai_compos_pub.toydeshima2.models import FilterMKIDSpec
from rai_compos_pub.toydeshima2.mkid import MKID
from rai_compos_pub.toydeshima2.filter import Filter

class FilterBank(rai.Compo):
    def _make(
            self,
            specs: Sequence[FilterMKIDSpec] | None = None,
            filter_compo: rai.t.CompoTypeLike = Filter,
            mkid_compo: rai.t.CompoTypeLike = MKID,
            mkid_spacing: float = 100,
            ):

        if specs is None:
            specs = (
                FilterMKIDSpec(
                    id=0,
                    kind='filter',
                    f_kid_design_ghz=0,
                    f_filter_design_ghz=0,
                    kid_qc=0,
                    l_al_mm=1,
                    l_wide_mm=1.2,
                    l_thz_um=10,
                    l_coup_um=10,
                    ),
                )

        for i, spec in enumerate(specs):
            if spec.kind != 'filter':
                continue

            fmkid = FilterMKID(spec, filter_compo, mkid_compo).proxy()
            if i % 2 == 0:
                fmkid.hflip()
            fmkid.marks.thz_connection.to((i * mkid_spacing, 0))

            self.subcompos[f'fmkid_{spec.id}'] = fmkid
            # TODO explain this method of adding subcompos in raidoc?
            # It's a bit hidden right now in the dictlist doc

        self.marks.thz_enter = (0, 0)
        self.marks.thz_exit = (mkid_spacing * len(specs), 0)



