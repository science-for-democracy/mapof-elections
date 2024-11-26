import numpy as np

import pytest

import mapof.elections as mapel

registered_approval_cultures_to_test = {
    'impartial',
    'identity',
    'resampling',
    'disjoint_resampling',
    'moving_resampling',
    'noise',
    'euclidean',
    'truncated_urn',
    'urn_partylist',
    'full',
    'empty',
}


class TestCultures:

    @pytest.mark.parametrize("culture_id", registered_approval_cultures_to_test)
    def test_approval_cultures(self, culture_id):

        num_voters = np.random.randint(10, 20)
        num_candidates = np.random.randint(10, 20)

        if culture_id in ['resampling']:
            election = mapel.generate_approval_election(culture_id=culture_id,
                                                        num_voters=num_voters,
                                                        num_candidates=num_candidates,
                                                        params={'phi': 0.4, 'p': 0.4})
        elif culture_id in ['noise']:
            election = mapel.generate_approval_election(culture_id=culture_id,
                                                        num_voters=num_voters,
                                                        num_candidates=num_candidates,
                                                        params={'phi': 0.4,
                                                                'rel_size_central_vote': 0.5})
        elif culture_id in ['moving_resampling']:
            election = mapel.generate_approval_election(culture_id=culture_id,
                                                        num_voters=num_voters,
                                                        num_candidates=num_candidates,
                                                        params={'phi': 0.4,
                                                                'p': 0.4,
                                                                'num_legs': 3})
        elif culture_id in ['disjoint_resampling']:
            election = mapel.generate_approval_election(culture_id=culture_id,
                                                        num_voters=num_voters,
                                                        num_candidates=num_candidates,
                                                        params={'phi': 0.4,
                                                                'p': 0.2,
                                                                'num_central_votes': 3})

        elif culture_id in ['truncated_urn']:
            election = mapel.generate_approval_election(culture_id=culture_id,
                                                        num_voters=num_voters,
                                                        num_candidates=num_candidates,
                                                        params={'p': 0.4, 'alpha': 0.1})

        elif culture_id in ['urn_partylist']:
            election = mapel.generate_approval_election(culture_id=culture_id,
                                                        num_voters=num_voters,
                                                        num_candidates=num_candidates,
                                                        params={'alpha': 0.1,
                                                                'parties': 2})
        else:
            election = mapel.generate_approval_election(culture_id=culture_id,
                                                        num_voters=num_voters,
                                                        num_candidates=num_candidates)

        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

        assert len(election.votes) == num_voters
