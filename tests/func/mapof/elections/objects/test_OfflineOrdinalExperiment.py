
import mapof.elections as mapof


class TestOfflineOrdinalExperiment:

    def setup_method(self):
        self.experiment = mapof.prepare_offline_ordinal_experiment(experiment_id="test_id")

    def test_prepare_eletions(self):
        self.experiment.prepare_elections()

    def test_compute_distances(self):
        self.experiment.prepare_elections()
        self.experiment.compute_distances(distance_id="emd-positionwise")

    # def test_embed_2d(self):
    #     self.experiment.prepare_elections()
    #     self.experiment.compute_distances(distance_id="emd-positionwise")
    #     self.experiment.embed_2d(embedding_id="kk")
    #
    # def test_print_map_2d(self):
    #     self.experiment.prepare_elections()
    #     self.experiment.compute_distances(distance_id="emd-positionwise")
    #     self.experiment.embed_2d(embedding_id="kk")
    #     self.experiment.print_map_2d(show=False)
