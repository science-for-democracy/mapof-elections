#!/usr/bin/env python
import csv
import os
from abc import ABC

from mapof.elections.objects.ElectionExperiment import ElectionExperiment

import mapof.elections.cultures as cultures
import mapof.elections.features as features
import mapof.elections.distances as distances

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

        dirs = ["experiments"]
        for dir in dirs:
            if not os.path.isdir(dir):
                os.mkdir(os.path.join(os.getcwd(), dir))

        if not os.path.isdir(os.path.join(os.getcwd(), "experiments", self.experiment_id)):
            os.mkdir(os.path.join(os.getcwd(), "experiments", self.experiment_id))

        list_of_folders = ['distances',
                           'features',
                           'coordinates',
                           'elections']

        for folder_name in list_of_folders:
            if not os.path.isdir(os.path.join(os.getcwd(), "experiments",
                                              self.experiment_id, folder_name)):
                os.mkdir(os.path.join(os.getcwd(), "experiments",
                                      self.experiment_id, folder_name))

        path = os.path.join(os.getcwd(), "experiments", self.experiment_id, "map.csv")
        if not os.path.exists(path):

            with open(path, 'w') as file_csv:
                file_csv.write(
                    "size;num_candidates;num_voters;culture_id;params;color;alpha;"
                    "family_id;label;marker\n")
                file_csv.write("3;10;100;ic;{};black;1;ic;Impartial Culture;o\n")

    def export_frequency_matrices(self):
        path_to_folder = os.path.join(os.getcwd(), "experiments", self.experiment_id, "matrices")

        if not os.path.exists(path_to_folder):
            os.makedirs(path_to_folder)

        for file_name in os.listdir(path_to_folder):
            os.remove(os.path.join(path_to_folder, file_name))

        for election_id in self.elections:
            frequency_matrix = self.elections[election_id].get_frequency_matrix()
            file_name = election_id + ".csv"

            path_to_file = os.path.join(path_to_folder, file_name)
            with open(path_to_file, 'w', newline='') as csv_file:

                writer = csv.writer(csv_file, delimiter=';')
                for row in frequency_matrix:
                    writer.writerow(row)
