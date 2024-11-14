import pytest

import mapof.elections as mapof


@pytest.fixture(autouse=True)
def mock_path(mocker, tmp_path):
    mocker.patch("os.getcwd", return_value=str(tmp_path))
    mocker.patch("pathlib.Path.cwd", return_value=tmp_path)


@pytest.fixture
def offline_experiment():
    return mapof.prepare_offline_approval_experiment(experiment_id="test_id_app")


@pytest.fixture
def prepared_elections(offline_experiment):
    offline_experiment.prepare_elections()
    return offline_experiment


@pytest.fixture
def list_of_rules():
    return ['av', 'sav']

@pytest.fixture
def feature_params():
    return {'committee_size' : 2}


class TestOfflineApprovalExperiment:

    def test_compute_distances(self, prepared_elections):
        prepared_elections.compute_distances(distance_id="l1-approvalwise")

    # def test_embed_2d(self, prepared_elections):
    #     prepared_elections.compute_distances(distance_id="l1-approvalwise")
    #     prepared_elections.embed_2d(embedding_id="kk")
    #
    # def test_print_map_2d(self, prepared_elections):
    #     prepared_elections.compute_distances(distance_id="l1-approvalwise")
    #     prepared_elections.embed_2d(embedding_id="kk")
    #     prepared_elections.print_map_2d(show=False)

    def test_compute_rules(self, prepared_elections, list_of_rules):
        prepared_elections.compute_rules(list_of_rules, committee_size=2, resolute=False)

    def test_priceability(self, prepared_elections, list_of_rules,
                           feature_params):
        prepared_elections.compute_rules(list_of_rules, committee_size=2, resolute=False)

        prepared_elections.compute_rule_features(feature_id='priceability',
                                              list_of_rules=list_of_rules,
                                              feature_params=feature_params)

    def test_core(self, prepared_elections, list_of_rules,
                           feature_params):
        prepared_elections.compute_rules(list_of_rules, committee_size=2, resolute=False)

        prepared_elections.compute_rule_features(feature_id='core',
                                              list_of_rules=list_of_rules,
                                              feature_params=feature_params)

    def test_ejr(self, prepared_elections, list_of_rules,
                           feature_params):
        prepared_elections.compute_rules(list_of_rules, committee_size=2, resolute=False)

        prepared_elections.compute_rule_features(feature_id='ejr',
                                              list_of_rules=list_of_rules,
                                              feature_params=feature_params)

    # def test_distance_between_voting_rules(self):
    #     prepared_elections.prepare_elections()
    #
    #     list_of_rules = ['av', 'sav']
    #
    #     prepared_elections.compute_rules(list_of_rules, committee_size=2, resolute=False)
    #
    #     prepared_elections.compute_distance_between_rules(
    #         list_of_rules=['av', 'sav'],
    #         distance_id='hamming',
    #         committee_size=2)

    def test_election_import(self):
        prepared_elections = \
        mapof.prepare_offline_approval_experiment(experiment_id="test_id_app")
