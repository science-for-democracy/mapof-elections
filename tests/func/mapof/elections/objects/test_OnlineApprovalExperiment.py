import numpy as np
import pytest

import mapof.elections as mapof


@pytest.fixture
def experiment():
    return mapof.prepare_online_approval_experiment()


@pytest.fixture
def two_fam_experiment(experiment):

    def add_families():
        """Helper method to add default families to the experiment."""
        experiment.add_family(
            culture_id="impartial",
            num_candidates=10,
            num_voters=50,
            size=10,
            params={"p": 0.5},
            color="green",
            marker="x",
            label="IC",
        )

        experiment.add_family(
            culture_id="resampling",
            num_candidates=10,
            num_voters=50,
            size=10,
            params={"p": 0.5, "phi": 0.5},
            color="blue",
            marker="o",
            label="Resampling",
        )

    add_families()
    return experiment


class TestOnlineApprovalExperiment:

    def test_experiment_creation(self, experiment):
        assert experiment is not None, "Experiment should be created successfully"

    def test_adding_elections(self, experiment):
        experiment.add_election(
            culture_id="impartial", num_candidates=10, num_voters=50, params={"p": 0.5}
        )
        experiment.add_election(
            culture_id="identity", num_candidates=10, num_voters=50, params={"p": 0.5}
        )
        assert experiment.num_elections == 2, "Two elections should be added"

    def test_adding_families(self, two_fam_experiment):
        assert len(two_fam_experiment.families) == 2, "Two families should be added"

    def test_computing_distances(self, two_fam_experiment):
        two_fam_experiment.compute_distances(distance_id="l1-approvalwise")
        assert two_fam_experiment.distances is not None, "Distances should be computed"

    def test_embedding(self, two_fam_experiment):
        two_fam_experiment.compute_distances(distance_id="l1-approvalwise")
        two_fam_experiment.embed_2d(embedding_id="kk")
        assert (
            two_fam_experiment.coordinates is not None
        ), "Embedding should be performed"

    def test_print_map(self, two_fam_experiment):
        two_fam_experiment.compute_distances(distance_id="l1-approvalwise")
        two_fam_experiment.embed_2d(embedding_id="kk")
        two_fam_experiment.print_map_2d(show=False)

    def test_compute_rules(self, two_fam_experiment):
        list_of_rules = ["av", "sav"]

        two_fam_experiment.compute_rules(
            list_of_rules, committee_size=2, resolute=False
        )
