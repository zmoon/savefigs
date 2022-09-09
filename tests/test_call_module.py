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
    try:
        assert len(figs) == 1
        assert figs[0].name == "test_call_module_fig1.png"
    finally:
        for p_fig in figs:
            os.remove(p_fig)
