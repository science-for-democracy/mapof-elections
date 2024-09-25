
import mapof.elections as mapof


class TestOfflineApprovalExperiment:

    def setup_method(self):
        self.experiment = mapof.prepare_offline_approval_experiment(experiment_id="test_id")

    def test_blank(self):
        pass
