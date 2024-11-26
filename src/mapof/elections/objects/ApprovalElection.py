import os
from abc import ABC
from collections import Counter

import numpy as np
from mapof.core.distances import hamming
from matplotlib import pyplot as plt

import mapof.elections.persistence.election_exports as exports
import mapof.elections.persistence.election_imports as imports
from mapof.elections.cultures import generate_approval_votes
from mapof.elections.cultures.params import update_params_approval
from mapof.elections.objects.Election import Election


class ApprovalElection(Election, ABC):
    """ Approval Election class. """

    def __init__(self,
                 experiment_id=None,
                 election_id=None,
                 culture_id=None,
                 num_candidates=None,
                 variable=None,
                 params=None,
                 **kwargs):

        super().__init__(experiment_id=experiment_id,
                         election_id=election_id,
                         culture_id=culture_id,
                         num_candidates=num_candidates,
                         instance_type='approval',
                         params=params,
                         **kwargs)

        self.variable = variable

        self.approvalwise_vector = []
        self.reverse_approvals = []
        self.candidatelikeness_original_vectors = []

        if self.is_imported and self.experiment_id is not None:
            self.import_approval_election()

        self.try_updating_params()

    def import_approval_election(self) -> None:
        """
        Imports approval elections from a file.

        Returns
        -------
            None
        """

        try:
            (
                self.votes,
                self.num_voters,
                self.num_candidates,
                self.params,
                self.culture_id,
                self.num_options,
                self.quantities,
                self.distinct_votes,
            ) = imports.import_real_app_election(
                experiment_id=self.experiment_id,
                election_id=self.election_id,
                is_shifted=self.is_shifted
            )
        except Exception:
            pass

    def try_updating_params(self):
        if self.culture_id is not None:
            self.params = update_params_approval(
                self.params,
                self.variable,
                self.culture_id,
            )

    def votes_to_approvalwise_vector(self) -> None:
        """
        Converts votes to approvalwise vectors.

        Returns
        -------
            None
        """
        approvalwise_vector = np.zeros([self.num_candidates])
        for vote in self.votes:
            for c in vote:
                approvalwise_vector[c] += 1
        approvalwise_vector = approvalwise_vector / self.num_voters
        self.approvalwise_vector = np.sort(approvalwise_vector)

    def compute_reverse_approvals(self) -> None:
        """
        Computes the reverse approvals.

        Returns
        -------
            None
        """
        self.reverse_approvals = [set(i for i, vote in enumerate(self.votes) if c in vote)
                                  for c in range(self.num_candidates)]

    def get_reverse_approvals(self) -> list[set]:
        """
        Returns the reverse approvals.
        Additionally, if they are not computed, it computes them.

        Returns
        -------
            list[set]
                The reverse approvals.
        """
        if self.reverse_approvals is None or self.reverse_approvals == []:
            self.compute_reverse_approvals()
        return self.reverse_approvals

    def prepare_instance(self, is_exported=False, is_aggregated=True) -> None:
        """
        Prepares all the instances within the experiment.

        Parameters
        ----------
            is_exported : bool
            is_aggregated : bool

        Returns
        -------
            None
        """
        self.votes = generate_approval_votes(culture_id=self.culture_id,
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

    def _compute_distances_between_votes(self, distance_id: str = 'hamming') -> np.ndarray:
        """
        Computes distances between the votes.

        Parameters
        ----------
            distance_id : str
                Name of the distance.

        Returns
        -------
            np.ndarray
                Distances.
        """
        distances = np.zeros([self.num_voters, self.num_voters])
        for v1 in range(self.num_voters):
            for v2 in range(self.num_voters):
                if distance_id == 'hamming':
                    distances[v1][v2] = hamming(self.votes[v1], self.votes[v2])
                elif distance_id == 'jaccard':
                    if len(self.votes[v1].union(self.votes[v2])) == 0:
                        distances[v1][v2] = 1
                    else:
                        distances[v1][v2] = 1 - len(
                            self.votes[v1].intersection(self.votes[v2])) / len(
                            self.votes[v1].union(self.votes[v2]))

        self.distances['vote'] = distances

        if self.is_exported:
            exports.export_distances(self, object_type='vote')

        return distances

    def _compute_distances_between_candidates(self, distance_id='hamming') -> np.ndarray:
        """
        Computes distances between the candidates.

        Parameters
        ----------
            distance_id : str
                Name of the distance.

        Returns
        -------
            np.ndarray
                Distances.
        """
        self.compute_reverse_approvals()
        distances = np.zeros([self.num_candidates, self.num_candidates])
        for c1 in range(self.num_candidates):
            for c2 in range(self.num_candidates):
                if distance_id == 'hamming':
                    distances[c1][c2] = hamming(self.reverse_approvals[c1],
                                                self.reverse_approvals[c2])
                elif distance_id == 'jaccard':
                    if len(self.reverse_approvals[c1].union(self.reverse_approvals[c2])) == 0:
                        distances[c1][c2] = 1
                    else:
                        distances[c1][c2] = 1 - len(
                            self.reverse_approvals[c1].intersection(self.reverse_approvals[c2])) \
                                            / len(
                            self.reverse_approvals[c1].union(self.reverse_approvals[c2]))

        self.distances['candidate'] = distances

        if self.is_exported:
            exports.export_distances(self, object_type='candidate')

        return distances

    def get_candidatelikeness_original_vectors(self, is_recomputed=False):
        if self.candidatelikeness_original_vectors is not None \
                and len(self.candidatelikeness_original_vectors) > 0 \
                and not is_recomputed:
            return self.candidatelikeness_original_vectors
        return self._voted_to_candidatelikeness_original_vectors()

    def _voted_to_candidatelikeness_original_vectors(self):
        """
        Converts votes to candidate-likeness vectors
        """
        matrix = np.zeros([self.num_candidates, self.num_candidates])

        for c_1 in range(self.num_candidates):
            for c_2 in range(self.num_candidates):
                for vote in self.votes:
                    if (c_1 in vote and c_2 not in vote) or (c_1 not in vote and c_2 in vote):
                        matrix[c_1][c_2] += 1
        candidatelikeness_original_vectors = matrix / self.num_voters
        self.candidatelikeness_original_vectors = candidatelikeness_original_vectors
        return candidatelikeness_original_vectors

    def compute_distances(self, object_type=None, distance_id: str = 'hamming') -> np.ndarray:
        """ Computes distances between the votes or candidates. """
        if object_type is None:
            object_type = self.object_type

        if object_type == 'vote':
            return self._compute_distances_between_votes(distance_id=distance_id)
        elif object_type == 'candidate':
            return self._compute_distances_between_candidates(distance_id=distance_id)

    def print_map(
            self,
            show: bool = True,
            radius: float = None,
            name: str = None,
            alpha: float = 0.1,
            s=30,
            object_type=None,
            double_gradient=False,
            saveas=None,
            color='blue',
            marker='o',
            annotate: bool = False
    ):
        """ Print a map of the election (i.e., microscope). """

        if object_type is None:
            object_type = self.object_type

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

        if double_gradient:
            for i in range(len(X)):
                x = float(self.points['voters'][i][0])
                y = float(self.points['voters'][i][1])
                plt.scatter(X[i], Y[i], color=[0, y, x], s=s, alpha=alpha)
        else:
            plt.scatter(X, Y, color=color, s=s, alpha=alpha, marker=marker)

        if annotate:
            for i in range(len(X)):
                plt.annotate(i, (X[i], Y[i]), color='black')

        avg_x = np.mean(X)
        avg_y = np.mean(Y)

        if radius:
            plt.xlim([avg_x - radius, avg_x + radius])
            plt.ylim([avg_y - radius, avg_y + radius])

        plt.axis('off')

        if saveas is not None:

            if saveas == 'default':
                saveas = f'{self.label}_{object_type}'

            file_name = os.path.join(os.getcwd(), "images", name, f'{saveas}.png')
            plt.savefig(file_name, bbox_inches='tight', dpi=100)

        if show:
            plt.show()
        else:
            plt.clf()

        plt.close()
