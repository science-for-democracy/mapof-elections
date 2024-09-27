

import mapof.elections as mapof

from mapof.elections.other.winners import (
    compute_sntv_winners,
    compute_borda_winners,
    compute_stv_winners,
    get_borda_points
)


class TestWinners:

    def setup_method(self):
        self.election = mapof.generate_ordinal_election(
            culture_id='ic',
            num_voters=10,
            num_candidates=5
        )

    def test_compute_sntv_winners(self):
        winners = compute_sntv_winners(self.election, num_winners=3)
        assert len(winners) == 3

    def test_compute_borda_winners(self):
        winners = compute_borda_winners(self.election, num_winners=3)
        assert len(winners) == 3

    def test_compute_stv_winners(self):
        winners = compute_stv_winners(self.election, num_winners=3)
        assert len(winners) == 3

    def test_get_borda_points(self):
        points = get_borda_points(
            votes=self.election.votes,
            num_voters=self.election.num_voters,
            num_candidates=self.election.num_candidates
        )
        assert len(points) == self.election.num_candidates



