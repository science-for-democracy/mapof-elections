
import mapof.elections as mapof


class TestOfflineOrdinalExperiment:

    def setup_method(self):
        self.experiment = mapof.prepare_offline_ordinal_experiment(experiment_id="test_id")

    def test_blank(self):
        pass
