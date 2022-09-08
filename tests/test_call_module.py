import os
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

import savefigs

mpl.use("Agg")


def test_defaults():
    # Keep consistent with the test in `test_savefigs.py`
    fig = plt.figure()
    savefigs()
    plt.close(fig)

    figs = list(Path().cwd().glob("*.png"))
    assert len(figs) == 1
    assert figs[0].name == "test_savefigs_fig1.png"

    for p_fig in figs:
        os.remove(p_fig)
