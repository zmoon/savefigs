"""
Save all open Matplotlib figures
"""
import inspect
import math
import os
import warnings
from pathlib import Path
from typing import Iterable, Optional, Union

import matplotlib.pyplot as plt

__version__ = "0.1.0"

__all__ = ("savefigs",)


# import matplotlib as mpl
# def pickstem(fig: mpl.figure.Figure):
#     """Pick figure name stem."""
#     ...


# the main function
def savefigs(
    *,
    save_dir: Optional[Union[str, Path, os.PathLike]] = None,
    stem_prefix: Optional[str] = None,
    formats: Optional[Iterable[str]] = None,
    savefig_kwargs: Optional[dict] = None,
    clobber: bool = True,
    noclobber_method: str = "raise",
) -> None:
    """Save all open Matplotlib figures.

    Parameters
    ----------
    save_dir
        Directory in which to save the figures (must exist).
        Default: current working directory.
    stem_prefix
        Prefix applied to all save figures.
        Default: file stem of the calling file
        (if called from a script, else no stem prefix).
    formats
        File formats to be used in `Figure.savefig`'s `format` argument.
        For example, `'png'`, `'pdf'`, `'svg'`.
        Default: PNG only `['png']`.
    savefig_kwargs
        Keyword arguments to `matplotlib.figure.Figure.savefig`.
        Some won't be allowed (TBD...).
    clobber
        Whether to overwrite existing files.
    noclobber_method : {'raise', 'add_num'}
        What to do when `clobber=False`.
    """

    if save_dir is None:
        save_dir = Path.cwd()
    else:
        save_dir = Path(save_dir)

    if not save_dir.is_dir():
        raise ValueError("`save_dir` must be a directory that exists")

    if stem_prefix is None:
        caller_frame_info = inspect.stack()[1]
        caller_fn = caller_frame_info.filename
        if not caller_fn.startswith("<"):  # '<stdin>', '<ipython ...'>, '<string>'
            stem_prefix = f"{Path(caller_fn).stem}_"
        else:
            stem_prefix = ""

    if formats is None:
        formats = ["png"]

    if savefig_kwargs is None:
        savefig_kwargs = dict(transparent=True, bbox_inches="tight", pad_inches=0.05, dpi=200)

    for kw in ("format",):
        if kw in savefig_kwargs:
            savefig_kwargs.pop(kw)
            warnings.warn(f"savefig kwarg `{kw}` dropped")

    # Loop over open figures
    fignums = plt.get_fignums()
    n_figs = len(fignums)
    nd = int(math.log10(n_figs)) + 1 if n_figs else 0
    for num in fignums:
        fig = plt.figure(num)

        label = fig.get_label()  # TODO: also try `fig.canvas.manager.get_window_title`?
        s_num = str(num).zfill(nd)
        stem_fig = f"fig{s_num}" if not label else label
        stem = f"{stem_prefix}{stem_fig}"
        p_stem = save_dir / stem

        for format in formats:

            ext = f".{format}"
            p = p_stem.with_suffix(ext)
            if p.is_file() and not clobber:
                if noclobber_method == "raise":
                    raise Exception(f"file path {p.as_posix()} already exists")
                elif noclobber_method == "add_num":
                    n = 1  # there is already one
                    while p.is_file():
                        n += 1
                        p = (save_dir / f"{stem}_{n}").with_suffix(ext)
                else:
                    raise ValueError("invalid `noclobber_method`")

            fig.savefig(p, **savefig_kwargs)

    # TODO: Return paths?
