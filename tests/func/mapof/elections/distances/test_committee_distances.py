import pytest

import mapof.elections as mapof
from mapof.elections.distances.committee_distances import get_matching_cost_committee
import itertools
import numpy as np


registered_committee_distances_to_test = {
    'discrete',
    'hamming',
    'asymmetric'
}


class TestCommitteeDistances:

    def setup_method(self):
        num_voters = 20
        num_candidates = 10

        self.election_1 = mapof.generate_ordinal_election(
            culture_id='ic',
            num_voters=num_voters,
            num_candidates=num_candidates
        )

        candidates_set = np.array([i for i in range(num_candidates)])
        self.committee_1 = np.random.choice(candidates_set, 5, replace=False)
        self.committee_2 = np.random.choice(candidates_set, 5, replace=False)


    @pytest.mark.parametrize("distance_id", registered_committee_distances_to_test)
    def test_solve_ilp_voter_subelection(self, distance_id):
        get_matching_cost_committee(
            self.election_1,
            self.committee_1,
            self.committee_2,
            "distance_id"
        )

    # def test_solve_ilp_candidate_subelection(self):
    #     solve_ilp_candidate_subelection(self.election_1, self.election_2)