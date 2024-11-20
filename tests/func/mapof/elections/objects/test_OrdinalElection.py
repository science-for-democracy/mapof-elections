import pytest
import numpy as np

import mapof.elections as mapof


@pytest.fixture
def election_id():
    return "test_election_ord"


@pytest.fixture
def num_voters():
    return np.random.randint(10, 20)


@pytest.fixture
def num_candidates():
    return np.random.randint(6, 12)


class TestOrdinalElection:

    def test_vote_microscope(self, num_voters, num_candidates):
        culture_id = 'impartial'

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)

        assert type(election) is mapof.OrdinalElection

        election.object_type = 'vote'
        for distance_id in ['swap', 'spearman']:
            election.compute_distances(distance_id=distance_id, object_type='vote')
            election.embed(object_type='vote')
            election.print_map(show=False)

    def test_candidate_microscope(self, num_voters, num_candidates):
        culture_id = 'impartial'

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

        votes = [[0, 1, 2, 3], [1, 2, 0, 3], [3, 2, 0, 1]]
        election = mapof.generate_ordinal_election_from_votes(votes)

        assert election.num_voters == len(votes)
        assert election.num_candidates == len(votes[0])

    def test_is_condorcet_true(self):

        votes = [[0, 1, 2], [0, 1, 2], [2, 1, 0]]
        election = mapof.generate_ordinal_election_from_votes(votes)

        assert election.is_condorcet()

    def test_is_condorcet_false(self):

        votes = [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
        election = mapof.generate_ordinal_election_from_votes(votes)

        assert not election.is_condorcet()

    def test_export_election_without_experiment(self, num_voters,
                                                num_candidates, tmp_path,
                                                election_id):
        culture_id = 'impartial'

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   election_id=election_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
        election.export_to_file(tmp_path)
        exported_file = tmp_path / f"{election_id}.{election.format}"
        assert exported_file.exists(), "Election without experiment exported"
        " incorrectly"

    def test_export_aggregated_election_without_experiment(self, num_voters,
                                                           num_candidates,
                                                           tmp_path, election_id):
        culture_id = 'mallows'

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   election_id=election_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   params={"phi": 0})
        election.export_to_file(tmp_path, is_aggregated=True)
        exported_file = tmp_path / f"{election_id}.{election.format}"
        assert exported_file.exists(), "Aggregated election without experiment exported"
        " incorrectly"
        with open(exported_file, 'r') as file_:
            for i, line in enumerate(file_, start=1):
                if i == 7:
                    str_num = line.split(":")[0]
                    assert int(str_num) > 1, "Aggregation did not work"

    def test_export_pseudo_ordinal_election(self, num_voters, num_candidates,
                                            tmp_path, election_id):
        culture_id = 'impartial'

        election = mapof.generate_ordinal_election(culture_id=culture_id,
                                                   election_id=election_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
        election.export_to_file(tmp_path)
        exported_file = tmp_path / f"{election_id}.{election.format}"
        assert exported_file.exists(), "Pseudo election without experiment exported"
        " incorrectly"
        counter = 0
        with open(exported_file, 'r') as file_:
            for i, line in enumerate(file_, start=1):
                if i == 1:
                    filename = line.strip().split(":")[1]
                    assert filename == f" {election_id}.{election.format}", "Pseudo "
                    "export did not work well"
                if i > 6:
                    counter += 1
        assert counter == num_voters, "Pseudo export generated too few voters"
