"""util.py: utilities for toydeshima2"""

import csv
import importlib.resources
from dataclasses import fields

from rai_compos_pub.toydeshima2 import res
from rai_compos_pub.toydeshima2.models import FilterMKIDSpec

def autoconvert_dataclass(datacls, row):
    """
    Create dataclass from CSV row with automatic type conversion.

    Only works for dataclasses where the type annotations
    are simple types. Won't work for unions, etc.
    Use Pandas or Pydantic if you need more advanced deatures.
    """
    return datacls(*(
        fld.type(value)
        for fld, value in
        zip(fields(datacls), row, strict=True)
        ))

def yield_csv(name, skip_header = True, **kwargs):
    with importlib.resources.open_text(res, name) as csvfile:
        reader = csv.reader(csvfile, **kwargs)
        if skip_header:
            next(reader)
        yield from reader

def yield_kid_params():
    for row in yield_csv("kid_params.csv"):
        yield autoconvert_dataclass(FilterMKIDSpec, row)

def get_kid_params():
    return list(yield_kid_params())

if __name__ == '__main__':
    print('\n'.join(map(str, get_kid_params())))

