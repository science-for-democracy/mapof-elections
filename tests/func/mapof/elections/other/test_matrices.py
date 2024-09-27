
import pytest

from mapof.elections.other.matrices import \
    prepare_matrices, \
    generate_positionwise_matrix

culture_matrix_to_test = {
    'conitzer_matrix',
    'walsh_matrix',
    'single-crossing_matrix',
    'gs_caterpillar_matrix',
}


class TestMatrices:

    @pytest.mark.parametrize("culture_matrix_id", culture_matrix_to_test)
    def test_generate_positionwise_matrix(self, culture_matrix_id):
        matrix = generate_positionwise_matrix(culture_matrix_id, num_candidates=5)
        assert matrix.shape == (5, 5)

    # def test_generate_mallows_positionwise_matrix(self):
    #     matrix = generate_positionwise_matrix('norm-mallows_matrix', num_candidates=5,
    #                                           params={'normphi': 0.5})
    #     assert matrix.shape == (5, 5)
