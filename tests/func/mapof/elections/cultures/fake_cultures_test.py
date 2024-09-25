import pytest
import numpy as np

import mapof.elections as mapel

paths_to_test = {
    'unid',
    'anid',
    'stid',
    'anun',
    'stun',
    'stan',
}

guardians_to_test = {
    'identity',
    'uniformity',
    'antagonism',
    'stratification'
}


class TestCultures:

    @pytest.mark.parametrize("culture_id", paths_to_test)
    def test_fake_cultures(self, culture_id):
        num_voters = np.random.randint(10, 40)
        num_candidates = np.random.randint(10, 20)

        election = mapel.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   alpha=0.5)

        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

    @pytest.mark.parametrize("culture_id", paths_to_test)
    def test_fake_positionwise_vectors(self, culture_id):
        num_voters = np.random.randint(10, 40)
        num_candidates = np.random.randint(10, 20)

        election = mapel.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   alpha=0.5)
        election.votes_to_positionwise_vectors()

        assert election.vectors.shape == (num_candidates, num_candidates)

    @pytest.mark.parametrize("culture_id", guardians_to_test)
    def test_fake_positionwise_vectors(self, culture_id):
        num_voters = np.random.randint(10, 40)
        num_candidates = np.random.randint(10, 20)

        if culture_id == 'stratification':
            election = mapel.generate_ordinal_election(culture_id=culture_id,
                                                       num_voters=num_voters,
                                                       num_candidates=num_candidates,
                                                       weight=0.5)
        else:
            election = mapel.generate_ordinal_election(culture_id=culture_id,
                                                       num_voters=num_voters,
                                                       num_candidates=num_candidates)

        borda_vector = election.votes_to_bordawise_vector()

        assert len(borda_vector) == num_candidates

