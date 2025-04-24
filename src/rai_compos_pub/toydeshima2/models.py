"""models.py -- dataclasses for toydeshima2"""

from dataclasses import dataclass

@dataclass
class FilterMKIDSpec:
    """Details for building a filter+mkid."""
    id: int
    kind: str
    f_kid_design_ghz: float
    f_filter_design_ghz: float
    kid_qc: float
    l_al_mm: float
    l_wide_mm: float
    l_thz_um: float
    l_coup_um: float
