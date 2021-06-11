import os
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

from savefigs import __version__, savefigs


def test_version():
    assert __version__ == "0.1.0"


def test_defaults():
    fig = plt.figure()
    savefigs()
    plt.close(fig)

    figs = list(Path().cwd().glob("*.png"))
    assert len(figs) == 1
    assert figs[0].name == "test_savefigs_fig01.png"

    for p_fig in figs:
        os.remove(p_fig)


def test_save_dir(tmpdir):
    save_dir = Path(tmpdir)

    # Create, save, close
    fig = plt.figure()
    savefigs(save_dir=save_dir)
    plt.close(fig)

    # Check name
    figs = list(save_dir.glob("*"))
    assert len(figs) == 1
    assert figs[0].name == "test_savefigs_fig01.png"


def test_stem_prefix(tmpdir):
    save_dir = Path(tmpdir)

    # Create, save, close
    fig = plt.figure()
    savefigs(save_dir=save_dir, stem_prefix="hihi")
    plt.close(fig)

    # Check name
    figs = list(save_dir.glob("*"))
    assert len(figs) == 1
    assert figs[0].name == "hihifig01.png"


def test_clobber(tmpdir):
    save_dir = Path(tmpdir)

    # Save but don't close yet
    fig = plt.figure()
    savefigs(save_dir=save_dir)
    figs = list(save_dir.glob("*"))
    assert len(figs) == 1

    # Save again
    savefigs(save_dir=save_dir)
    figs = list(save_dir.glob("*"))
    assert len(figs) == 1, "first saved fig should be clobbered"

    # Now close
    plt.close(fig)


def test_noclobber(tmpdir):
    save_dir = Path(tmpdir)

    # Save but don't close yet
    fig = plt.figure()
    savefigs(save_dir=save_dir)
    figs = list(save_dir.glob("*"))
    assert len(figs) == 1

    # noclobber - raise
    with pytest.raises(Exception, match="file path .* already exists"):
        savefigs(save_dir=save_dir, clobber=False)

    # noclobber - add num to the end of the stem
    savefigs(save_dir=save_dir, clobber=False, noclobber_method="add_num")
    figs = sorted(save_dir.glob("*"))
    assert len(figs) == 2
    assert figs[-1].stem[-1] == "2"

    with pytest.raises(ValueError, match="invalid `noclobber_method`"):
        savefigs(save_dir=save_dir, clobber=False, noclobber_method="asdf")
    
    # Now close
    plt.close(fig)


def test_fig_with_label(tmpdir):
    save_dir = Path(tmpdir)

    # Create, save, close
    label = "The best figure"
    fig = plt.figure(num=label)
    assert fig.get_label() == label
    savefigs(save_dir=save_dir, stem_prefix="")
    plt.close(fig)

    # Check name
    figs = list(save_dir.glob("*"))
    assert len(figs) == 1
    assert figs[0].name == "The best figure.png"


def test_formats(tmp_path):
    save_dir = tmp_path

    # Create, save, close
    fig = plt.figure()
    formats = ["png", "pdf", "svg"]
    savefigs(save_dir=save_dir, formats=formats)
    plt.close(fig)

    # Check names
    figs = list(save_dir.glob("*"))
    assert len(figs) == len(formats)
    assert {p.suffix[1:] for p in figs} == set(formats)
