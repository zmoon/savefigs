"""
Save all open Matplotlib figures
"""
import inspect
import logging
import math
import os
import sys
import tempfile
import warnings
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Union

import matplotlib.pyplot as plt

__version__ = "0.1.2"

__all__ = ("savefigs",)

_p_tmp = Path(tempfile.gettempdir())

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger(__name__)


# import matplotlib as mpl
# def pickstem(fig: mpl.figure.Figure):
#     """Pick figure name stem."""
#     ...


def _get_ipython_last_ran_file() -> Optional[Path]:
    import IPython

    hist = IPython.core.history.HistoryAccessor(profile="default")

    for t in reversed(list(hist.get_tail(200))):
        cmd = t[2]
        if cmd.startswith("runfile("):
            return Path(cmd.split(", wdir=")[0][9:-1])

    return None


def _caller_is_ipykernel_interactive(fn: str) -> bool:
    p = Path(fn)
    # e.g., `$TEMP/ipykernel_255368/2963069196.py`
    return not fn.startswith("<") and (
        p.parents[0].name.startswith("ipykernel_") and p.parents[1] == _p_tmp
    )


def _caller_is_ipython(fn: str) -> bool:
    # e.g., '<ipython-input-5-9043666a436b>'
    return fn.startswith("<ipython")


# the main function
def savefigs(
    *,
    save_dir: Optional[Union[str, Path, os.PathLike]] = None,
    stem_prefix: Optional[str] = None,
    formats: Optional[Iterable[str]] = None,
    savefig_kwargs: Optional[Dict[str, Any]] = None,
    clobber: bool = True,
    noclobber_method: str = "raise",
    debug: bool = False,
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
    debug
        Whether to print info/debug messages (to stdout).
    """
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)

    if save_dir is None:
        save_dir = Path.cwd()
    else:
        save_dir = Path(save_dir)

    if not save_dir.is_dir():
        raise ValueError("`save_dir` must be a directory that exists")

    if stem_prefix is None:
        stem_prefix = ""

        # Attempt to detect caller file
        caller_frame_info = inspect.stack()[1]
        caller = caller_frame_info.filename
        logger.info(f"caller: {caller!r}")
        if _caller_is_ipykernel_interactive(caller) or _caller_is_ipython(caller):
            logger.info("caller detected as ipy interactive (ipython or ipykernel)")
            p_caller = _get_ipython_last_ran_file()
        elif caller in ["<stdin>", "<string>"]:  # Python REPL or `python -c`
            logger.info("caller is stdin (Python REPL) or string input (`-c`)")
            p_caller = None
        else:
            logger.info("caller detected as not ipy interactive, stdin, nor string")
            p_caller = Path(caller)

        # Use caller filename stem in stem_prefix if it has been found
        if p_caller is not None:
            logger.info(f"caller file: {p_caller.as_posix()!r}")
            stem_prefix = f"{p_caller.stem}_"
        else:
            logger.info("caller file: none (or not detected)")

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
