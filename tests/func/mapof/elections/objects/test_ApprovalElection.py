import pytest
import numpy as np

import mapof.elections as mapof

@pytest.fixture
def election_id():
    return "test_election"

@pytest.fixture
def num_voters():
  return np.random.randint(10, 20)

@pytest.fixture
def num_candidates():
  return np.random.randint(6, 12)

class TestApprovalElection:

    def test_vote_microscope(self, num_voters, num_candidates):
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

    def test_candidate_microscope(self, num_voters, num_candidates):
        culture_id = 'resampling'

        election = mapof.generate_approval_election(culture_id=culture_id,
                                                    num_voters=num_voters,
                                                    num_candidates=num_candidates,
                                                   params = {"phi": .4,
                                                             "p": .4})

        assert type(election) is mapof.ApprovalElection

        election.object_type = 'candidate'
        for distance_id in ['hamming', 'jaccard']:
            election.compute_distances(distance_id=distance_id)
            election.embed()
            election.print_map(show=False)

    def test_export_election_without_experiment(self, tmp_path, election_id, num_voters, num_candidates):
        culture_id = 'impartial'

        election = mapof.generate_approval_election(culture_id=culture_id,
                                                   election_id=election_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates)
        election.export_to_file(tmp_path)
        exported_file = tmp_path / f"{election_id}.{election.format}"
        assert exported_file.exists(), "Election without experiment exported"
        " incorrectly"

    def test_export_aggregated_election_without_experiment(self, tmp_path,
                                                           election_id, num_voters, num_candidates):
        culture_id = 'resampling'

        election = mapof.generate_approval_election(culture_id=culture_id,
                                                   election_id=election_id,
                                                   num_voters=num_voters,
                                                   num_candidates=num_candidates,
                                                   params = {"phi": 1,
                                                             "p": 1})
        election.export_to_file(tmp_path, is_aggregated=True)
        exported_file = tmp_path / f"{election_id}.{election.format}"
        assert exported_file.exists(), "Aggregated election without experiment exported"
        " incorrectly"
        with open(exported_file, 'r') as file_:
            for i, line in enumerate(file_, start=1):
                if i == 7:
                    str_num = line.split(":")[0]
                    assert int(str_num) > 1, "Aggregation did not work"





