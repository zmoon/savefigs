# savefigs

[![CI workflow status](https://github.com/zmoon/savefigs/actions/workflows/ci.yml/badge.svg)](https://github.com/zmoon/savefigs/actions/workflows/ci.yml)
[![Version on PyPI](https://img.shields.io/pypi/v/savefigs.svg)](https://pypi.org/project/savefigs/)

The goal is to make it easy to save all open Matplotlib figures, with names that are useful.

## Usage

Assume we have a script `some_script.py` that creates multiple Matplotlib figures.

Import the `savefigs` function:
```python
from savefigs import savefigs
```

The below examples assume the figures do not have a label (`fig.get_label()`, set using the `num` argument to `plt.figure()`).
If a figure does have a label, it will be used in place of `fig{N}`.

Default save settings:
```python
savefigs()
# ./some_script_fig1.png, ./some_script_fig2.png, ...
```

Specify directory:
```python
savefigs(save_dir="figs")  # must exist
# ./figs/some_script_fig1.png, ./figs/some_script_fig2.png, ...
```

Specify a prefix to the base stem format:
```python
savefigs(stem_prefix="run1")
# ./run1_fig1.png, ./run1_fig2.png, ...
```

Save in multiple file formats:
```python
savefigs(formats=["png", "pdf"])
# ./some_script_fig1.png, ./some_script_fig1.pdf, ...
```

Avoid overwriting files:
```python
savefigs(clobber=False, clobber_method="add_num")
```
