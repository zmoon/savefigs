from pathlib import Path

import savefigs

HERE = Path(__file__).parent


def test_save_script_figs(tmp_path):
    save_dir = tmp_path / "asdf1234461436"
    save_dir.mkdir()
    savefigs.save_script_figs(HERE / "sample_script.py", save_dir=save_dir)
    figs = list(save_dir.glob("*.png"))
    assert len(figs) == 1
    assert figs[0].name == "sample_script_fig1.png"
