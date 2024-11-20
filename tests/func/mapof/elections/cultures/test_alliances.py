import pytest
import numpy as np

import mapof.elections as mapof


alliance_cultures_to_test = {
    'impartial',
    'urn',
    'norm_mallows',
    'euclidean',
}


class TestCultures:

    @pytest.mark.parametrize("culture_id", alliance_cultures_to_test)
    def test_alliance_cultures(self, culture_id):
        num_voters = np.random.randint(10, 20)
        num_candidates = np.random.randint(6, 12)

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   params={'num_alliances': 2})

        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

        assert len(election.votes) == num_voters
        assert len(election.votes[0]) == num_candidates
