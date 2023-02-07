# savefigs

Easily save all open Matplotlib figures, with useful filenames.

[![CI workflow status](https://github.com/zmoon/savefigs/actions/workflows/ci.yml/badge.svg)](https://github.com/zmoon/savefigs/actions/workflows/ci.yml)
[![Version on PyPI](https://img.shields.io/pypi/v/savefigs.svg)](https://pypi.org/project/savefigs/)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

## Usage

*Assume we have a script `some_script.py` that creates multiple Matplotlib figures.*

Import the `savefigs` function:
```python
from savefigs import savefigs
```

The below examples assume the figures do not have labels (`fig.get_label()`).
If a figure does have a label, it will be used in place of `fig{num}`.

Default save settings (`./{script filename stem}{figure label or fig{num}}.png`):
```python
savefigs()
# ./some_script_fig1.png, ./some_script_fig2.png, ...
```
👆 The filenames tell us which script generated the figures as well as their relative places in the figure generation order (or labels if they are labeled).

Specify directory:
```python
savefigs(save_dir="figs")  # must exist
# ./figs/some_script_fig1.png, ./figs/some_script_fig2.png, ...
```

Specify a different prefix to the base stem format:
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
savefigs(clobber=False, noclobber_method="add_num")
# ./some_script_fig3.png (assuming ./some_script_fig{1,2}.png already exist)
```
👆 By default (without changing `noclobber_method`), setting `clobber=False` will instead error.

## Background

When writing a script that creates multiple figures, I usually label them (usually using the `num` argument to `plt.figure()`/`plt.subplots()`), which makes it easier to find the correct figure window. Then, at the end of the script I write a loop like:
```python
for num in plt.get_fignums():
    fig = plt.figure(num)
    fig.savefig(f"{fig.get_label()}.pdf", ...)
    # Maybe another format...
```
`savefigs()` essentially does this, but is more robust and provides additional features through keyword arguments. And it saves having to write those lines in the script, instead allowing the simple one-liner:
```python
from savefigs import savefigs; savefigs()
```
