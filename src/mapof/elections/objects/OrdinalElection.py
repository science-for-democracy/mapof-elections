import csv
import logging
import os
from collections import Counter

import numpy as np
from mapof.core.distances import swap_distance_between_potes, \
    spearman_distance_between_potes
from matplotlib import pyplot as plt

import mapof.elections.persistence.election_exports as exports
import mapof.elections.persistence.election_imports as imports
from mapof.elections.cultures import generate_ordinal_votes, \
    from_approval, generate_ordinal_alliance_votes
from mapof.elections.cultures.mallows import get_mallows_matrix
from mapof.elections.cultures.matrices.group_separable_matrices import get_gs_caterpillar_matrix
from mapof.elections.cultures.matrices.single_crossing_matrices import get_single_crossing_matrix
from mapof.elections.cultures.matrices.single_peaked_matrices import (
    get_conitzer_matrix,
    get_walsh_matrix,
)
from mapof.elections.cultures.pseudo_cultures import (
    get_frequency_matrix_for_guardian,
    get_pseudo_matrix_single,
    update_params_ordinal,
    get_pseudo_convex,
    get_pseudo_borda_vector,
    get_pseudo_multiplication,
)
from mapof.elections.features.simple_ordinal import is_condorcet
from mapof.elections.objects.Election import Election
from mapof.elections.other.glossary import PATHS
from mapof.elections.other.ordinal_rules import voting_rule


