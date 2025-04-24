# Public components for RAIMAD

This repository is a staging ground for new RAIMAD components.
You can browse these component on [RAIDEX](https://tifuun.github.io/raidex/)

## Using these components in your own project

You can install this packge from github using pip
in order to make the relevant components available in your Python
environment:

```shell
pip install git+https://github.com/tifuun/rai_compos_pub
```

`rai_compos_pub` will then be available from within Python:

```python
from rai_compos_pub import CPWSegment

my_segment = CPWSegment(.........
```

## Contributing to this package

If you would like to contribute to this project,
you can clone the repository using `git`
and install it in pip editable mode:

```shell
git clone https://github.com/tifuun/rai_compos_pub
pip install -e ./rai_compos_pub
```

This will also make the package available in Python.
But now you can also make changes and add new components
to this package by editing your local code of the repo.

You can then submit your changes using `git`.

Please see the
["collaboration" RAIDOC page](https://tifuun.github.io/raidoc/pages/collaboration.html)
for more information.

## Organisation

If you would like to add a new component,
please put its code in a separate file under `src/rai_compos_pub`.
Make sure to also add an import line in `src/rai_compos_pub/__init__.py`
to make your component available in the root namespace of the package.

## Toy DESHIMA2.0

As a demonstration of RAIMAD features, we have made a
"toy" version of the DESHIMA2.0 spectrometer chip.
All of its components can be found under <src/rai_compos_pub/toydeshima2>.
The toplevel `ToyDESHIMA2` component is in
<src/rai_compos_pub/toydeshima2/toydeshima2.py>.
It can be exported to CIF like this (once you've `pip install -e`'d this repo):
```
raimad export rai_compos_pub.toydeshima2.toydeshima2:ToyDESHIMA2
```

