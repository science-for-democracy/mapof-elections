import pytest
import numpy as np

import mapof.elections as mapof

registered_ordinal_distances_to_test = {
    'emd-positionwise',
    'l1-positionwise',
    'emd-bordawise',
    'l1-pairwise',

    'discrete',
    'swap',
    'spearman',

    'blank',
    'positionwise_infty',
    'l1-voterlikeness',
    'ilp_spearman',

    'truncated_swap'
}


class TestOrdinalDistances:

    @pytest.mark.parametrize("distance_id", registered_ordinal_distances_to_test)
    def test_ordinal_distances(self, distance_id):

        num_voters = np.random.randint(4, 6)
        num_candidates = np.random.randint(3, 5)

        ele_1 = mapof.generate_ordinal_election(culture_id='impartial',
                                                num_voters=num_voters,
                                                num_candidates=num_candidates)

        ele_2 = mapof.generate_ordinal_election(culture_id='impartial',
                                                num_voters=num_voters,
                                                num_candidates=num_candidates)

        distance, mapping = mapof.compute_distance(ele_1, ele_2, distance_id=distance_id)
        assert type(float(distance)) is float
