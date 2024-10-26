
import pytest

from mapof.elections.cultures.matrices.matrices import generate_frequency_matrix


guardians_to_test = {
    'pseudo_identity',
    'pseudo_uniformity',
    'pseudo_antagonism',
    'pseudo_stratification'
}

paths_to_test = {
    'pseudo_unid',
    'pseudo_anid',
    'pseudo_stid',
    'pseudo_anun',
    'pseudo_stun',
    'pseudo_stan',
}

cultures_to_test = {
    'pseudo_sp_conitzer',
    'pseudo_sp_walsh',
    'pseudo_single-crossing',
}

class TestMatrices:

    @pytest.mark.parametrize("culture_id", guardians_to_test)
    def test_generate_positionwise_matrix_for_guardians(self, culture_id):
        frequency_matrix = generate_frequency_matrix(culture_id, num_candidates=6)
        assert frequency_matrix.shape == (6, 6)

    @pytest.mark.parametrize("culture_id", paths_to_test)
    def test_generate_frequency_matrix_for_paths(self, culture_id):
        params = {'alpha': 0.5}
        frequency_matrix = generate_frequency_matrix(culture_id, num_candidates=6, params=params)
        assert frequency_matrix.shape == (6, 6)

    @pytest.mark.parametrize("culture_id", cultures_to_test)
    def test_generate_positionwise_matrix_for_cultures(self, culture_id):
        frequency_matrix = generate_frequency_matrix(culture_id, num_candidates=6)
        assert frequency_matrix.shape == (6, 6)



    # def test_generate_mallows_positionwise_matrix(self):
    #     frequency_matrix = generate_positionwise_matrix('norm-mallows_matrix', num_candidates=5,
    #                                           params={'normphi': 0.5})
    #     assert frequency_matrix.shape == (5, 5)
