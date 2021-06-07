"""
Save all open Matplotlib figures.
"""
import inspect
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt


__version__ = "0.1.0"



# def pickstem(fig: mpl.figure.Figure):
#     """Pick figure name stem."""
#     ...


# the main function
def savefigs(
    *, 
    save_dir=None,
    stem_prefix: str = None,
    savefig_kwargs: dict = None,
):
    """Save all open Matplotlib figures.
    
    Parameters
    ----------
    save_dir : path-like
        Directory in which to save the figures.
        Default: current working directory.
    stem_prefix
        Prefix applied to all save figures.
        Default: file stem of the calling file
        (if called from a script, else no stem prefix).
    savefig_kwargs
        Keyword arguments to `matplotlib.figure.Figure.savefig`.
        Some won't be allowed (TBD...).
    """
    
    if save_dir is None:
        save_dir = Path.cwd()

    if stem_prefix is None:
        caller_frame_info = inspect.stack()[1]
        caller_fn = caller_frame_info.filename
        if not caller_fn.startswith("<"):  # '<stdin>', '<ipython ...'>, '<string>'
            stem_prefix = f"{Path(caller_fn).stem}_"
        else:
            stem_prefix = ""

    if savefig_kwargs is None:
        savefig_kwargs = dict(transparent=True, bbox_inches="tight", pad_inches=0.05, dpi=200)

    for num in plt.get_fignums():
        fig = plt.figure(num)
        label = fig.get_label()
        stem_fig = f"fig{fig.number:02d}" if not label else label
        p_stem = save_dir / f"{stem_prefix}{stem_fig}"
        fig.savefig(p_stem.with_suffix(".png"), **savefig_kwargs)
        # if pdf:
        #     fig.savefig(p_stem.with_suffix(".pdf"), **savefig_kwargs)