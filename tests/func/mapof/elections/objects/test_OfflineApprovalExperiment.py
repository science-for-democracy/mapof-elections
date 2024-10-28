
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

    def test_priceability(self):
        self.experiment.prepare_elections()

        list_of_rules = ['av', 'sav']

        self.experiment.compute_rules(list_of_rules, committee_size=2, resolute=False)

        self.experiment.compute_rule_features(feature_id='priceability',
                                              list_of_rules=['av', 'sav'],
                                              feature_params={'committee_size': 2})

    def test_core(self):
        self.experiment.prepare_elections()

        list_of_rules = ['av', 'sav']

        self.experiment.compute_rules(list_of_rules, committee_size=2, resolute=False)

        self.experiment.compute_rule_features(feature_id='core',
                                              list_of_rules=['av', 'sav'],
                                              feature_params={'committee_size': 2})

    def test_ejr(self):
        self.experiment.prepare_elections()

        list_of_rules = ['av', 'sav']

        self.experiment.compute_rules(list_of_rules, committee_size=2, resolute=False)

        self.experiment.compute_rule_features(feature_id='ejr',
                                              list_of_rules=['av', 'sav'],
                                              feature_params={'committee_size': 2})
