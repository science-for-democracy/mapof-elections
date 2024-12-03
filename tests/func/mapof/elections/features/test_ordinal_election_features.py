import pytest
import numpy as np

import mapof.elections as mapof


registered_ordinal_features_to_test = {
    'highest_borda_score',
    'highest_plurality_score',
    'highest_copeland_score',
    'lowest_dodgson_score',
    'highest_cc_score',
    'highest_hb_score',
    'highest_pav_score',
    'borda_spread',
    'greedy_approx_cc_score',
    'greedy_approx_hb_score',
    'greedy_approx_pav_score',
    'removal_approx_cc_score',
    'removal_approx_hb_score',
    'removal_approx_pav_score',
    'banzhaf_cc_score',
    'cand_pos_dist_std',
    'agreement',
    'kkemeny_diversity_full',
    'kkemeny_polarization',
    'support_pairs',
    'support_triplets',
    'support_votes',
    'entropy',
    'is_condorcet',
    'effective_num_candidates',
    'partylist',
    'ranging_cc_score'
}




class TestFeaturesSanity:

    @pytest.mark.parametrize("feature_id", registered_ordinal_features_to_test)
    def test_ordinal_features_sanity(self, feature_id):

        num_voters = np.random.randint(10, 20)
        num_candidates = np.random.randint(5, 10)

        election = mapof.generate_ordinal_election(culture_id='impartial',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
        election.compute_feature(feature_id)


    def test_parameterized_diversity(self):

        num_voters = np.random.randint(10, 20)
        num_candidates = np.random.randint(5, 10)

        election = mapof.generate_ordinal_election(culture_id='impartial',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
        election.compute_feature('kkemeny_diversity_upto_r', r=5)

