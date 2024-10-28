import mapof.elections as mapof
from mapof.elections.distances.ilp_subelections import (
    solve_ilp_voter_subelection,
    solve_ilp_candidate_subelection,
)


class TestOrdinalDistances:

    def setup_method(self):
        self.election_1 = mapof.generate_ordinal_election(
            culture_id='ic',
            num_voters=6,
            num_candidates=4
        )

        self.election_2 = mapof.generate_ordinal_election(
            culture_id='ic',
            num_voters=6,
            num_candidates=4
        )

    def test_solve_ilp_voter_subelection(self):
        solve_ilp_voter_subelection(self.election_1, self.election_2)

    # def test_solve_ilp_candidate_subelection(self):
    #     solve_ilp_candidate_subelection(self.election_1, self.election_2)
