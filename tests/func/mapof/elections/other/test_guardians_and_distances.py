
import pytest

from mapof.elections.cultures.pseudo_cultures import (
    get_pairwise_matrix_for_guardian,
    get_pseudo_borda_vector
)

guardians_to_test = {
    'pseudo_identity',
    'pseudo_uniformity',
    'pseudo_antagonism',
    'pseudo_stratification'
}


class TestGuardiansAndDistances:

    @pytest.mark.parametrize("culture_id", guardians_to_test)
    def test_get_pairwise_matrix_for_guardian(self, culture_id):
        pairwise_matrix = get_pairwise_matrix_for_guardian(culture_id, num_candidates=6)
        assert pairwise_matrix.shape == (6, 6)

    @pytest.mark.parametrize("culture_id", guardians_to_test)
    def test_get_pseudo_borda_vector(self, culture_id):
        borda_vector = get_pseudo_borda_vector(culture_id, num_candidates=6, num_voters=10)
        assert len(borda_vector) == 6