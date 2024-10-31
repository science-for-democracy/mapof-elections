
import mapof.elections as mapof


class TestOfflineOrdinalExperiment:

    def setup_method(self):
        self.experiment = mapof.prepare_offline_ordinal_experiment(experiment_id="test_id_soc")

    def test_prepare_elections(self):
        self.experiment.prepare_elections()

    def test_compute_distances(self):
        self.experiment.prepare_elections()
        self.experiment.compute_distances(distance_id="emd-positionwise")

    # def test_embed_2d(self):
    #     self.experiment.prepare_elections()
    #     self.experiment.compute_distances(distance_id="emd-positionwise")
    #     self.experiment.embed_2d(embedding_id="mds")
    #
    # def test_print_map_2d(self):
    #     self.experiment.prepare_elections()
    #     self.experiment.compute_distances(distance_id="emd-positionwise")
    #     self.experiment.embed_2d(embedding_id="mds")
    #     self.experiment.print_map_2d(show=False)

    def test_add_election(self):
        self.experiment.prepare_elections()

        self.experiment.add_election(
            election_id='test_election_id',
            culture_id="ic",
            num_candidates=10,
            num_voters=100
            )

    def test_add_family(self):
        self.experiment.prepare_elections()

        self.experiment.add_family(
            family_id='test_family_id',
            culture_id="ic",
            num_candidates=10,
            num_voters=100,
            size=3,
            )

    def test_pseud_election(self):
        self.experiment.prepare_elections()

        self.experiment.add_election(
            election_id='test_election_id_pseudo',
            culture_id="pseudo_uniformity",
            num_candidates=10,
            num_voters=100
            )