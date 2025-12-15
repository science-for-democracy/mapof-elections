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
    generate_ordinal_alliance_votes, registered_pseudo_ordinal_cultures
from mapof.elections.cultures.pseudo_cultures import (
    get_frequency_matrix_for_guardian,
    get_pairwise_matrix_for_guardian,
    update_params_ordinal,
    get_pseudo_convex,
    get_pseudo_borda_vector,
)
from mapof.elections.features.simple_ordinal import is_condorcet
from mapof.elections.objects.Election import Election
from mapof.elections.objects.Microscope import Microscope
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
                 fast_import=False,
                 frequency_matrix=None,
                 params=None,
                 **kwargs):

        """Create an OrdinalElection instance.

        Parameters
        ----------
        experiment_id : str or None
            Identifier of the parent experiment (used for persistence).
        election_id : str or None
            Identifier of this election instance.
        culture_id : str or None
            Identifier of the generating culture (may be a pseudo-culture).
        votes : list or None
            Raw votes as lists/tuples of candidate indices.
        label : str or None
            Human-readable label for plotting/export.
        num_voters : int or None
            Number of voters in the election.
        num_candidates : int or None
            Number of candidates in the election.
        fast_import : bool
            If True, skip expensive import steps when constructing the object.
        frequency_matrix : array-like or None
            Precomputed frequency matrix (used for pseudo cultures).
        params : dict or None
            Culture or generation parameters.
        **kwargs : dict
            Additional keyword arguments forwarded to the base class.
        """

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

        self.frequency_matrix = []
        self.bordawise_vector = []
        self.potes = None
        self.condorcet = None
        self.points = {}
        self.alliances = {}
        self.quantities = None
        self.microscope = None

        if frequency_matrix is not None:
            self.frequency_matrix = frequency_matrix

        if self.is_imported and self.experiment_id is not None and not fast_import:
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
                ) = imports.import_pseudo_ordinal_election(
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
                    self.num_distinct_votes,
                    self.quantities,
                    self.distinct_votes
                ) = imports.import_ordinal_election(
                    experiment_id=self.experiment_id,
                    election_id=self.election_id,
                    is_shifted=self.is_shifted)

                if not self.fast_import:
                    self._votes_to_frequency_matrix()

        except Exception:
            logging.warning(f'Could not import instance {self.election_id}.')

    def try_updating_params(self):
        """Update `self.params` based on `culture_id` when available.

        This uses culture-specific logic (e.g. pseudo-cultures) to ensure params
        are consistent with the number of candidates.
        """
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
        """Return the Borda-style vector for the election, computing it if needed.

        Parameters
        ----------
        is_recomputed : bool
            If True, force recomputation even if a cached value exists.
        """
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
        """ Converts votes to a frequency matrix. """
        frequency_matrix = np.zeros([self.num_candidates, self.num_candidates])

        if self.is_pseudo and self.frequency_matrix is not None:
            frequency_matrix = self.frequency_matrix

        if self.culture_id in PATHS:
            frequency_matrix = get_pseudo_convex(
                self.culture_id,
                self.num_candidates,
                self.params,
                get_frequency_matrix_for_guardian
            )
        elif self.culture_id in registered_pseudo_ordinal_cultures:
            frequency_matrix = registered_pseudo_ordinal_cultures[self.culture_id](
                self.num_candidates,
                params=self.params,
            )
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
        """ Convert votes to pairwise matrix. """
        matrix = np.zeros([self.num_candidates, self.num_candidates])
        if self.is_pseudo:
            if self.culture_id in {
                'pseudo_identity',
                'pseudo_uniformity',
                'pseudo_antagonism',
                'pseudo_stratification'
            }:
                matrix = get_pairwise_matrix_for_guardian(self.culture_id, self.num_candidates)
            elif self.culture_id in PATHS:
                matrix = get_pseudo_convex(self.culture_id,
                                           self.num_candidates,
                                           self.params,
                                           get_pairwise_matrix_for_guardian)

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
        """Compute winners using the given voting rule and return them.

        This sets `self.winners` (existing behavior) and also returns the winners
        for convenience so callers can do `w = obj.compute_voting_rule(...)`.
        """
        self.winners = voting_rule(election=self, method=method, committee_size=committee_size)
        return self.winners

    def compute_winners(self, **kwargs):  # deprecated name / for backward compatibility
        # old callers used compute_winners(method=..., committee_size=...)
        # emit a deprecation warning and forward kwargs to compute_voting_rule
        import warnings
        warnings.warn(
            "OrdinalElection.compute_winners is deprecated, use compute_voting_rule instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.compute_voting_rule(**kwargs)

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
            self.num_distinct_votes = len(counted_votes)
        else:
            self.quantities = [self.num_voters]
            self.num_distinct_votes = 1

        if is_exported:
            exports.export_election_within_experiment(self, is_aggregated=is_aggregated)

    def compute_distances(self, distance_id='swap', object_type=None):
         """ Return: distances between votes """
         if object_type is None:
             object_type = self.object_type

         # Ensure distances is always defined regardless of branches below.
         distances = []

         self.distinct_potes = convert_votes_to_potes(self.distinct_votes)
         self.num_dist_votes = len(self.distinct_votes)
         self.num_distinct_votes = self.num_dist_votes

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
        """Import ideal points from a CSV file.

        The file is expected to have two columns (x, y) without a header.

        Parameters
        ----------
        name : str
            Base name of the file to import (without path or extension).

        Returns
        -------
        list of [float, float]
            List of ideal points as [x, y] coordinates.
        """
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
        """Convert a label string to a TeX-friendly format.

        This is used for rendering labels in plots with proper mathematical formatting.

        Parameters
        ----------
        name : str
            The label string to convert.

        Returns
        -------
        str
            The converted label string, suitable for use in TeX/LaTeX.
        """
        result = name
        result = result.replace('phi', '$\\ \\phi$')
        result = result.replace('alpha', '$\\ \\alpha$')
        result = result.replace('omega', '$\\ \\omega$')
        result = result.replace('§', '\n', 1)
        result = result.replace('0.005', '$\\frac{1}{200}$')
        result = result.replace('0.025', '$\\frac{1}{40}$')
        result = result.replace('0.75', '$\\frac{3}{4}$')
        result = result.replace('0.25', '$\\frac{1}{4}$')
        result = result.replace('0.01', '$\\frac{1}{100}$')
        result = result.replace('0.05', '$\\frac{1}{20}$')
        result = result.replace('0.5', '$\\frac{1}{2}$')
        result = result.replace('0.1', '$\\frac{1}{10}$')
        result = result.replace('0.2', '$\\frac{1}{5}$')
        result = result.replace('0.4', '$\\frac{2}{5}$')
        result = result.replace('0.8', '$\\frac{4}{5}$')
        return result.replace(' ', '\n', 1)

    def set_microscope(
            self,
            radius=None,
            alpha=0.1,
            s=30,
            object_type=None,
            double_gradient=False,
            color='blue',
            marker='o',
            title_size=20
    ):
        """Set up a Microscope (2D scatter plot) for visualizing election data.

        This method configures and saves a Microscope object to `self.microscope`,
        which can be used for detailed inspection of the election's spatial properties.

        Parameters
        ----------
        radius : float or None
            If given, set the x and y limits of the plot to be centered around the
            average coordinates with this radius.
        alpha : float
            Transparency level for the points in the scatter plot.
        s : int
            Base size for the points in the scatter plot (scaled by voter quantity).
        object_type : str or None
            Type of objects to plot ('vote' or 'candidate'). If None, inferred from
            `self.object_type`.
        double_gradient : bool
            If True, use a double gradient based on voter coordinates for coloring.
        color : str
            Base color for the points in the scatter plot.
        marker : str
            Marker style for the points in the scatter plot.
        title_size : int
            Font size for the title of the plot.

        Returns
        -------
        Microscope
            The configured Microscope object.
        """
        if object_type is None:
            object_type = self.object_type

        fig, ax = plt.subplots(figsize=(6.4, 6.4))

        X = []
        Y = []
        for elem in self.coordinates[object_type]:
            X.append(elem[0])
            Y.append(elem[1])

        start = False
        if start:
            ax.scatter(X[0], Y[0],
                       color='sienna',
                       s=1000,
                       alpha=1,
                       marker='X')

        if object_type == 'vote':
            if double_gradient:
                for i in range(len(X)):
                    x = float(self.points['voters'][i][0])
                    y = float(self.points['voters'][i][1])
                    ax.scatter(X[i], Y[i], color=[0, y, x], s=s, alpha=alpha)
            else:
                for i in range(len(X)):
                    ax.scatter(X[i], Y[i], color=color, alpha=alpha, marker=marker,
                               s=self.quantities[i] * s)
        elif object_type == 'candidate':
            for i in range(len(X)):
                ax.scatter(X[i], Y[i], color=color, alpha=alpha, marker=marker, s=s)

        avg_x = np.mean(X)
        avg_y = np.mean(Y)

        if radius:
            # Compute integer axis bounds explicitly to satisfy static analyzers.
            xmin = int(avg_x - radius)
            xmax = int(avg_x + radius)
            ymin = int(avg_y - radius)
            ymax = int(avg_y + radius)
            ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))

        try:
            ax.set_title(self.texify_label(self.label), size=title_size)
        except Exception:
            pass

        ax.axis('off')

        plt.close(fig)

        self.microscope = Microscope(fig, ax, self.experiment_id, self.label, object_type)
        return self.microscope


def convert_votes_to_potes(votes) -> np.ndarray:
    """Convert votes to positional votes (potes).

    Parameters
    ----------
    votes : sequence
        Iterable of vote rankings (iterables of candidate indices).

    Returns
    -------
    np.ndarray
        Array of potes with shape (len(votes), num_candidates).
    """
    return np.array([[list(vote).index(i) for i, _ in enumerate(vote)]
                     for vote in votes])
