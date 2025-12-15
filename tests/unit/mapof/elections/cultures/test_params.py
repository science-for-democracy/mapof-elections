import pytest

from mapof.elections.cultures.params import get_params_for_paths


def test_get_params_for_paths_extremes_argument_sets_range_endpoints():
    path = {'variable': 'phi'}

    params, variable = get_params_for_paths(path, size=5, j=2, extremes=True)

    assert variable == 'phi'
    assert params['phi'] == pytest.approx(2 / 4)
    assert path['start'] == 0.0


def test_get_params_for_paths_applies_path_extremes_and_scaling():
    path = {'variable': 'alpha', 'extremes': True, 'scale': 0.5, 'start': 0.2}

    params, variable = get_params_for_paths(path, size=4, j=3)

    assert variable == 'alpha'
    assert params['alpha'] == pytest.approx(0.2 + 0.5 * (3 / 3))


def test_get_params_for_paths_step_overrides_progression_and_sets_start():
    path = {'variable': 'beta', 'step': 0.2}

    params, variable = get_params_for_paths(path, size=6, j=3)

    assert variable == 'beta'
    assert params['beta'] == pytest.approx(0 + 3 * 0.2)
    assert path['start'] == 0.0
