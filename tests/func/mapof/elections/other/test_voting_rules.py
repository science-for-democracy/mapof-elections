

import mapof.elections as mapof

from mapof.elections.other.ordinal_rules import (
    compute_standard_voting_rule,
    compute_sntv_voting_rule,
    compute_borda_voting_rule,
    compute_stv_voting_rule,
    get_borda_points

)


class TestWinners:

    def setup_method(self):
        self.election = mapof.generate_ordinal_election(
            culture_id='impartial',
            num_voters=10,
            num_candidates=5
        )

    def test_compute_sntv_winners(self):
        winners = compute_sntv_voting_rule(self.election, committee_size=3)
        assert len(winners) == 3

    def test_compute_borda_winners(self):
        winners = compute_borda_voting_rule(self.election, committee_size=3)
        assert len(winners) == 3

    def test_compute_stv_winners(self):
        winners = compute_stv_voting_rule(self.election, committee_size=3)
        assert len(winners) == 3

    def test_get_borda_points(self):
        points = get_borda_points(
            votes=self.election.votes,
            num_voters=self.election.num_voters,
            num_candidates=self.election.num_candidates
        )
        assert len(points) == self.election.num_candidates

    def test_scoring_rule(self):
        winners = compute_standard_voting_rule(
            self.election,
            committee_size=3,
            type="scoring",
            name="borda"
        )
        assert len(winners) == 3

    def test_borda_owa(self):
        winners = compute_standard_voting_rule(
            self.election,
            committee_size=3,
            type="borda_owa",
            name="borda"
        )
        assert len(winners) == 3

    def test_bloc_owa(self):
        winners = compute_standard_voting_rule(
            self.election,
            committee_size=3,
            type="bloc_owa",
            name="borda"
        )
        assert len(winners) == 3