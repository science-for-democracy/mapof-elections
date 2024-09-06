import numpy as np

import mapof.elections as mapel


class TestOrdinalElection:

    def test_vote_microscope(self):

        num_voters = np.random.randint(10, 50)
        num_candidates = np.random.randint(10, 20)
        culture_id = 'ic'

        election = mapel.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        assert type(election) is mapel.OrdinalElection

        election.object_type = 'vote'
        for distance_id in ['swap', 'spearman']:
            election.compute_distances(distance_id=distance_id)
            election.embed()
            election.print_map(show=False)

    def test_candidate_microscope(self):

        num_voters = np.random.randint(10, 50)
        num_candidates = np.random.randint(10, 20)
        culture_id = 'ic'

        election = mapel.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        assert type(election) is mapel.OrdinalElection

        election.object_type = 'candidate'
        for distance_id in ['domination', 'position']:
            election.compute_distances(distance_id=distance_id)
            election.embed()
            election.print_map(show=False)



