import numpy as np

import mapof.elections as mapof


class TestOrdinalElection:

    def test_vote_microscope(self):

        num_voters = np.random.randint(10, 50)
        num_candidates = np.random.randint(10, 20)
        culture_id = 'ic'

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        assert type(election) is mapof.OrdinalElection

        election.object_type = 'vote'
        for distance_id in ['swap', 'spearman']:
            election.compute_distances(distance_id=distance_id, object_type='vote')
            election.embed(object_type='vote')
            election.print_map(show=False)

    def test_candidate_microscope(self):

        num_voters = np.random.randint(10, 50)
        num_candidates = np.random.randint(10, 20)
        culture_id = 'ic'

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        assert type(election) is mapof.OrdinalElection

        election.object_type = 'candidate'
        for distance_id in ['domination', 'position']:
            election.compute_distances(distance_id=distance_id)
            election.embed()
            election.print_map(show=False)

    def test_generate_ordinal_election_from_votes(self):

        votes = [[0,1,2,3], [1,2,0,3], [3,2,0,1]]
        election = mapof.generate_ordinal_election_from_votes(votes)

        assert election.num_voters == len(votes)
        assert election.num_candidates == len(votes[0])

    def test_is_condorcet_true(self):

        votes = [[0,1,2], [0,1,2], [2,1,0]]
        election = mapof.generate_ordinal_election_from_votes(votes)

        assert election.is_condorcet()

    def test_is_condorcet_false(self):

        votes = [[0,1,2], [1,2,0], [2,0,1]]
        election = mapof.generate_ordinal_election_from_votes(votes)

        assert not election.is_condorcet()

    def test_export_election_without_experiment(self):

        num_voters = np.random.randint(10, 50)
        num_candidates = np.random.randint(10, 20)
        culture_id = 'ic'

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   election_id='test_election',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
        path_to_folder = ''
        election.export_to_file(path_to_folder)

    def test_export_aggregated_election_without_experiment(self):

        num_voters = np.random.randint(10, 50)
        num_candidates = np.random.randint(10, 20)
        culture_id = 'ic'

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   election_id='test_election',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
        path_to_folder = ''
        election.export_to_file(path_to_folder, is_aggregated=True)

    def test_export_pseudo_ordinal_election(self):

        num_voters = np.random.randint(10, 50)
        num_candidates = np.random.randint(10, 20)
        culture_id = 'ic'

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   election_id='psuedo_uniformity',
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
        path_to_folder = ''
        election.export_to_file(path_to_folder)


