from abc import ABC
from pathlib import Path

import mapof.elections.cultures as cultures
import mapof.elections.distances as distances
import mapof.elections.features as features
import mapof.elections.persistence.election_exports as exports
from mapof.elections.objects.ElectionExperiment import ElectionExperiment

try:
    from sklearn.manifold import MDS
    from sklearn.manifold import TSNE
    from sklearn.manifold import SpectralEmbedding
    from sklearn.manifold import LocallyLinearEmbedding
    from sklearn.manifold import Isomap
except ImportError as error:
    MDS = None
    TSNE = None
    SpectralEmbedding = None
    LocallyLinearEmbedding = None
    Isomap = None
    print(error)


class OrdinalElectionExperiment(ElectionExperiment, ABC):
    """Abstract set of elections."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_culture(self, name, function):
        cultures.add_ordinal_culture(name, function)

    def add_feature(self, name, function):
        features.add_ordinal_feature(name, function)

    def add_distance(self, name, function):
        distances.add_ordinal_distance(name, function)

    def add_folders_to_experiment(self) -> None:
        """
        Creates the folders within the experiment directory.

        Returns
        -------
            None
        """

        dirs = ["experiments"]
        for ddir in dirs:
            (Path.cwd() / ddir).mkdir(exist_ok=True)

        (Path.cwd() / "experiments" / self.experiment_id).mkdir(exist_ok=True)


        list_of_folders = ['distances',
                           'features',
                           'coordinates',
                           'elections']

        for folder_name in list_of_folders:
            to_check = Path.cwd() / "experiments" / self.experiment_id / folder_name
            to_check.mkdir(exist_ok=True)

        path = Path.cwd() / "experiments" / self.experiment_id / "map.csv"
        if not path.exists():
            with open(path, 'w') as file_csv:
                file_csv.write(
                    "size;num_candidates;num_voters;culture_id;params;family_id;"
                    "label;color;alpha;marker;ms;path;show\n"
                )

    def export_frequency_matrices(self) -> None:
        """

        Exports the frequency matrices of the election experiment.

        Returns
        -------
            None
        """
        exports.export_frequency_matrices(self)
