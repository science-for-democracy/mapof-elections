import pytest
import numpy as np

import mapof.elections as mapof

#      waiting for the update in prefsampling
#     'group-separable': mask.group_separable_mask,

#     'unst_topsize': compass_approx.generate_unst_topsize_votes,  # unsupported culture
#     'idst_blocks': compass_approx.generate_idst_blocks_votes,
#     'norm-mallows_mixture': mallows.generate_norm_mallows_mixture_votes,  # unsupported culture
#     'mallows_triangle': mallows.generate_mallows_votes,  # unsupported culture
#     'walsh_party': unused.generate_sp_party,  # unsupported culture
#     'conitzer_party': unused.generate_sp_party,  # unsupported culture
#     'mallows_party': mallows.generate_mallows_party,  # unsupported culture
#     'ic_party': unused.generate_ic_party,  # unsupported culture
#     'un_from_list': compass_approx.generate_un_from_list,  # unsupported culture
#     'urn_model': pref_ordinal.urn,  # deprecated name


new_to_test = {
    'didi',
    'placektt_luce'
}

simple_ordinal_cultures_to_test = {
    'identity',
    'id',
    'ic',
    'impartial',
    'impartial_culture',
    'iac',
    'urn',
    'single-peaked_walsh',
    'single-peaked_conitzer',
    'spoc',
    'single-crossing',
    'mallows',
    'norm-mallows',
}

cultures_with_even_number_of_voters = {
    'an',
    'antagonism',
}

tree_samplers_to_test = {
    # 'balanced',
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


class TestCultures:

    @pytest.mark.parametrize("culture_id", simple_ordinal_cultures_to_test)
    def test_simple_cultures(self, culture_id):
        num_voters = np.random.randint(10, 100)
        num_candidates = np.random.randint(10, 100)

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

        assert len(election.votes) == num_voters
        assert len(election.votes[0]) == num_candidates


    @pytest.mark.parametrize("culture_id", cultures_with_even_number_of_voters)
    def test_simple_cultures(self, culture_id):
        num_voters = 20
        num_candidates = 10

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

        assert len(election.votes) == num_voters
        assert len(election.votes[0]) == num_candidates

    # @pytest.mark.parametrize("culture_id", unpopular_ordinal_cultures_to_test)
    # def test_unpopular_cultures(self, culture_id):
    #     num_voters = 10
    #     num_candidates = 6
    #
    #     election = mapel.generate_ordinal_election(culture_id=culture_id,
    #                                                num_voters=num_voters,
    #                                                num_candidates=num_candidates)
    #
    #     assert election.num_candidates == num_candidates
    #     assert election.num_voters == num_voters

    @pytest.mark.parametrize("space", spaces_to_test)
    def test_euclidean(self, space):
        num_voters = np.random.randint(10, 100)
        num_candidates = np.random.randint(10, 100)
        election = mapof.generate_ordinal_election(culture_id='euclidean',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   space=space)
        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

        assert len(election.votes) == num_voters
        assert len(election.votes[0]) == num_candidates

    @pytest.mark.parametrize("culture_id", approx_cultures)
    def test_approx_cultures(self, culture_id):
        num_voters = 20
        num_candidates = 10
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
        election = mapof.generate_ordinal_election(culture_id='group-separable',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   tree_sampler=tree_sampler)
        assert election.num_candidates == num_candidates
        assert election.num_voters == num_voters

        assert len(election.votes) == num_voters
        assert len(election.votes[0]) == num_candidates

