import math

import pytest

from mapof.elections.distances import feature_distance as fd


class DummyElection:
    """Minimal election stub exposing the get_feature API."""

    def __init__(self, features, missing=None):
        self.features = features
        self.missing = missing or set()

    def get_feature(self, feature_id, compute_if_missing=False, **_):
        if compute_if_missing:
            raise AssertionError("feature_distance should not recompute features")
        if feature_id in self.missing:
            raise KeyError(feature_id)
        return self.features[feature_id]


def test_feature_l1_distance_is_correct():
    election_1 = DummyElection({'f1': 1.0, 'f2': 4.0})
    election_2 = DummyElection({'f1': 0.0, 'f2': 1.0})

    distance = fd.features_vector_l1(election_1, election_2, ['f1', 'f2'])

    assert distance == pytest.approx(4.0)


def test_feature_l2_distance_is_correct():
    election_1 = DummyElection({'score': 3.0, 'ratio': 1.0})
    election_2 = DummyElection({'score': 1.0, 'ratio': 1.0})

    distance = fd.features_vector_l2(election_1, election_2, ['score', 'ratio'])

    assert distance == pytest.approx(math.sqrt(4.0))


def test_missing_feature_raises_informative_error():
    election_1 = DummyElection({'exists': 0.0})
    election_2 = DummyElection({'exists': 1.0}, missing={'missing'})

    with pytest.raises(Exception, match="Feature missing not found"):
        fd.features_vector_l1(election_1, election_2, ['exists', 'missing'])
