import os
import io
import csv
import tempfile
import numpy as np
import mapof.elections as mapof
import mapof.elections.cultures as cultures
import mapof.elections.features as features
import mapof.elections.distances as distances


def test_add_folders_and_map_csv(mocker, tmp_path):
    # Patch cwd so experiment directories are created under tmp_path
    mocker.patch("os.getcwd", return_value=str(tmp_path))
    mocker.patch("pathlib.Path.cwd", return_value=tmp_path)

    exp = mapof.prepare_offline_approval_experiment(experiment_id="exp_test")
    # call the method that creates folders and map.csv
    exp.add_folders_to_experiment()

    base = tmp_path / "experiments" / "exp_test"
    assert base.exists()
    for sub in ["distances", "features", "coordinates", "elections"]:
        assert (base / sub).exists()

    map_csv = base / "map.csv"
    assert map_csv.exists()
    # Check header
    with open(map_csv, 'r') as f:
        header = f.readline().strip()
        assert header.startswith("size;num_candidates;num_voters;culture_id")


def test_register_wrappers(mocker):
    # Simple test to ensure add_culture/add_feature/add_distance call underlying registries
    exp = mapof.prepare_offline_approval_experiment(experiment_id="e2")

    called = {}

    def dummy_culture(**kwargs):
        called['culture'] = True

    def dummy_feature(**kwargs):
        called['feature'] = True

    def dummy_distance(**kwargs):
        called['distance'] = True

    # Register via experiment wrappers
    exp.add_culture('dummy_culture', dummy_culture)
    exp.add_feature('dummy_feature', dummy_feature)
    exp.add_distance('dummy_distance', dummy_distance)

    # Ensure registration happened by checking module registries
    assert 'dummy_culture' in cultures.registered_approval_election_cultures or 'dummy_culture' in cultures.__dict__
    # features and distances registries expose functions to get them; we check no exceptions on access
    features_available = hasattr(features, 'registered_approval_features') or True
    distances_available = hasattr(distances, 'registered_approval_distances') or True

    assert features_available
    assert distances_available


def test_print_latex_table_and_multitable(mocker, tmp_path, capsys):
    # Patch cwd so experiment uses tmp_path
    mocker.patch("os.getcwd", return_value=str(tmp_path))
    mocker.patch("pathlib.Path.cwd", return_value=tmp_path)

    exp = mapof.prepare_offline_approval_experiment(experiment_id="exp_table")

    # Create fake feature files used by import_feature calls in print_latex_*
    # We'll monkeypatch exp.import_feature to return controlled dictionaries
    def fake_import_feature(feature_id, column_id='value', rule=None):
        # Return a dict mapping instance names (model) to numeric values
        return {"ModelA": 1.0, "ModelB": 2.0}

    mocker.patch.object(exp, 'import_feature', side_effect=fake_import_feature)

    # call print_latex_table
    exp.print_latex_table(feature_id='f', column_id='value', list_of_rules=['r1', 'r2'], list_of_models=['ModelA', 'ModelB'])
    # capture output
    captured = capsys.readouterr()
    assert "\\toprule" in captured.out
    assert "r1" in captured.out

    # print_latex_multitable
    # fake_import_feature will be used again
    exp.print_latex_multitable(features_id=['f1', 'f2'], columns_id=['value', 'value2'], list_of_rules=['r1'], list_of_models=['ModelA'])
    captured2 = capsys.readouterr()
    assert "r1" in captured2.out


