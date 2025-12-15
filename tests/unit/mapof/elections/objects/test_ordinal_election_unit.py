import numpy as np

import mapof.elections as mapof
from mapof.elections.objects.OrdinalElection import convert_votes_to_potes


def _simple_election(votes):
    election = mapof.generate_ordinal_election_from_votes(votes)
    election.compute_potes()
    return election


def test_frequency_matrix_cache_and_recompute():
    votes = [[0, 1], [1, 0]]
    election = _simple_election(votes)

    matrix = election.get_frequency_matrix()
    expected = matrix.copy()

    # Cached matrix should be reused without recomputation.
    matrix[0][0] = 999
    cached = election.get_frequency_matrix()
    assert cached[0][0] == 999

    recomputed = election.get_frequency_matrix(is_recomputed=True)
    np.testing.assert_allclose(recomputed, expected)


def test_bordawise_vector_cache_and_sorting():
    votes = [[0, 1], [1, 0]]
    election = _simple_election(votes)

    expected = election._votes_to_bordawise_vector()
    election.bordawise_vector = expected.copy()
    np.testing.assert_allclose(election.get_bordawise_vector(), expected)

    election.bordawise_vector[0] = 5
    cached = election.get_bordawise_vector()
    assert cached[0] == 5
    recomputed = election.get_bordawise_vector(is_recomputed=True)
    np.testing.assert_allclose(recomputed, expected)


def test_votes_to_pairwise_matrix_matches_manual_counts():
    votes = [
        [0, 1, 2],
        [1, 2, 0],
        [2, 0, 1],
    ]
    election = _simple_election(votes)

    pairwise = election.votes_to_pairwise_matrix()

    num_candidates = election.num_candidates
    num_voters = election.num_voters
    expected = np.zeros_like(pairwise)
    for a in range(num_candidates):
        for b in range(num_candidates):
            if a == b:
                continue
            preferred = sum(1 for vote in votes if vote.index(a) < vote.index(b))
            expected[a][b] = preferred / num_voters
    np.testing.assert_allclose(pairwise, expected)


def test_convert_votes_to_potes_positions():
    votes = [[0, 1, 2], [2, 0, 1]]
    potes = convert_votes_to_potes(votes)
    expected = np.array([[0, 1, 2], [1, 2, 0]])
    np.testing.assert_array_equal(potes, expected)


def test_votes_to_agg_voterlikeness_vector_counts_disagreements():
    votes = [
        [0, 1, 2],
        [0, 2, 1],
        [2, 0, 1],
    ]
    election = _simple_election(votes)

    vector, total = election.votes_to_agg_voterlikeness_vector()

    assert total == election.num_voters
    expected = np.zeros_like(vector)
    for v1, pote_a in enumerate(election.potes):
        for pote_b in election.potes:
            disagreements = 0
            for i in range(election.num_candidates):
                for j in range(i + 1, election.num_candidates):
                    diff_a = pote_a[i] - pote_a[j]
                    diff_b = pote_b[i] - pote_b[j]
                    if diff_a * diff_b < 0:
                        disagreements += 1
            expected[v1] += disagreements
    np.testing.assert_array_equal(vector, expected)
