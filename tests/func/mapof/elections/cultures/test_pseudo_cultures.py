import pytest
import numpy as np

import mapof.elections as mapof

paths_to_test = {
    'pseudo_unid',
    'pseudo_anid',
    'pseudo_stid',
    'pseudo_anun',
    'pseudo_stun',
    'pseudo_stan',
}

guardians_to_test = {
    'pseudo_identity',
    'pseudo_uniformity',
    'pseudo_antagonism',
    'pseudo_stratification'
}

cultures_to_test = {
    'pseudo_single_peaked_conitzer',
    'pseudo_single_peaked_walsh',
    'pseudo_single_crossing',
}


class TestPseudoElection:

    @pytest.mark.parametrize("culture_id", guardians_to_test)
    def test_pseudo_guardians(self, culture_id):
        num_voters = np.random.randint(10, 40)
        num_candidates = np.random.randint(10, 20)

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

    @pytest.mark.parametrize("culture_id", paths_to_test)
    def test_pseudo_paths(self, culture_id):
        num_voters = np.random.randint(10, 40)
        num_candidates = np.random.randint(10, 20)

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   params={'alpha': 0.5})

        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

    @pytest.mark.parametrize("culture_id", cultures_to_test)
    def test_pseudo_cultures(self, culture_id):
        num_voters = np.random.randint(10, 40)
        num_candidates = np.random.randint(10, 20)

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

    def test_pseudo_stratification_culture(self):
        num_voters = np.random.randint(10, 40)
        num_candidates = np.random.randint(10, 20)

        for weight in [0.25, 0.75]:
            election = mapof.generate_ordinal_election(culture_id='pseudo_stratification',
                                                       num_voters=num_voters,
                                                       num_candidates=num_candidates,
                                                       params={'weight': weight})

            assert election.num_candidates == num_candidates
            assert election.num_voters == num_voters

    def test_pseudo_norm_mallows_culture(self):
        num_voters = 12
        num_candidates = 6

        election = mapof.generate_ordinal_election(culture_id='pseudo_norm_mallows',
                                                       num_voters=num_voters,
                                                       num_candidates=num_candidates,
                                                       params={'normphi': 0.5})

        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters


class TestFrequencyMatrixOfPseudoElection:

    @pytest.mark.parametrize("culture_id", guardians_to_test)
    def test_pseudo_guardians_frequency_matrix(self, culture_id):
        num_voters = np.random.randint(10, 40)
        num_candidates = np.random.randint(10, 20)

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        frequency_matrix = election.get_frequency_matrix()

        assert frequency_matrix.shape == (num_candidates, num_candidates)

    @pytest.mark.parametrize("culture_id", paths_to_test)
    def test_pseudo_paths_frequency_matrix(self, culture_id):
        num_voters = np.random.randint(10, 40)
        num_candidates = np.random.randint(10, 20)

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   params={'alpha': 0.5})
        frequency_matrix = election.get_frequency_matrix()

        assert frequency_matrix.shape == (num_candidates, num_candidates)

    @pytest.mark.parametrize("culture_id", cultures_to_test)
    def test_pseudo_culture_frequency_matrix(self, culture_id):
        num_voters = np.random.randint(10, 40)
        num_candidates = np.random.randint(10, 20)

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
        frequency_matrix = election.get_frequency_matrix()

        assert frequency_matrix.shape == (num_candidates, num_candidates)

    def test_pseudo_stratification_frequency_matrix(self):
        num_voters = np.random.randint(10, 40)
        num_candidates = np.random.randint(10, 20)

        for weight in [0.25, 0.75]:
            election = mapof.generate_ordinal_election(culture_id='pseudo_stratification',
                                                       num_voters=num_voters,
                                                       num_candidates=num_candidates,
                                                       params={'weight': weight})
        frequency_matrix = election.get_frequency_matrix()

        assert frequency_matrix.shape == (num_candidates, num_candidates)

    # def test_pseudo_norm_mallows_frequency_matrix(self):
    #     num_voters = 12
    #     num_candidates = 6
    #
    #     election = mapof.generate_ordinal_election(culture_id='pseudo_norm_mallows',
    #                                                num_voters=num_voters,
    #                                                num_candidates=num_candidates,
    #                                                params={'normphi': 0.5})
    #     frequency_matrix = election.get_frequency_matrix()
    #
    #     assert frequency_matrix.shape == (num_candidates, num_candidates)
