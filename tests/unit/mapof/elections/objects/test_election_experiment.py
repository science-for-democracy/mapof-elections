import importlib
import os
import sys
import types
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _new_package(name: str) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__path__ = []
    return module


def _install_test_stubs():
    import mapof  # noqa: F401  # ensure namespace package is loaded

    for mod in [m for m in sys.modules if m.startswith("mapof.core") or m.startswith("sklearn")]:
        sys.modules.pop(mod, None)

    sklearn_mod = _new_package("sklearn")
    sys.modules["sklearn"] = sklearn_mod
    decomposition_mod = types.ModuleType("sklearn.decomposition")

    class _DummyPCA:
        def __init__(self, *_, **__):
            pass

        def fit_transform(self, data):
            return data

    decomposition_mod.PCA = _DummyPCA
    sys.modules["sklearn.decomposition"] = decomposition_mod
    sklearn_mod.decomposition = decomposition_mod

    manifold_mod = types.ModuleType("sklearn.manifold")

    class _DummyManifold:
        def __init__(self, *_, **__):
            pass

        def fit_transform(self, data):
            return data

    manifold_mod.MDS = _DummyManifold
    manifold_mod.TSNE = _DummyManifold
    manifold_mod.SpectralEmbedding = _DummyManifold
    manifold_mod.LocallyLinearEmbedding = _DummyManifold
    manifold_mod.Isomap = _DummyManifold
    sys.modules["sklearn.manifold"] = manifold_mod
    sklearn_mod.manifold = manifold_mod

    core_pkg = _new_package("mapof.core")
    sys.modules["mapof.core"] = core_pkg

    persistence_pkg = _new_package("mapof.core.persistence")
    sys.modules["mapof.core.persistence"] = persistence_pkg
    core_pkg.persistence = persistence_pkg
    exports_mod = types.ModuleType("mapof.core.persistence.experiment_exports")

    def _export_feature_to_file(*_, **__):
        return None

    exports_mod.export_feature_to_file = _export_feature_to_file
    sys.modules["mapof.core.persistence.experiment_exports"] = exports_mod
    persistence_pkg.experiment_exports = exports_mod

    printing_mod = types.ModuleType("mapof.core.printing")
    printing_mod.print_matrix = lambda *_, **__: None
    sys.modules["mapof.core.printing"] = printing_mod
    core_pkg.printing = printing_mod

    matchings_mod = types.ModuleType("mapof.core.matchings")
    matchings_mod.solve_matching_vectors = lambda cost_table: (0, list(range(len(cost_table))))
    matchings_mod.solve_matching_matrices = lambda *_, **__: 0
    sys.modules["mapof.core.matchings"] = matchings_mod

    features_pkg = _new_package("mapof.core.features")
    sys.modules["mapof.core.features"] = features_pkg
    register_mod = types.ModuleType("mapof.core.features.register")
    register_mod.registered_experiment_features = {}
    register_mod.features_embedding_related = set()
    sys.modules["mapof.core.features.register"] = register_mod
    features_pkg.register = register_mod

    mallows_mod = types.ModuleType("mapof.core.features.mallows")
    mallows_mod.phi_from_normphi = lambda *_args, **kwargs: float(kwargs.get('normphi', 0))
    sys.modules["mapof.core.features.mallows"] = mallows_mod
    features_pkg.mallows = mallows_mod

    utils_mod = types.ModuleType("mapof.core.utils")

    def _get_instance_id(single: bool, family_id: str, idx: int):
        return family_id if single else f"{family_id}_{idx}"

    def _make_folder_if_do_not_exist(path: str):
        os.makedirs(path, exist_ok=True)

    utils_mod.get_instance_id = _get_instance_id
    utils_mod.make_folder_if_do_not_exist = _make_folder_if_do_not_exist
    sys.modules["mapof.core.utils"] = utils_mod

    distances_mod = types.ModuleType("mapof.core.distances")
    distances_mod.swap_distance_between_potes = lambda *_, **__: 0
    distances_mod.spearman_distance_between_potes = lambda *_, **__: 0
    distances_mod.swap_distance = lambda *_, **__: (0, None)
    distances_mod.map_str_to_func = lambda *_: lambda *a, **k: 0
    distances_mod.l2 = lambda *_, **__: 0
    distances_mod.hamming = lambda *_, **__: 0
    sys.modules["mapof.core.distances"] = distances_mod

    objects_pkg = _new_package("mapof.core.objects")
    sys.modules["mapof.core.objects"] = objects_pkg

    experiment_mod = types.ModuleType("mapof.core.objects.Experiment")

    class _BaseExperiment:
        def __init__(self, **kwargs):
            self.instances = kwargs.get('instances') or {}
            self.families = kwargs.get('families')
            self.num_instances = kwargs.get('num_instances', 0)
            self.num_families = kwargs.get('num_families', 0)
            self.num_elections = kwargs.get('num_elections', 0)
            self.experiment_id = kwargs.get('experiment_id', 'exp')
            self.instance_type = kwargs.get('instance_type', 'ordinal')
            self.is_exported = kwargs.get('is_exported', False)
            self.fast_import = kwargs.get('fast_import', False)
            self.with_matrix = kwargs.get('with_matrix', False)
            self.features = {}
            self.embedding_id = kwargs.get('embedding_id', 'embedding')
            self.election_sizes = set()

    experiment_mod.Experiment = _BaseExperiment
    sys.modules["mapof.core.objects.Experiment"] = experiment_mod
    objects_pkg.Experiment = _BaseExperiment

    instance_mod = types.ModuleType("mapof.core.objects.Instance")

    class _BaseInstance:
        def __init__(self, *_, **__):
            pass

    instance_mod.Instance = _BaseInstance
    sys.modules["mapof.core.objects.Instance"] = instance_mod
    objects_pkg.Instance = _BaseInstance

    family_mod = types.ModuleType("mapof.core.objects.Family")

    class _BaseFamily:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
            self.size = kwargs.get('size', 0)
            self.instance_ids = kwargs.get('instance_ids', [])

    family_mod.Family = _BaseFamily
    sys.modules["mapof.core.objects.Family"] = family_mod
    objects_pkg.Family = _BaseFamily


_install_test_stubs()

if "mapof.elections.objects.ElectionExperiment" in sys.modules:
    del sys.modules["mapof.elections.objects.ElectionExperiment"]

from mapof.elections.objects.ElectionExperiment import ElectionExperiment, _check_if_all_equal


class ConcreteExperiment(ElectionExperiment):
    def add_folders_to_experiment(self):
        return None

    def add_feature(self, name, function):
        return (name, function)

    def add_culture(self, name, function):
        return (name, function)


class RecordingAddElectionExperiment(ConcreteExperiment):
    def __init__(self):
        super().__init__(experiment_id='exp', instance_type='ordinal')
        self.calls = []

    def add_election(self, **kwargs):
        self.calls.append(kwargs)
        return ['ok']


class RecordingFamilyExperiment(ConcreteExperiment):
    def __init__(self):
        super().__init__(experiment_id='exp', instance_type='ordinal')
        self.family_args = None

    def add_family(self, **kwargs):
        self.family_args = kwargs
        return ['family']


def test_add_election_from_matrix_requires_square_matrix():
    experiment = RecordingAddElectionExperiment()
    matrix = [[1, 0, 0], [0, 1, 0]]

    with pytest.raises(ValueError, match="Matrix is not square"):
        experiment.add_election_from_matrix(matrix)


def test_add_election_from_matrix_passes_frequency_matrix_to_add_election():
    experiment = RecordingAddElectionExperiment()
    matrix = [[0, 1], [1, 0]]

    result = experiment.add_election_from_matrix(matrix, label='freq', params={'foo': 'bar'})

    assert result is None
    assert experiment.calls, "add_election should be invoked"
    call = experiment.calls[-1]
    assert call['frequency_matrix'] == matrix
    assert call['num_candidates'] == 2
    assert call['culture_id'] == 'frequency_matrix'


def test_elections_property_is_alias_for_instances():
    experiment = ConcreteExperiment(experiment_id='exp', instance_type='ordinal')
    dummy = object()

    experiment.elections = {'foo': dummy}

    assert experiment.instances['foo'] is dummy
    assert experiment.elections['foo'] is dummy

    experiment.num_elections = 5
    assert experiment.num_instances == 5
    assert experiment.num_elections == 5


def test_add_election_uses_default_sizes_when_missing():
    experiment = RecordingFamilyExperiment()
    experiment.default_num_candidates = 7
    experiment.default_num_voters = 13

    experiment.add_election(culture_id='test-culture', size=3)

    assert experiment.family_args['num_candidates'] == 7
    assert experiment.family_args['num_voters'] == 13
    assert experiment.family_args['culture_id'] == 'test-culture'


def test_check_if_all_equal_warns_on_mixed_values():
    with pytest.warns(UserWarning, match='Not all num_candidates values are equal!'):
        _check_if_all_equal([1, 2], 'num_candidates')


def test_check_if_all_equal_silent_for_uniform_values():
    import warnings

    with warnings.catch_warnings(record=True) as records:
        warnings.simplefilter('error')
        _check_if_all_equal([4, 4, 4], 'num_voters')
    assert records == []
