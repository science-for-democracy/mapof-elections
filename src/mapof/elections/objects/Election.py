import copy
import csv
import itertools
import logging
import math
import os
from abc import abstractmethod

import matplotlib.pyplot as plt
import numpy as np

from mapof.core.distances import l2
from mapof.core.objects.Instance import Instance
from sklearn.manifold import MDS

import mapof.elections.persistence.election_exports as exports
import mapof.elections.persistence.election_imports as imports
from mapof.elections.features import get_local_feature
from mapof.elections.objects.ElectionFeatures import ElectionFeatures
from mapof.elections.other.glossary import is_pseudo_culture
from mapof.elections.other.ordinal_rules import (
    compute_sntv_voting_rule,
    compute_borda_voting_rule,
    compute_stv_voting_rule
)

from sklearn.decomposition import PCA


from mapof.elections.other.approval_rules import compute_abcvoting_rule_for_single_election


OBJECT_TYPES = ['vote', 'candidate']


class Election(Instance):
    """ (Abstract) Election class. """

    def __init__(self,
                 experiment_id=None,
                 election_id=None,
                 culture_id=None,
                 votes=None,
                 instance_type: str = None,
                 num_voters: int = None,
                 num_candidates: int = None,
                 label=None,
                 fast_import=False,
                 is_shifted=False,
                 is_imported=False,
                 is_exported=True,
                 params=None,
                 **kwargs):

        super().__init__(experiment_id=experiment_id,
                         instance_id=election_id,
                         culture_id=culture_id,
                         params=params,
                         **kwargs)

        self.instance_type = instance_type
        self.format = get_format_from_instance_type(instance_type)
        self.election_id = election_id
        self.label = label
        self.num_voters = num_voters
        self.num_candidates = num_candidates
        self.votes = votes
        self.is_exported = is_exported
        self.winners = None
        self.alternative_winners = {}
        self.is_pseudo = is_pseudo_culture(culture_id)
        self.potes = None
        self.features = {}
        self.object_type = 'vote'
        self.points = {}
        self.is_shifted = is_shifted
        self.is_imported = is_imported
        self.fast_import = fast_import
        self.winning_committee = {}
        self.election_features = ElectionFeatures(election_id)

        self.distances = {}
        self.import_distances()

        self.coordinates = {}
        self.import_coordinates()

    def import_distances(self) -> None:
        """
        Imports distances from a .csv file.

        Returns
        -------
            None
        """
        if not self.fast_import:
            for object_type in OBJECT_TYPES:
                try:
                    self.distances[object_type] = \
                        imports.import_distances(self.experiment_id, self.election_id, object_type)
                except Exception:
                    pass

    def import_coordinates(self) -> None:
        """
        Imports coordinates from a .csv file.

        Returns
        -------
            None
        """
        for object_type in OBJECT_TYPES:
            try:
                self.coordinates[object_type] = \
                    imports.import_coordinates(self.experiment_id, self.election_id, object_type)
            except Exception:
                pass

    def get_distances(self, object_type):
        try:
            return self.distances[object_type]
        except Exception:
            self.distances[object_type] = \
                imports.import_distances(self.experiment_id, self.election_id, object_type)
            return self.distances[object_type]

    def get_coordiantes(self, object_type):
        try:
            return self.coordinates[object_type]
        except Exception:
            self.coordinates[object_type] = \
                imports.import_coordinates(self.experiment_id, self.election_id, object_type)
            return self.coordinates[object_type]

    def set_default_object_type(self, object_type):
        self.object_type = object_type

    def import_matrix(self) -> np.ndarray:
        file_name = f'{self.election_id}.csv'
        path = os.path.join(os.getcwd(), "experiments", self.experiment_id, 'matrices', file_name)
        matrix = np.zeros([self.num_candidates, self.num_candidates])

        with open(path, 'r', newline='') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            for i, row in enumerate(reader):
                for j, candidate_id in enumerate(row):
                    matrix[i][j] = row[candidate_id]
        return matrix

    def compute_potes(self, mapping=None):
        """ Convert votes to positional votes (called potes) """
        if not self.is_pseudo:
            if mapping is None:
                self.potes = np.array([[list(vote).index(i) for i, _ in enumerate(vote)]
                                       for vote in self.votes])
            else:
                self.potes = np.array([[list(vote).index(mapping[i]) for i, _ in enumerate(vote)]
                                       for vote in self.votes])
            return self.potes

    def vector_to_interval(self, vector, precision=None) -> list:
        # discreet version for now
        interval = []
        w = int(precision / self.num_candidates)
        for i in range(self.num_candidates):
            for j in range(w):
                interval.append(vector[i] / w)
        return interval

    def compute_alternative_winners(self, method=None, party_id=None, committee_size=None):

        election_without_party_id = _remove_candidate_from_election(copy.deepcopy(self),
                                                                    party_id, committee_size)
        election_without_party_id = map_the_votes(election_without_party_id, party_id, committee_size)

        if method == 'sntv':
            winners_without_party_id = compute_sntv_voting_rule(
                election=election_without_party_id, committee_size=committee_size)
        elif method == 'borda':
            winners_without_party_id = compute_borda_voting_rule(
                election=election_without_party_id, committee_size=committee_size)
        elif method == 'stv':
            winners_without_party_id = compute_stv_voting_rule(
                election=election_without_party_id, committee_size=committee_size)
        else:
            winners_without_party_id = []

        self.alternative_winners[party_id] = _unmap_the_winners(winners_without_party_id, party_id,
                                                                committee_size)

    @abstractmethod
    def compute_distances(self):
        pass

    def embed(self, algorithm='mds', object_type=None):

        if object_type is None:
            object_type = self.object_type

        if algorithm.lower() == 'pca':
            pca = PCA(n_components=2)
            self.coordinates[object_type] = pca.fit_transform(self.distances[object_type])
        elif algorithm.lower() == 'mds':
            MDS_object = MDS(n_components=2,
                             dissimilarity='precomputed',
                             normalized_stress='auto')
            self.coordinates[object_type] = MDS_object.fit_transform(self.distances[object_type])
        else:
            logging.warning('No such algorithm!')

        if not self.all_dist_zeros(object_type):
            dist = np.zeros(
                [len(self.coordinates[object_type]), len(self.coordinates[object_type])])
            for pos_1, pos_2 in itertools.combinations(
                    [i for i in range(len(self.coordinates[object_type]))],
                    2):
                dist[pos_1][pos_2] = l2(self.coordinates[object_type][pos_1],
                                        self.coordinates[object_type][pos_2])

            result = np.where(dist == np.amax(dist))
            id_1 = result[0][0]
            id_2 = result[1][0]

            # rotate
            a = id_1
            b = id_2

            try:
                d_x = self.coordinates[object_type][a][0] - self.coordinates[object_type][b][0]
                d_y = self.coordinates[object_type][a][1] - self.coordinates[object_type][b][1]
                alpha = math.atan(d_x / d_y)
                self.rotate(alpha - math.pi / 2., object_type)
                self.rotate(math.pi / 4., object_type)
            except Exception:
                pass

            # PUT heavier corner in the left lower part
            if self.coordinates[object_type][a][0] < self.coordinates[object_type][b][0]:
                left = a
                right = b
            else:
                left = b
                right = a
            try:
                left_ctr = 0
                right_ctr = 0
                for v in range(len(self.coordinates[object_type])):
                    d_left = l2(self.coordinates[object_type][left],
                                self.coordinates[object_type][v])
                    d_right = l2(self.coordinates[object_type][right],
                                 self.coordinates[object_type][v])
                    if d_left < d_right:
                        left_ctr += 1
                    else:
                        right_ctr += 1

                if left_ctr < right_ctr:
                    self.rotate(math.pi, object_type)

            except Exception:
                pass

        if self.is_exported and self.experiment_id is not None:
            exports.export_coordinates(self, object_type=object_type)

    def all_dist_zeros(self, object_type):
        if np.abs(self.distances[object_type]).sum():
            return False
        else:
            return True

    @staticmethod
    def rotate_point(cx, cy, angle, px, py) -> (float, float):
        """ Rotate two-dimensional point by an angle """
        s, c = math.sin(angle), math.cos(angle)
        px -= cx
        py -= cy
        x_new, y_new = px * c - py * s, px * s + py * c
        px, py = x_new + cx, y_new + cy

        return px, py

    def rotate(self, angle, object_type) -> None:
        """ Rotate all the points by a given angle """
        for instance_id in range(len(self.coordinates[object_type])):
            self.coordinates[object_type][instance_id][0], \
            self.coordinates[object_type][instance_id][1] = \
                self.rotate_point(0.5, 0.5, angle, self.coordinates[object_type][instance_id][0],
                                  self.coordinates[object_type][instance_id][1])

    def compute_feature(self, feature_id, feature_long_id=None, **kwargs):
        if feature_long_id is None:
            feature_long_id = feature_id
        feature = get_local_feature(feature_id)
        self.features[feature_long_id] = feature(self, **kwargs)

    def compute_rule(self, rule_id, **kwargs):
        compute_abcvoting_rule_for_single_election(self, rule_id, **kwargs)

    def get_feature(self,
                    feature_id,
                    feature_long_id=None,
                    overwrite=False,
                    **kwargs):
        if feature_long_id is None:
            feature_long_id = feature_id
        if feature_id not in self.features or overwrite:
            self.compute_feature(feature_id, feature_long_id, **kwargs)
        return self.features[feature_long_id]

    def export_to_file(self, path_to_folder, is_aggregated=False):
        return exports.export_election_without_experiment(self, path_to_folder, is_aggregated)


def map_the_votes(election, party_id, party_size) -> Election:
    new_votes = [[] for _ in range(election.num_voters)]
    for i in range(election.num_voters):
        for j in range(election.num_candidates):
            if election.votes[i][j] >= party_id * party_size:
                new_votes[i].append(election.votes[i][j] - party_size)
            else:
                new_votes[i].append(election.votes[i][j])
    election.votes = new_votes
    return election


def _unmap_the_winners(winners, party_id, party_size):
    new_winners = []
    for j in range(len(winners)):
        if winners[j] >= party_id * party_size:
            new_winners.append(winners[j] + party_size)
        else:
            new_winners.append(winners[j])
    return new_winners


def _remove_candidate_from_election(election, party_id, party_size) -> Election:
    for vote in election.votes:
        for i in range(party_size):
            _id = party_id * party_size + i
            vote.remove(_id)
    election.num_candidates -= party_size
    return election


def get_format_from_instance_type(instance_type):
    if instance_type == 'approval':
        return 'app'
    elif instance_type == 'ordinal':
        return 'soc'
