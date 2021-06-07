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


# cla as plt.close("all") alias?


# the main function
def savefigs(
    *, 
    save_dir=None,
    stem_prefix: str = None,
    savefig_kwargs: dict = None,
    clobber: bool = True,
    noclobber_method: str = "raise",
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
    clobber
        Whether to overwrite existing files.
    noclobber_method : {'raise', 'add_num'}
        What to do when `clobber=False`.
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

    # Loop over open figures
    for num in plt.get_fignums():
        fig = plt.figure(num)
        
        label = fig.get_label()
        stem_fig = f"fig{fig.number:02d}" if not label else label
        stem = f"{stem_prefix}{stem_fig}"
        p_stem = save_dir / stem

        p = p_stem.with_suffix(".png")
        if p.is_file() and not clobber:
            if noclobber_method == "raise":
                raise Exception(f"file path {p.as_posix()} already exists")
            elif noclobber_method == "add_num":
                n = 2
                while p.is_file():
                    p = (save_dir / f"{stem}_{n}").with_suffix(".png")
            else:
                raise ValueError("invalid `noclobber_method`")

        fig.savefig(p, **savefig_kwargs)
        # if pdf:
        #     fig.savefig(p_stem.with_suffix(".pdf"), **savefig_kwargs)