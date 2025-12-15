import numpy as np
import pytest

from mapof.elections.distances import positionwise_infty as positionwise


class DummyElection:
    def __init__(self, matrix):
        self._matrix = np.array(matrix, dtype=float)
        self.num_candidates = len(matrix)

    def get_frequency_matrix(self):
        return np.array(self._matrix)


def test_stretch_matrix_replicates_columns_and_preserves_sum():
    matrix = np.array([[2, 0], [0, 2]], dtype=float)

    stretched = positionwise.stretch_matrix(matrix, matrix_size=2, factor=2)

    assert stretched.shape == (4, 4)
    assert np.allclose(stretched[:, 0], [1, 1, 0, 0])
    assert np.allclose(stretched[:, 0], stretched[:, 1])
    assert np.allclose(stretched[:, 2], stretched[:, 3])
    for idx in range(matrix.shape[1]):
        base_column = idx * 2
        assert np.isclose(stretched[:, base_column].sum(), matrix[:, idx].sum())


def test_copy_to_original_mapping_includes_original_votes():
    mapping = positionwise.copy_to_original_mapping(positionwise.find_copies(3, 2))

    assert mapping == {0: 0, 1: 0, 2: 2, 3: 2, 4: 4, 5: 4}


def test_memoization_to_cost_table_expands_using_copy_mappings():
    memo_table = {
        (0, 0): 1.0,
        (0, 2): 2.0,
        (2, 0): 3.0,
        (2, 2): 4.0,
    }
    e1_map = {0: 0, 1: 0, 2: 2, 3: 2}
    e2_map = {0: 0, 1: 0, 2: 2, 3: 2}

    cost_table = positionwise.memoization_to_cost_table(memo_table, 4, e1_map, e2_map)

    assert cost_table == [
        [1.0, 1.0, 2.0, 2.0],
        [1.0, 1.0, 2.0, 2.0],
        [3.0, 3.0, 4.0, 4.0],
        [3.0, 3.0, 4.0, 4.0],
    ]


def test_positionwise_size_independent_uses_solver_and_normalizes(mocker):
    election_one = DummyElection([[1, 0], [0, 1]])
    election_two = DummyElection(np.eye(3))
    captured = {}

    def fake_solver(cost_table):
        captured["table"] = cost_table
        return 12.0, ["mapping"]

    mocker.patch(
        "mapof.elections.distances.positionwise_infty.solve_matching_vectors",
        side_effect=fake_solver,
    )

    distance, mapping = positionwise.positionwise_size_independent(
        election_one, election_two
    )

    # lcm(2, 3) = 6 -> normalization divisor is 2 * 3 = 6
    assert distance == pytest.approx(12.0 / 6)
    assert mapping == ["mapping"]

    election_lcm = positionwise.lcm(
        election_one.num_candidates, election_two.num_candidates
    )
    factor_one = int(election_lcm / election_one.num_candidates)
    factor_two = int(election_lcm / election_two.num_candidates)
    e1_stretched = positionwise.stretch_matrix(
        election_one.get_frequency_matrix(), election_one.num_candidates, factor_one
    )
    e2_stretched = positionwise.stretch_matrix(
        election_two.get_frequency_matrix(), election_two.num_candidates, factor_two
    )
    e1_original_to_copies = positionwise.find_copies(
        matrix_size=election_one.num_candidates, factor=factor_one
    )
    e2_original_to_copies = positionwise.find_copies(
        matrix_size=election_two.num_candidates, factor=factor_two
    )
    memo_table = positionwise.memoization(
        e1_stretched,
        e1_original_to_copies.keys(),
        e2_stretched,
        e2_original_to_copies.keys(),
    )
    expected_cost = positionwise.memoization_to_cost_table(
        memo_table,
        election_lcm,
        positionwise.copy_to_original_mapping(e1_original_to_copies),
        positionwise.copy_to_original_mapping(e2_original_to_copies),
    )

    np.testing.assert_allclose(np.array(captured["table"]), np.array(expected_cost))
