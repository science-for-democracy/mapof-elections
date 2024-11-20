import mapof.elections as mapel
from mapof.elections.distances import main_ordinal_distances as mod


class TestSwapDistance:
    def test_bf_vs_ilp_swap_distance(self):
        for _ in range(5):
            election_1 = mapel.generate_ordinal_election(culture_id='impartial',
                                                         num_voters=5,
                                                         num_candidates=3)
            election_2 = mapel.generate_ordinal_election(culture_id='impartial',
                                                         num_voters=5,
                                                         num_candidates=3)

            distance_1, _ = mapel.compute_distance(election_1, election_2,
                                                   distance_id='swap')

            distance_2, _ = mod.swap_distance_bf(election_1, election_2)

            assert distance_1 == distance_2, "C++ BF swap distance differs from \
           Python BF swap distance"
