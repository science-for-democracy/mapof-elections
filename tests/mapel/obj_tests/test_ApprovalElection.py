import numpy as np

import mapof.elections as mapel


class TestApprovalElection:

    def test_vote_microscope(self):

        num_voters = np.random.randint(10, 100)
        num_candidates = np.random.randint(10, 100)
        culture_id = 'resampling'

        election = mapel.generate_approval_election(culture_id=culture_id,
                                                    num_voters=num_voters,
                                                    num_candidates=num_candidates,
                                                    phi=0.4,
                                                    p=0.4)

        assert type(election) is mapel.ApprovalElection

        election.object_type = 'vote'
        election.compute_distances()
        election.embed()
        election.print_map(show=False)

    def test_candidate_microscope(self):

        num_voters = np.random.randint(10, 100)
        num_candidates = np.random.randint(10, 100)
        culture_id = 'resampling'

        election = mapel.generate_approval_election(culture_id=culture_id,
                                                    num_voters=num_voters,
                                                    num_candidates=num_candidates,
                                                    phi=0.4,
                                                    p=0.4)

        assert type(election) is mapel.ApprovalElection

        election.object_type = 'candidate'
        election.compute_distances()
        election.embed()
        election.print_map(show=False)



