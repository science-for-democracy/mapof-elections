
import mapof.elections as mapof


class TestOfflineApprovalExperiment:

    def setup_method(self):
        self.experiment = mapof.prepare_offline_approval_experiment(experiment_id="test_id")

    def test_prepare_eletions(self):
        self.experiment.prepare_elections()

    def test_compute_distances(self):
        self.experiment.prepare_elections()
        self.experiment.compute_distances(distance_id="l1-approvalwise")

    # def test_embed_2d(self):
    #     self.experiment.prepare_elections()
    #     self.experiment.compute_distances(distance_id="l1-approvalwise")
    #     self.experiment.embed_2d(embedding_id="kk")
    #
    # def test_print_map_2d(self):
    #     self.experiment.prepare_elections()
    #     self.experiment.compute_distances(distance_id="l1-approvalwise")
    #     self.experiment.embed_2d(embedding_id="kk")
    #     self.experiment.print_map_2d(show=False)

    def test_compute_rules(self):
        self.experiment.prepare_elections()

        list_of_rules = ['av', 'sav']

        self.experiment.compute_rules(list_of_rules, committee_size=2, resolute=False)