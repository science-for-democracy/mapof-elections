import os
from pathlib import Path

import mapof.elections.objects.Microscope as microscope_module
from mapof.elections.objects.Microscope import Microscope


class DummyFigure:
    """Simple stand-in for a matplotlib figure used by Microscope tests."""

    def __init__(self):
        self.saved_paths = []
        self.shown = False

    def savefig(self, path, **kwargs):
        # Simulate matplotlib by creating the output file.
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("dummy image content")
        self.saved_paths.append((path, kwargs))

    def show(self):
        self.shown = True


def test_microscope_defaults_when_identifiers_missing():
    scope = Microscope(DummyFigure(), object(), experiment_id=None, label=None, object_type='vote')

    assert scope.experiment_id == 'online'
    assert scope.label == 'noname'
    assert scope.object_type == 'vote'


def test_save_to_file_creates_directory_and_sanitizes_filename(monkeypatch, tmp_path):
    monkeypatch.setattr(microscope_module.os, "getcwd", lambda: str(tmp_path))
    fig = DummyFigure()
    scope = Microscope(fig, object(), experiment_id="exp42", label="demo", object_type='candidate')

    raw_name = f"nested{os.sep}name"
    saved_path = scope.save_to_file(saveas=raw_name)

    expected_dir = tmp_path / "images" / "exp42"
    assert saved_path.startswith(str(expected_dir))
    assert Path(saved_path).exists()
    # Path separators in the provided name should be replaced with underscores
    assert os.sep not in Path(saved_path).stem
    assert Path(saved_path).stem == "nested_name"
    assert fig.saved_paths[0][0] == saved_path


def test_show_and_save_invokes_show_before_saving(monkeypatch, tmp_path):
    monkeypatch.setattr(microscope_module.os, "getcwd", lambda: str(tmp_path))
    fig = DummyFigure()
    scope = Microscope(fig, object(), experiment_id="exp-online", label="sample", object_type='vote')

    saved_path = scope.show_and_save(saveas="result")

    assert fig.shown, "show() should be executed before saving"
    assert Path(saved_path).exists()
    assert saved_path == fig.saved_paths[0][0]