class OrdinalElection(Election):
    """ Ordinal Election class. """

    def __init__(self,
                 experiment_id=None,
                 election_id=None,
                 culture_id=None,
                 votes=None,
                 label=None,
                 num_voters: int = None,
                 num_candidates: int = None,
                 variable=None,
                 fast_import=False,
                 frequency_matrix=None,
                 params=None,
                 **kwargs):

        super().__init__(experiment_id=experiment_id,
                         election_id=election_id,
                         culture_id=culture_id,
                         votes=votes,
                         label=label,
                         num_voters=num_voters,
                         num_candidates=num_candidates,
                         fast_import=fast_import,
                         instance_type='ordinal',
                         params=params,
                         **kwargs)

        self.variable = variable
        self.frequency_matrix = []
        self.bordawise_vector = []
        self.potes = None
        self.condorcet = None
        self.points = {}
        self.alliances = {}
        self.quantities = None

        if frequency_matrix is not None:
            self.frequency_matrix = frequency_matrix

        if self.is_imported and self.experiment_id is not None:
            self.import_ordinal_election()

        self.try_updating_params()

    def import_ordinal_election(self):
        """ Import ordinal election. """

        try:
            self.is_pseudo = imports.check_if_pseudo(self.experiment_id, self.election_id)

            if self.is_pseudo:
                (
                    self.culture_id,
                    self.params,
                    self.num_voters,
                    self.num_candidates,
                    self.frequency_matrix
                ) = imports.import_pseudo_soc_election(
                    self.experiment_id,
                    self.election_id
                )
            else:
                (
                    self.votes,
                    self.num_voters,
                    self.num_candidates,
                    self.params,
                    self.culture_id,
                    self.alliances,
                    self.num_options,
                    self.quantities,
                    self.distinct_votes
                ) = imports.import_real_soc_election(
                    experiment_id=self.experiment_id,
                    election_id=self.election_id,
                    is_shifted=self.is_shifted)

                try:
                    self.points['voters'] = self.import_ideal_points('voters')
                    self.points['candidates'] = self.import_ideal_points('candidates')
                except Exception:
                    pass

            if not self.fast_import:
                self._votes_to_frequency_matrix()

        except Exception:
            pass

    def try_updating_params(self):
        if self.culture_id is not None:
            self.params = update_params_ordinal(
                self.params,
                self.culture_id,
                self.num_candidates
            )

    def get_frequency_matrix(self, is_recomputed=False):
        """ Get frequency_matrix. """
        if self.frequency_matrix is not None \
                and len(self.frequency_matrix) > 0 \
                and not is_recomputed:
            return self.frequency_matrix
        return self._votes_to_frequency_matrix()

    def get_bordawise_vector(self, is_recomputed=False):
        if self.bordawise_vector is not None \
                and len(self.bordawise_vector) > 0 \
                and not is_recomputed:
            return self.bordawise_vector
        return self._votes_to_bordawise_vector()

    def get_potes(self, is_recomputed=False):
        """ Get potes. """
        if self.potes is not None \
                and not is_recomputed:
            return self.potes
        return self.compute_potes()

    def _votes_to_frequency_matrix(self):
        """ Converts votes to positionwise frequency_matrix. """
        frequency_matrix = np.zeros([self.num_candidates, self.num_candidates])

        if self.is_pseudo and self.frequency_matrix is not None:
            frequency_matrix = self.frequency_matrix
        if self.culture_id == 'pseudo_single_peaked_conitzer':
            frequency_matrix = get_conitzer_matrix(self.num_candidates)
        elif self.culture_id == 'pseudo_single_peaked_walsh':
            frequency_matrix = get_walsh_matrix(self.num_candidates)
        elif self.culture_id == 'pseudo_single_crossing':
            frequency_matrix = get_single_crossing_matrix(self.num_candidates)
        elif self.culture_id == 'gs_caterpillar_matrix':
            frequency_matrix = get_gs_caterpillar_matrix(self.num_candidates)
        elif self.culture_id in {'norm_mallows_matrix', 'mallows_matrix_path'}:
            frequency_matrix = get_mallows_matrix(self.num_candidates, self.params)
        elif self.culture_id in {
            'pseudo_identity',
            'pseudo_uniformity',
            'pseudo_antagonism',
            'pseudo_stratification'
        }:
            frequency_matrix = get_frequency_matrix_for_guardian(
                self.culture_id,
                self.num_candidates,
                self.params,
            )
        elif self.culture_id in {'walsh_path', 'conitzer_path'}:
            frequency_matrix = get_pseudo_multiplication(
                self.num_candidates,
                self.params,
                self.culture_id)
        elif self.culture_id in PATHS:
            frequency_matrix = get_pseudo_convex(
                self.culture_id,
                self.num_candidates,
                self.params,
                get_frequency_matrix_for_guardian)
        elif self.culture_id in ['from_approval']:
            frequency_matrix = from_approval(
                num_candidates=self.num_candidates,
                num_voters=self.num_voters,
                params=self.params)
        else:
            for i in range(self.num_voters):
                pos = 0
                for j in range(self.num_candidates):
                    vote = self.votes[i][j]
                    if vote == -1:
                        continue
                    frequency_matrix[vote][pos] += 1
                    pos += 1
            for i in range(self.num_candidates):
                for j in range(self.num_candidates):
                    frequency_matrix[i][j] /= float(self.num_voters)

        self.frequency_matrix = frequency_matrix
        return frequency_matrix

    def votes_to_pairwise_matrix(self) -> np.ndarray:
        """ Convert votes to pairwise frequency_matrix. """
        matrix = np.zeros([self.num_candidates, self.num_candidates])
        if self.is_pseudo:
            if self.culture_id in {'identity', 'uniformity', 'antagonism', 'stratification'}:
                matrix = get_pseudo_matrix_single(self.culture_id, self.num_candidates)
            elif self.culture_id in PATHS:
                matrix = get_pseudo_convex(self.culture_id,
                                           self.num_candidates,
                                           self.params,
                                           get_pseudo_matrix_single)

        else:
            for v in range(self.num_voters):
                for c1 in range(self.num_candidates):
                    for c2 in range(c1 + 1, self.num_candidates):
                        matrix[int(self.votes[v][c1])][
                            int(self.votes[v][c2])] += 1
            for i in range(self.num_candidates):
                for j in range(i + 1, self.num_candidates):
                    matrix[i][j] /= float(self.num_voters)
                    matrix[j][i] = 1. - matrix[i][j]
        return matrix

    def _votes_to_bordawise_vector(self) -> np.ndarray:
        """ Convert ordinal votes to Borda vector. """
        borda_vector = np.zeros([self.num_candidates])
        if self.is_pseudo:
            if self.culture_id in {
                'pseudo_identity',
                'pseudo_uniformity',
                'pseudo_antagonism',
                'pseudo_stratification'
            }:
                borda_vector = get_pseudo_borda_vector(self.culture_id,
                                                       self.num_candidates,
                                                       self.num_voters)
            elif self.culture_id in PATHS:
                borda_vector = get_pseudo_convex(self.culture_id,
                                                 self.num_candidates,
                                                 self.params,
                                                 get_pseudo_borda_vector)
        else:
            c = self.num_candidates
            v = self.num_voters
            matrix = self._votes_to_frequency_matrix()
            borda_vector = [sum([matrix[i][j] * (c - j - 1) for j in range(c)]) * v for i in
                            range(self.num_candidates)]
            borda_vector = sorted(borda_vector, reverse=True)

        return np.array(borda_vector)

    def votes_to_voterlikeness_matrix(self, vote_distance='swap') -> np.ndarray:
        """ convert VOTES to voter-likeness MATRIX """
        matrix = np.zeros([self.num_voters, self.num_voters])
        self.compute_potes()

        for v1 in range(self.num_voters):
            for v2 in range(self.num_voters):
                if vote_distance == 'swap':
                    matrix[v1][v2] = swap_distance_between_potes(self.potes[v1], self.potes[v2])
                elif vote_distance == 'spearman':
                    matrix[v1][v2] = spearman_distance_between_potes(self.potes[v1], self.potes[v2])

        for i in range(self.num_voters):
            for j in range(i + 1, self.num_voters):
                matrix[j][i] = matrix[i][j]

        return matrix

    def votes_to_agg_voterlikeness_vector(self):
        """ Converts ordinal votes to Borda vector. """

        vector = np.zeros([self.num_voters])

        for v1 in range(self.num_voters):
            for v2 in range(self.num_voters):

                swap_distance = 0
                for i in range(self.num_candidates):
                    for j in range(i + 1, self.num_candidates):
                        if (self.potes[v1][i] > self.potes[v1][j] and
                            self.potes[v2][i] < self.potes[v2][j]) or \
                                (self.potes[v1][i] < self.potes[v1][j] and
                                 self.potes[v2][i] > self.potes[v2][j]):
                            swap_distance += 1
                vector[v1] += swap_distance

        return vector, len(vector)

    def compute_voting_rule(self, method=None, committee_size=None):
        self.winners = voting_rule(election=self, method=method, committee_size=committee_size)

    def compute_winners(self, **kwargs):  # deprecated name / for backward compatibility
        return self.compute_voting_rule(self, **kwargs)

    def prepare_instance(self, is_exported=None, is_aggregated=True):
        """ Prepares instance """
        if 'num_alliances' in self.params:
            self.votes, self.alliances = generate_ordinal_alliance_votes(
                culture_id=self.culture_id,
                num_candidates=self.num_candidates,
                num_voters=self.num_voters,
                params=self.params)
        else:
            self.votes = generate_ordinal_votes(culture_id=self.culture_id,
                                                num_candidates=self.num_candidates,
                                                num_voters=self.num_voters,
                                                params=self.params)
        if not self.is_pseudo:
            c = Counter(map(tuple, self.votes))
            counted_votes = [[count, list(row)] for row, count in c.items()]
            counted_votes = sorted(counted_votes, reverse=True)
            self.quantities = [a[0] for a in counted_votes]
            self.distinct_votes = [a[1] for a in counted_votes]
            self.num_options = len(counted_votes)
        else:
            self.quantities = [self.num_voters]
            self.num_options = 1

        if is_exported:
            exports.export_election_within_experiment(self, is_aggregated=is_aggregated)

    def compute_distances(self, distance_id='swap', object_type=None):
        """ Return: distances between votes """
        if object_type is None:
            object_type = self.object_type

        self.distinct_potes = convert_votes_to_potes(self.distinct_votes)
        self.num_dist_votes = len(self.distinct_votes)
        self.num_options = self.num_dist_votes

        if object_type == 'vote':
            distances = np.zeros([self.num_dist_votes, self.num_dist_votes])
            for v1 in range(self.num_dist_votes):
                for v2 in range(self.num_dist_votes):
                    if distance_id == 'swap':
                        distances[v1][v2] = swap_distance_between_potes(
                            self.distinct_potes[v1], self.distinct_potes[v2])
                    elif distance_id == 'spearman':
                        distances[v1][v2] = spearman_distance_between_potes(
                            self.distinct_potes[v1], self.distinct_potes[v2])
        elif object_type == 'candidate':
            self.compute_potes()
            if distance_id == 'domination':
                distances = self.votes_to_pairwise_matrix()
                distances = np.abs(distances - 0.5) * self.num_voters
                np.fill_diagonal(distances, 0)
            elif distance_id == 'position':
                distances = np.zeros([self.num_candidates, self.num_candidates])
                for c1 in range(self.num_candidates):
                    for c2 in range(self.num_candidates):
                        dist = 0
                        for pote in self.potes:
                            dist += abs(pote[c1] - pote[c2])
                        distances[c1][c2] = dist
        else:
            logging.warning('incorrect object_type')
            distances = []

        self.distances[object_type] = distances

        if self.is_exported:
            exports.export_distances(self, object_type=object_type)

    def is_condorcet(self):
        """ Check if election witness Condorcet winner"""
        if self.condorcet is None:
            self.condorcet = is_condorcet(self)['value']
        return self.condorcet

    def import_ideal_points(self, name):
        path = os.path.join(os.getcwd(), "experiments", self.experiment_id, "elections",
                            f'{self.election_id}_{name}.csv')
        points = []
        with open(path, 'r', newline='') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            for row in reader:
                points.append([float(row['x']), float(row['y'])])
        return points

    @staticmethod
    def texify_label(name):
        return name.replace('phi', '$\phi$'). \
            replace('alpha', '$\\ \\alpha$'). \
            replace('omega', '$\\ \\omega$'). \
            replace('§', '\n', 1). \
            replace('0.005', '$\\frac{1}{200}$'). \
            replace('0.025', '$\\frac{1}{40}$'). \
            replace('0.75', '$\\frac{3}{4}$'). \
            replace('0.25', '$\\frac{1}{4}$'). \
            replace('0.01', '$\\frac{1}{100}$'). \
            replace('0.05', '$\\frac{1}{20}$'). \
            replace('0.5', '$\\frac{1}{2}$'). \
            replace('0.1', '$\\frac{1}{10}$'). \
            replace('0.2', '$\\frac{1}{5}$'). \
            replace('0.4', '$\\frac{2}{5}$'). \
            replace('0.8', '$\\frac{4}{5}$'). \
            replace(' ', '\n', 1)

    def print_map(
            self,
            show=True,
            radius=None,
            alpha=0.1,
            s=30,
            object_type=None,
            double_gradient=False,
            saveas=None,
            color='blue',
            marker='o',
            title_size=20
    ):

        if object_type is None:
            object_type = self.object_type

        plt.figure(figsize=(6.4, 6.4))

        X = []
        Y = []
        for elem in self.coordinates[object_type]:
            X.append(elem[0])
            Y.append(elem[1])

        start = False
        if start:
            plt.scatter(X[0], Y[0],
                        color='sienna',
                        s=1000,
                        alpha=1,
                        marker='X')

        if object_type == 'vote':
            if double_gradient:
                for i in range(len(X)):
                    x = float(self.points['voters'][i][0])
                    y = float(self.points['voters'][i][1])
                    plt.scatter(X[i], Y[i], color=[0, y, x], s=s, alpha=alpha)
            else:
                for i in range(len(X)):
                    plt.scatter(X[i], Y[i], color=color, alpha=alpha, marker=marker,
                                s=self.quantities[i] * s)

        elif object_type == 'candidate':
            for i in range(len(X)):
                plt.scatter(X[i], Y[i], color=color, alpha=alpha, marker=marker,
                            s=s)

        avg_x = np.mean(X)
        avg_y = np.mean(Y)

        if radius:
            plt.xlim([avg_x - radius, avg_x + radius])
            plt.ylim([avg_y - radius, avg_y + radius])

        try:
            plt.title(self.texify_label(self.label), size=title_size)  # tmp
        except Exception:
            pass

        plt.axis('off')

        if saveas is not None:

            if saveas == 'default':

                path_to_folder = os.path.join(os.getcwd(), "images", self.experiment_id)
                if not os.path.isdir(path_to_folder):
                    os.mkdir(os.path.join(os.getcwd(), path_to_folder))

                saveas = f'{self.label}_{object_type}'

            file_name = os.path.join(os.getcwd(), "images", self.experiment_id, f'{saveas}.png')
            plt.savefig(file_name, bbox_inches='tight', dpi=100)

        if show:
            plt.show()
        else:
            plt.clf()

        plt.close()


def convert_votes_to_potes(votes) -> np.array:
    """ Converts votes to positional votes (called potes) """
    return np.array([[list(vote).index(i) for i, _ in enumerate(vote)]
                     for vote in votes])
