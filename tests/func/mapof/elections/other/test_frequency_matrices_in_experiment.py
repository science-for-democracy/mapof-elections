import pytest 
import pathlib

import mapof.elections as mapof

@pytest.fixture
def exp_id():
  return "test_id"

@pytest.fixture
def experiment(mocker, tmp_path, exp_id):
    mocker.patch("os.getcwd", return_value=str(tmp_path))
    mocker.patch("pathlib.Path.cwd", return_value=tmp_path)
    experiment = mapof.prepare_offline_ordinal_experiment(experiment_id=exp_id)
    experiment.prepare_elections()
    return experiment

class TestExportingMatricesOrdinalExperiment:

    def test_export_frequency_matrices(self, experiment, exp_id):
        experiment.export_frequency_matrices()
        matrices_dir = pathlib.Path.cwd() / "experiments" / exp_id / "matrices"
        assert matrices_dir.exists(), "Matrices not exported properly"


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
