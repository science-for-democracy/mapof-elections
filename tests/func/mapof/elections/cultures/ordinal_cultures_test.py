import pytest
import numpy as np

import mapof.elections as mapel

simple_ordinal_cultures_to_test = {
    'ic',
    'iac',
    'urn',
    'single-crossing',
    'mallows',
    'norm-mallows',
    'conitzer',
    'spoc_conitzer',
    'walsh',
    'real_identity',
}

tree_samplers_to_test = {
    'balanced',
    'caterpillar',
    None
}

spaces_to_test = {
    'uniform',
    'sphere',
    'gaussian',
    'ball',
    None
}


class TestCultures:

    @pytest.mark.parametrize("culture_id", simple_ordinal_cultures_to_test)
    def test_simple_cultures(self, culture_id):
        num_voters = np.random.randint(10, 100)
        num_candidates = np.random.randint(10, 100)

        election = mapel.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

    @pytest.mark.parametrize("tree_sampler", tree_samplers_to_test)
    def test_group_separable(self, tree_sampler):
        num_voters = np.random.randint(10, 100)
        num_candidates = np.random.randint(10, 100)
        election = mapel.generate_ordinal_election(culture_id='group-separable',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   tree_sampler=tree_sampler)
        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

    @pytest.mark.parametrize("space", spaces_to_test)
    def test_group_separable(self, space):
        num_voters = np.random.randint(10, 100)
        num_candidates = np.random.randint(10, 100)
        election = mapel.generate_ordinal_election(culture_id='euclidean',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   space=space)
        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

    def test_stratification(self):
        num_voters = np.random.randint(10, 100)
        num_candidates = np.random.randint(10, 100)
        election = mapel.generate_ordinal_election(culture_id='stratification',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   weight=0.5)
        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters