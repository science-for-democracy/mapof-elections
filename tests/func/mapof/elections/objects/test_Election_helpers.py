from types import SimpleNamespace

import numpy as np
import pytest

from mapof.elections.objects.Election import (
    Election,
    _get_format_from_instance_type,
    _map_the_votes,
    _remove_candidate_from_election,
    _unmap_the_winners,
)


def _make_election(votes, num_candidates):
    return SimpleNamespace(
        votes=[list(vote) for vote in votes],
        num_voters=len(votes),
        num_candidates=num_candidates,
    )


class TestVectorToInterval:

    def test_uses_num_candidates_when_precision_missing(self):
        dummy = SimpleNamespace(num_candidates=3)

        result = Election.vector_to_interval(dummy, [3.0, 6.0, 9.0])

        assert result == [3.0, 6.0, 9.0]

    def test_precision_is_split_evenly_across_candidates(self):
        dummy = SimpleNamespace(num_candidates=2)

        result = Election.vector_to_interval(dummy, [4.0, 8.0], precision=4)

        assert result == [2.0, 2.0, 4.0, 4.0]

    def test_precision_smaller_than_candidates_is_clamped(self):
        dummy = SimpleNamespace(num_candidates=4)

        result = Election.vector_to_interval(dummy, [1.0, 2.0, 3.0, 4.0], precision=2)

        assert result == [1.0, 2.0, 3.0, 4.0]

    @pytest.mark.parametrize(
        "num_candidates, vector",
        [
            (0, [1.0]),
            (2, [1.0]),
        ],
    )
    def test_invalid_inputs_raise_value_error(self, num_candidates, vector):
        dummy = SimpleNamespace(num_candidates=num_candidates)

        with pytest.raises(ValueError):
            Election.vector_to_interval(dummy, vector)


class TestVoteRemappingHelpers:

    def test_map_the_votes_shifts_candidates_after_removed_block(self):
        votes = [
            [0, 1, 2, 3],
            [3, 2, 1, 0],
        ]
        election = _make_election(votes, num_candidates=4)

        remapped = _map_the_votes(election, party_id=1, party_size=2)

        assert remapped.votes == [
            [0, 1, 0, 1],
            [1, 0, 1, 0],
        ]

    def test_unmap_the_winners_restores_original_indices(self):
        winners = [0, 1, 2]

        restored = _unmap_the_winners(winners, party_id=1, party_size=2)

        assert restored == [0, 1, 4]

    def test_remove_candidate_from_election_updates_votes_and_num_candidates(self):
        votes = [
            [0, 1, 2, 3],
            [3, 2, 1, 0],
        ]
        election = _make_election(votes, num_candidates=4)

        updated = _remove_candidate_from_election(election, party_id=0, party_size=2)

        assert updated.num_candidates == 2
        assert updated.votes == [
            [2, 3],
            [3, 2],
        ]


class TestMiscHelpers:

    def test_all_dist_zeros_handles_missing_and_empty_arrays(self):
        election = SimpleNamespace(distances={})

        # Missing entry -> treated as zeros
        assert Election.all_dist_zeros(election, 'vote')

        election.distances['vote'] = np.zeros((2, 2))
        assert Election.all_dist_zeros(election, 'vote')

    def test_all_dist_zeros_detects_nonzero_or_invalid_inputs(self):
        election = SimpleNamespace(distances={'vote': np.array([[0, 1], [0, 0]])})

        assert not Election.all_dist_zeros(election, 'vote')

        election.distances['vote'] = "not an array"
        assert not Election.all_dist_zeros(election, 'vote')

    def test_get_format_from_instance_type(self):
        assert _get_format_from_instance_type('approval') == 'app'
        assert _get_format_from_instance_type('ordinal') == 'soc'
        assert _get_format_from_instance_type('mixed') is None
