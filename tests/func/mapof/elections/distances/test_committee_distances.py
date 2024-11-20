import pytest
import numpy as np

import mapof.elections as mapof
from mapof.elections.distances.committee_distances import get_matching_cost_committee


registered_committee_distances_to_test = {
    # 'discrete',
    # 'hamming',
    'asymmetric'
}


class TestCommitteeDistances:

    def setup_method(self):
        num_voters = 20
        num_candidates = 10

        self.election_1 = mapof.generate_approval_election(
            culture_id='impartial',
            num_voters=num_voters,
            num_candidates=num_candidates,
            p=0.5
        )

        candidates_set = np.array([i for i in range(num_candidates)])
        self.committee_1 = set(np.random.choice(candidates_set, 5, replace=False))
        self.committee_2 = set(np.random.choice(candidates_set, 5, replace=False))

    @pytest.mark.parametrize("distance_id", registered_committee_distances_to_test)
    def test_matching_cost_committee(self, distance_id):
        print("votes", self.election_1.votes)
        cost = get_matching_cost_committee(
            self.election_1,
            self.committee_1,
            self.committee_2,
            distance_id
        )
        assert type(cost) == int or type(cost) == float or type(cost) == np.float64
