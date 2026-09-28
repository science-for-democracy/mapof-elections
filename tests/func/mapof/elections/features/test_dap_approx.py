import numpy as np
import pytest

from mapof.elections.features.register import registered_ordinal_election_features
from mapof.elections.features import dap_approx
from mapof.elections.objects.OrdinalElection import OrdinalElection


def _election(votes):
    votes = np.array(votes)
    return OrdinalElection(votes=votes,
                           num_voters=votes.shape[0],
                           num_candidates=votes.shape[1])


@pytest.fixture
def identity_election():
    return _election([[0, 1, 2, 3]] * 6)


@pytest.fixture
def antagonism_election():
    return _election([[0, 1, 2, 3]] * 3 + [[3, 2, 1, 0]] * 3)


@pytest.mark.parametrize("feature_id", ['diversity_approx',
                                        'agreement_approx',
                                        'polarization_approx',
                                        'cand_pos_dist_std_approx'])
def test_dap_approx_features_are_registered(feature_id):
    assert feature_id in registered_ordinal_election_features


def test_identity_has_full_agreement_and_no_diversity_or_polarization(identity_election):
    assert dap_approx.agreement_index(identity_election)['value'] == pytest.approx(1)
    assert dap_approx.diversity_index(identity_election)['value'] == pytest.approx(0)
    assert dap_approx.polarization_index(identity_election)['value'] == pytest.approx(0)


def test_antagonism_has_no_agreement_and_full_polarization(antagonism_election):
    assert dap_approx.agreement_index(antagonism_election)['value'] == pytest.approx(0)
    assert dap_approx.polarization_index(antagonism_election)['value'] == pytest.approx(1)
    # k=1: 3 opposite votes at swap distance 6 -> 18, k>=2: 0; 18 * 2/5 / 6 / 6
    assert dap_approx.diversity_index(antagonism_election)['value'] == pytest.approx(0.2)


def test_features_via_election_compute_feature(antagonism_election):
    antagonism_election.compute_feature('polarization_approx')
    assert antagonism_election.features['polarization_approx']['value'] == pytest.approx(1)


def test_pseudo_election_returns_none(identity_election):
    identity_election.is_pseudo = True
    for feature in [dap_approx.agreement_index, dap_approx.diversity_index,
                    dap_approx.polarization_index, dap_approx.cand_pos_dist_std]:
        assert feature(identity_election)['value'] is None


def test_vote2pote_places_unreported_candidates_in_the_middle():
    pote = dap_approx.vote2pote(np.array([1, 0, -1, -1]), 4)
    assert list(pote) == [1, 0, 2.5, 2.5]
