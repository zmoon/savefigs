import os
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

from savefigs import savefigs

mpl.use("Agg")


def test_defaults():
    fig = plt.figure()
    savefigs()
    plt.close(fig)

    figs = list(Path().cwd().glob("*.png"))
    try:
        assert len(figs) == 1
        assert figs[0].name == "test_savefigs_fig1.png"
    finally:
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
    assert figs[0].name == "test_savefigs_fig1.png"


def test_bad_save_dir():
    with pytest.raises(ValueError, match="`save_dir` must be a directory that exists"):
        savefigs(save_dir="asdf1234")


def test_stem_prefix(tmpdir):
    save_dir = Path(tmpdir)

    # Create, save, close
    fig = plt.figure()
    savefigs(save_dir=save_dir, stem_prefix="hihi")
    plt.close(fig)

    # Check name
    figs = list(save_dir.glob("*"))
    assert len(figs) == 1
    assert figs[0].name == "hihifig1.png"


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


def test_savefig_kwargs(tmp_path):
    save_dir = tmp_path

    # Create
    fig = plt.figure()

    # Check dropped kws
    for kw in ("format",):
        with pytest.warns(UserWarning, match="savefig kwarg .* dropped"):
            savefigs(save_dir=save_dir, savefig_kwargs={kw: True})

    # Close
    plt.close(fig)


def test_fignum_zfill(tmp_path):
    save_dir = tmp_path

    N = 10
    for _ in range(N):
        plt.figure()

    savefigs(save_dir=save_dir, savefig_kwargs=dict(dpi=10))

    # Check names
    figs = list(save_dir.glob("*"))
    assert sorted(p.name for p in figs) == [
        f"test_savefigs_fig{n:02d}.png" for n in range(1, N + 1)
    ]
