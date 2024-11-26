import pytest
import numpy as np

import mapof.elections as mapof


simple_ordinal_cultures_to_test = {
    'identity',
    'impartial',
    'iac',
    'urn',
    'single_peaked_walsh',
    'single_peaked_conitzer',
    'spoc',
    'single_crossing',
    'mallows',
    'norm_mallows',
}

cultures_with_even_number_of_voters = {
    'antagonism',
}

tree_samplers_to_test = {
    'balanced',
    'caterpillar',
}

spaces_to_test = {
    'uniform',
    'sphere',
    'gaussian',
    'ball',
}

approx_cultures = {
    'approx_stratification',
    'approx_uniformity',
}

unpopular_ordinal_cultures_to_test = {
    'idan_part',
    'idun_part',
    'idst_part',
    'anun_part',
    'anst_part',
    'unst_part',
}

other_cultures = {
    'idst_blocks',
    'unst_topsize',
    'un_from_list',
}


class TestCultures:

    @pytest.mark.parametrize("culture_id", simple_ordinal_cultures_to_test)
    def test_simple_cultures(self, culture_id):
        num_voters = np.random.randint(10, 50)
        num_candidates = np.random.randint(10, 20)

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

        assert len(election.votes) == num_voters
        assert len(election.votes[0]) == num_candidates

    @pytest.mark.parametrize("culture_id", cultures_with_even_number_of_voters)
    def test_simple_cultures_even(self, culture_id):
        num_voters = 20
        num_candidates = 10

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

        assert len(election.votes) == num_voters
        assert len(election.votes[0]) == num_candidates

    @pytest.mark.parametrize("culture_id", unpopular_ordinal_cultures_to_test)
    def test_unpopular_cultures(self, culture_id):
        num_voters = 10
        num_candidates = 6
    
        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
    
        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

    @pytest.mark.parametrize("space", spaces_to_test)
    def test_euclidean(self, space):
        num_voters = np.random.randint(10, 50)
        num_candidates = np.random.randint(10, 20)
        election = mapof.generate_ordinal_election(culture_id='euclidean',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   params={'space': space})
        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

        assert len(election.votes) == num_voters
        assert len(election.votes[0]) == num_candidates

    @pytest.mark.parametrize("culture_id", approx_cultures)
    def test_approx_cultures(self, culture_id):
        num_voters = 16
        num_candidates = 8
        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

        assert len(election.votes) == num_voters
        assert len(election.votes[0]) == num_candidates

    def test_single_crossing(self):
        culture_id = 'single_crossing'
        num_voters = 10
        num_candidates = 10
        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

        assert len(election.votes) == num_voters
        assert len(election.votes[0]) == num_candidates

    @pytest.mark.parametrize("culture_id", other_cultures)
    def test_other_cultures(self, culture_id):
        num_voters = 16
        num_candidates = 8
        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

        assert len(election.votes) == num_voters
        assert len(election.votes[0]) == num_candidates

    @pytest.mark.parametrize("tree_sampler", tree_samplers_to_test)
    def test_group_separable(self, tree_sampler):
        num_voters = 20
        num_candidates = 10
        election = mapof.generate_ordinal_election(culture_id='group_separable',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   tree_sampler=tree_sampler)
        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

        assert len(election.votes) == num_voters
        assert len(election.votes[0]) == num_candidates



