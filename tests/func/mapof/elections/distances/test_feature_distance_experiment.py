import numpy as np
import pytest

import mapof.elections as mapof

DAP = ['diversity_approx', 'agreement_approx', 'polarization_approx']


@pytest.fixture
def experiment():
    experiment = mapof.prepare_online_ordinal_experiment()
    experiment.add_family(culture_id='impartial', size=2, num_candidates=5, num_voters=10)
    experiment.add_family(culture_id='identity', size=1, num_candidates=5, num_voters=10)
    return experiment


def _vector(experiment, election_id, feature_ids):
    return np.array([experiment.features[f]['value'][election_id] for f in feature_ids])


@pytest.mark.parametrize("distance_id, ord", [('feature_l1', 1), ('feature_l2', 2)])
def test_feature_distance_on_computed_dap_features(experiment, distance_id, ord):
    for feature_id in DAP:
        experiment.compute_feature(feature_id)

    experiment.compute_distances(distance_id=distance_id, feature_ids=DAP)

    ids = list(experiment.instances)
    for i, id_1 in enumerate(ids):
        for id_2 in ids[i + 1:]:
            expected = np.linalg.norm(
                _vector(experiment, id_1, DAP) - _vector(experiment, id_2, DAP), ord=ord)
            assert experiment.distances[id_1][id_2] == pytest.approx(expected)


def test_feature_distance_on_manually_assigned_features(experiment):
    ids = list(experiment.instances)
    # import_feature returns plain {instance_id: value} dictionaries
    experiment.features['d'] = {ids[0]: 0.0, ids[1]: 3.0, ids[2]: 0.0}
    experiment.features['a'] = {ids[0]: 0.0, ids[1]: 4.0, ids[2]: 1.0}

    experiment.compute_distances(distance_id='feature_l2', feature_ids=['d', 'a'])

    assert experiment.distances[ids[0]][ids[1]] == pytest.approx(5.0)
    assert experiment.distances[ids[0]][ids[2]] == pytest.approx(1.0)


def test_missing_feature_raises(experiment):
    with pytest.raises(ValueError, match="Feature d not found"):
        experiment.compute_distances(distance_id='feature_l2', feature_ids=['d'])


def test_other_distances_are_unaffected_after_feature_distance(experiment):
    experiment.features['d'] = {i: 0.0 for i in experiment.instances}
    experiment.compute_distances(distance_id='feature_l2', feature_ids=['d'])

    experiment.compute_distances(distance_id='emd-positionwise')

    ids = list(experiment.instances)
    assert experiment.distances[ids[0]][ids[1]] > 0
