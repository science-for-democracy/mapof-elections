import pytest

import mapof.elections as mapof

@pytest.fixture(autouse=True)
def mock_path(mocker, tmp_path):
    mocker.patch("os.getcwd", return_value=str(tmp_path))
    mocker.patch("pathlib.Path.cwd", return_value=tmp_path)

@pytest.fixture
def offline_experiment():
    return mapof.prepare_offline_ordinal_experiment(experiment_id="test_id_soc")


@pytest.fixture
def prepared_elections(offline_experiment):
    offline_experiment.prepare_elections()
    return offline_experiment


class TestOfflineOrdinalExperiment:

    def test_compute_distances(self, prepared_elections):
        prepared_elections.compute_distances(distance_id="emd-positionwise")

    # def test_embed_2d(self, prepared_elections):
    #     prepared_elections.compute_distances(distance_id="emd-positionwise")
    #     prepared_elections.embed_2d(embedding_id="mds")
    #
    # def test_print_map_2d(self, prepared_elections):
    #     prepared_elections.compute_distances(distance_id="emd-positionwise")
    #     prepared_elections.embed_2d(embedding_id="mds")
    #     prepared_elections.print_map_2d(show=False)

    def test_add_election(self, prepared_elections):
        prepared_elections.add_election(
            election_id='test_election_id',
            culture_id="impartial",
            num_candidates=10,
            num_voters=100
            )
        assert len(prepared_elections.families) == 1

    def test_add_family(self, prepared_elections):
        prepared_elections.add_family(
            family_id='test_family_id',
            culture_id="impartial",
            num_candidates=10,
            num_voters=100,
            size=3,
            )
        assert len(prepared_elections.families) == 1

    def test_pseud_election(self, prepared_elections):
        prepared_elections.add_election(
            election_id='test_election_id_pseudo',
            culture_id="pseudo_uniformity",
            num_candidates=10,
            num_voters=100
            )
        assert len(prepared_elections.families) == 1

    def test_election_import(self):
        self.experiment = mapof.prepare_offline_ordinal_experiment(experiment_id="test_id_soc")
