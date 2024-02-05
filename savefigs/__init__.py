"""
Save all open Matplotlib figures
"""

import functools
import inspect
import logging
import math
import os
import sys
import tempfile
import types
import warnings
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Union

import matplotlib.pyplot as plt

__version__ = "0.2.1"

__all__ = ("savefigs", "default_savefig_kwargs")

_P_TMP = Path(tempfile.gettempdir())
"""`Path` for the operating system root temp dir (according to `tempfile.gettempdir()`)."""

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger(__name__)

default_savefig_kwargs = {
    "dpi": 200,
    "transparent": True,
    "bbox_inches": "tight",
    "pad_inches": 0.05,
}


# import matplotlib as mpl
# def pickstem(fig: mpl.figure.Figure):
#     """Pick figure name stem."""
#     ...


def _get_ipython_last_ran_file() -> Optional[Path]:
    from IPython import get_ipython

    # Get current ipython session
    ip = get_ipython()  # will be `None` if no current session
    hm = ip.history_manager
    session_info = hm.get_session_info()
    # ^ tuple: ID, start datetime, end datetime, ...
    logger.debug(f"ipython session info: {session_info!r}")

    # Grab all commands of the session, including last
    hist = list(hm.get_range())

    logger.debug(f"last ipython command: {hist[-1]!r}")
    # ^ Should have `savefigs` in it somewhere
    #   Also end datetime in the session info should be `None`

    if "savefigs(" not in hist[-1][2]:
        logger.debug(
            "`savefigs` appears not to be used in the last command, "
            "skipping history search for last file."
        )
        return None

    # Search backwards in history for the last `runfile` command
    # TODO: also look for `run` or `%run`?
    # TODO: check if the run command actually ran successfully?
    p = None
    for t in reversed(hist):
        # tuple: session ID, command #, command (string)
        cmd = t[2]
        if cmd.startswith("runfile("):
            p = Path(cmd.split(", wdir=")[0][9:-1])

    if p is None:
        logger.info("file not identified in ipython history")
    else:
        logger.info(f"file identified in ipython history: {p.as_posix()!r}")

    return p


def _caller_is_ipykernel_interactive(fn: str) -> bool:
    p = Path(fn)
    # e.g., `$TMP/ipykernel_255368/2963069196.py`
    return not fn.startswith("<") and (
        p.parents[0].name.startswith("ipykernel_") and p.parents[1] == _P_TMP
    )


def _caller_is_ipython(fn: str) -> bool:
    # e.g., '<ipython-input-5-9043666a436b>'
    return fn.startswith("<ipython")


def savefigs(
    *,
    save_dir: Optional[Union[str, Path, os.PathLike]] = None,
    stem_prefix: Optional[str] = None,
    formats: Optional[Iterable[str]] = None,
    savefig_kwargs: Optional[Dict[str, Any]] = None,
    clobber: bool = True,
    noclobber_method: str = "raise",
    debug: bool = False,
    stack_pos: int = 1,
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
        File formats to be used in
        [`Figure.savefig`](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.savefig)'s
        `format` argument.
        For example, `'png'`, `'pdf'`, `'svg'`.
        Default: PNG only (`['png']`).
    savefig_kwargs
        Keyword arguments to
        [`Figure.savefig`](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.savefig),
        in order to override our defaults and those of Matplotlib.
        `format` is ignored if passed.
        Our defaults (`savefigs.default_savefig_kwargs`) are:

            | key           | value     |
            | ------------- | --------- |
            | `dpi`         | `200`     |
            | `transparent` | `True`    |
            | `bbox_inches` | `'tight'` |
            | `pad_inches`  | `0.05`    |

    clobber
        Whether to overwrite existing files.
    noclobber_method : {'raise', 'add_num'}
        What to do when `clobber=False`.
    debug
        Whether to print info/debug messages (to stdout).
    stack_pos
        Stack position to look at when detecting the caller
        to determine what to use for the default `stem_prefix`.
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
        caller_frame_info = inspect.stack()[stack_pos]
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

    # Set savefig kwargs, using the defaults and any inputs
    savefig_kwargs_in = savefig_kwargs if savefig_kwargs is not None else {}
    savefig_kwargs = default_savefig_kwargs.copy()
    savefig_kwargs.update(savefig_kwargs_in)
    logger.info(f"savefig kwargs: {savefig_kwargs}")

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


# Set up as a callable module, so that the more-concise
# `import savefigs; savefigs()`
# can be used, instead of
# `from savefigs import savefigs; savefigs()`
# https://stackoverflow.com/a/48100440


class _CallSavefigs(types.ModuleType):
    @functools.wraps(savefigs)
    def __call__(self, *args, **kwargs):  # module callable
        kwargs["stack_pos"] = kwargs.get("stack_pos", 2)  # new default
        savefigs(*args, **kwargs)


sys.modules[__name__].__class__ = _CallSavefigs
