import numpy as np

import mapof.elections as mapof


class TestApprovalElection:

    def test_vote_microscope(self):

        num_voters = np.random.randint(10, 50)
        num_candidates = np.random.randint(10, 20)
        culture_id = 'resampling'

        election = mapof.generate_approval_election(culture_id=culture_id,
                                                    num_voters=num_voters,
                                                    num_candidates=num_candidates,
                                                    phi=0.4,
                                                    p=0.4)

        assert type(election) is mapof.ApprovalElection

        election.object_type = 'vote'
        for distance_id in ['hamming', 'jaccard']:
            election.compute_distances(distance_id=distance_id)
            election.embed()
            election.print_map(show=False)

    def test_candidate_microscope(self):

        num_voters = np.random.randint(10, 50)
        num_candidates = np.random.randint(10, 20)
        culture_id = 'resampling'

        election = mapof.generate_approval_election(culture_id=culture_id,
                                                    num_voters=num_voters,
                                                    num_candidates=num_candidates,
                                                    phi=0.4,
                                                    p=0.4)

        assert type(election) is mapof.ApprovalElection

        election.object_type = 'candidate'
        for distance_id in ['hamming', 'jaccard']:
            election.compute_distances(distance_id=distance_id)
            election.embed()
            election.print_map(show=False)

    def test_export_election_without_experiment(self):

        num_voters = np.random.randint(10, 50)
        num_candidates = np.random.randint(10, 20)
        culture_id = 'ic'

        election = mapof.generate_approval_election(culture_id=culture_id,
                                                   election_id='test_election',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
        path_to_folder = ''
        election.export_to_file(path_to_folder)

    def test_export_aggregated_election_without_experiment(self):

        num_voters = np.random.randint(10, 50)
        num_candidates = np.random.randint(10, 20)
        culture_id = 'ic'

        election = mapof.generate_approval_election(culture_id=culture_id,
                                                   election_id='test_election',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
        path_to_folder = ''
        election.export_to_file(path_to_folder, is_aggregated=True)




