
import mapof.elections as mapof


class TestOnlineApprovalExperiment:

    def setup_method(self):
        """Set up the experiment instance for each test."""
        self.experiment = mapof.prepare_online_approval_experiment()

    def add_elections(self):
        self.experiment.add_election(
            culture_id='ic',
            num_candidates=10,
            num_voters=50,
            p=0.5
        )
        self.experiment.add_election(
            culture_id='id',
            num_candidates=10,
            num_voters=50,
            p=0.5
        )

    def add_families(self):
        """Helper method to add default families to the experiment."""
        self.experiment.add_family(
            culture_id='ic',
            num_candidates=10,
            num_voters=50,
            size=10,
            p=0.5,
            color='green',
            marker='x',
            label='IC'
        )

        self.experiment.add_family(
            culture_id='resampling',
            num_candidates=10,
            num_voters=50,
            size=10,
            phi=0.5,
            p=0.5,
            color='blue',
            marker='o',
            label='Resampling'
        )

    def test_experiment_creation(self):
        assert self.experiment is not None, "Experiment should be created successfully"

    def test_adding_elections(self):
        self.add_elections()
        assert self.experiment.num_elections == 2, "Two elections should be added"

    def test_adding_families(self):
        self.add_families()
        assert len(self.experiment.families) == 2, "Two families should be added"

    def test_computing_distances(self):
        self.add_families()
        self.experiment.compute_distances(distance_id='l1-approvalwise')
        assert self.experiment.distances is not None, "Distances should be computed"

    def test_embedding(self):
        self.add_families()
        self.experiment.compute_distances(distance_id='l1-approvalwise')
        self.experiment.embed_2d(embedding_id='kk')
        assert self.experiment.coordinates is not None, "Embedding should be performed"

    def test_print_map(self):
        self.add_families()
        self.experiment.compute_distances(distance_id='l1-approvalwise')
        self.experiment.embed_2d(embedding_id='kk')
        self.experiment.print_map_2d(show=False)

