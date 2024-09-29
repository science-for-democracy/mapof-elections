
import mapof.elections as mapof


class TestOnlineOrdinalExperiment:

    def setup_method(self):
        """Set up the experiment instance for each test."""
        self.experiment = mapof.prepare_online_ordinal_experiment()

    def add_elections(self):
        self.experiment.add_election(
            culture_id='ic',
            num_candidates=5,
            num_voters=50
        )
        self.experiment.add_election(
            culture_id='urn',
            num_candidates=5,
            num_voters=50,
            alpha=0.1
        )

    def add_families(self):
        """Helper method to add default families to the experiment."""
        self.experiment.add_family(
            culture_id='ic',
            num_candidates=5,
            num_voters=10,
            size=10,
            color='green',
            marker='x',
            label='IC'
        )

        self.experiment.add_family(
            culture_id='norm-mallows',
            num_candidates=5,
            num_voters=10,
            size=10,
            normphi=0.5,
            color='blue',
            marker='o',
            label='Norm-Mallows'
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
        self.experiment.compute_distances(distance_id='emd-positionwise')
        assert self.experiment.distances is not None, "Distances should be computed"

    def test_embedding(self):
        self.add_families()
        self.experiment.compute_distances(distance_id='emd-positionwise')
        self.experiment.embed_2d(embedding_id='fr')
        assert self.experiment.coordinates is not None, "Embedding should be performed"

    def test_print_map(self):
        self.add_families()
        self.experiment.compute_distances(distance_id='emd-positionwise')
        self.experiment.embed_2d(embedding_id='fr')
        self.experiment.print_map_2d(show=True)

    def test_compute_feature(self):
        self.add_families()
        self.experiment.compute_distances(distance_id='emd-positionwise')
        self.experiment.embed_2d(embedding_id='fr')

        feature_id = 'highest_borda_score'
        self.experiment.compute_feature(feature_id=feature_id)

    def test_print_map_colored_by_feature(self):
        self.add_families()
        self.experiment.compute_distances(distance_id='emd-positionwise')
        self.experiment.embed_2d(embedding_id='fr')

        feature_id = 'highest_borda_score'
        self.experiment.compute_feature(feature_id=feature_id)
        self.experiment.print_map_2d_colored_by_feature(
            show=True,
            feature_id=feature_id,
            upper_limit=100,
            lower_limit=0,
            rounding=0)





