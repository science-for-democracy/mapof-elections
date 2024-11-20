import pytest
import numpy as np

import mapof.elections as mapof


registered_approval_features_without_params = {
    'max_approval_score',
    'abstract',
}

registered_complex_approval_with_params = {
    'cohesiveness',
    'justified_ratio',
    'number_of_cohesive_groups',
    'number_of_cohesive_groups_brute',
    'proportionality_degree_av',
    'proportionality_degree_pav',
    'proportionality_degree_cc',
}


class TestFeatures:

    @pytest.mark.parametrize("feature_id", registered_approval_features_without_params)
    def test_approval_features_without_params(self, feature_id):

        num_voters = np.random.randint(10, 20)
        num_candidates = np.random.randint(5, 10)

        election = mapof.generate_approval_election(culture_id='impartial',
                                                    num_voters=num_voters,
                                                    num_candidates=num_candidates,
                                                    p=0.5)

        election.compute_feature(feature_id)

    @pytest.mark.parametrize("feature_id", registered_complex_approval_with_params)
    def test_approval_features_with_params(self, feature_id):

        num_voters = np.random.randint(10, 20)
        num_candidates = np.random.randint(5, 10)

        election = mapof.generate_approval_election(culture_id='impartial',
                                                    num_voters=num_voters,
                                                    num_candidates=num_candidates,
                                                    p=0.5)

        election.compute_feature(feature_id, feature_params={'committee_size': 2})

    def test_priceability(self):

        num_voters = np.random.randint(10, 20)
        num_candidates = np.random.randint(5, 10)

        election = mapof.generate_approval_election(culture_id='impartial',
                                                    num_voters=num_voters,
                                                    num_candidates=num_candidates,
                                                    p=0.5)

        election.compute_rule(rule_id='av')

        election.compute_feature(feature_id='priceability',
                                 feature_params={'committee_size': 2, 'rule': 'av'})

    def test_core(self):

        num_voters = np.random.randint(10, 20)
        num_candidates = np.random.randint(5, 10)

        election = mapof.generate_approval_election(culture_id='impartial',
                                                    num_voters=num_voters,
                                                    num_candidates=num_candidates,
                                                    p=0.5)

        election.compute_rule(rule_id='av')

        election.compute_feature(feature_id='core',
                                 feature_params={'committee_size': 2, 'rule': 'av'})

    def test_ejr(self):

        num_voters = np.random.randint(10, 20)
        num_candidates = np.random.randint(5, 10)

        election = mapof.generate_approval_election(culture_id='impartial',
                                                    num_voters=num_voters,
                                                    num_candidates=num_candidates,
                                                    p=0.5)

        election.compute_rule(rule_id='av')

        election.compute_feature(feature_id='ejr',
                                 feature_params={'committee_size': 2, 'rule': 'av'})
