from pathlib import Path

import matplotlib.pyplot as plt

from savefigs import __version__, savefigs


def test_version():
    assert __version__ == "0.1.0"


def test_save_dir(tmpdir):
    save_dir = Path(tmpdir)

    # Create and save
    fig = plt.figure()
    savefigs(save_dir=save_dir)
    plt.close(fig)

    # Check name
    figs = list(save_dir.glob("*"))
    assert len(figs) == 1
    assert figs[0].name == "test_savefigs_fig01.png"


def test_stem_prefix(tmpdir):
    save_dir = Path(tmpdir)

    # Create and save
    fig = plt.figure()
    savefigs(save_dir=save_dir, stem_prefix="hihi")
    plt.close(fig)

    # Check name
    figs = list(save_dir.glob("*"))
    assert len(figs) == 1
    assert figs[0].name == "hihifig01.png"
