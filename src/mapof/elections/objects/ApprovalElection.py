import logging
from abc import ABC
from collections import Counter
from typing import List, Set, Optional

import numpy as np
from mapof.core.distances import hamming
from matplotlib import pyplot as plt

import mapof.elections.persistence.election_exports as exports
import mapof.elections.persistence.election_imports as imports
from mapof.elections.cultures import generate_approval_votes
from mapof.elections.cultures.params import update_params_approval
from mapof.elections.objects.Election import Election
from mapof.elections.objects.Microscope import Microscope


class ApprovalElection(Election, ABC):
    """ Approval Election class. """

    def __init__(self,
                 experiment_id=None,
                 election_id=None,
                 culture_id=None,
                 num_candidates=None,
                 fast_import=False,
                 params=None,
                 **kwargs):

        super().__init__(experiment_id=experiment_id,
                         election_id=election_id,
                         culture_id=culture_id,
                         num_candidates=num_candidates,
                         instance_type='approval',
                         fast_import=fast_import,
                         params=params,
                         **kwargs)

        # cached / derived values (None until computed)
        self.approvalwise_vector: Optional[np.ndarray] = None
        self.reverse_approvals: Optional[List[Set[int]]] = None
        self.candidatelikeness_original_vectors: Optional[np.ndarray] = None

        if self.is_imported and self.experiment_id is not None and not fast_import:
            self.import_approval_election()

        self.try_updating_params()

    def import_approval_election(self) -> None:
        """
        Imports approval elections from a file.
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
            ) = imports.import_approval_election(
                experiment_id=self.experiment_id,
                election_id=self.election_id,
                is_shifted=self.is_shifted
            )
        except Exception:
            logging.warning(f'Could not import instance {self.election_id}.')

    def try_updating_params(self) -> None:
        if self.culture_id is not None:
            self.params = update_params_approval(
                self.params,
                self.culture_id,
            )

    def votes_to_approvalwise_vector(self) -> None:
        """
        Converts votes to an approval-wise frequency vector (fraction of voters approving each candidate).
        The resulting vector is sorted (ascending) to match prior behavior.
        """
        approvalwise_vector = np.zeros(self.num_candidates, dtype=float)
        for vote in self.votes:
            for c in vote:
                approvalwise_vector[int(c)] += 1
        approvalwise_vector = approvalwise_vector / float(self.num_voters)
        self.approvalwise_vector = np.sort(approvalwise_vector)

    def compute_reverse_approvals(self) -> None:
        """
        Computes reverse approvals: for each candidate, the set of voters who approve them.
        """
        self.reverse_approvals = [
            {i for i, vote in enumerate(self.votes) if c in vote}
            for c in range(self.num_candidates)
        ]

    def get_reverse_approvals(self) -> List[Set[int]]:
        """
        Returns the reverse approvals, computing them if necessary.
        """
        # Only compute reverse approvals when the cached value is None.
        # Previously this used `if not self.reverse_approvals:`, which would
        # recompute when the cached data is an empty list (falsy). Using `is None`
        # preserves an intentionally-empty cache.
        if self.reverse_approvals is None:
            self.compute_reverse_approvals()
        return self.reverse_approvals

    def prepare_instance(self, is_exported: bool = False, is_aggregated: bool = True) -> None:
        """
        Prepares all the instances within the experiment.
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
        Computes distances between votes. Uses symmetry to compute only upper triangle and mirrors it.
        """
        n = self.num_voters
        distances = np.zeros((n, n), dtype=float)

        if distance_id == 'hamming':
            for v1 in range(n):
                a = self.votes[v1]
                for v2 in range(v1, n):
                    b = self.votes[v2]
                    d = hamming(a, b)
                    distances[v1, v2] = d
                    distances[v2, v1] = d

            self.distances['vote'] = distances

            if self.is_exported:
                exports.export_distances(self, object_type='vote')

            return distances
        elif distance_id == 'jaccard':
            for v1 in range(n):
                a = self.votes[v1]
                for v2 in range(v1, n):
                    b = self.votes[v2]
                    union_len = len(a.union(b))
                    if union_len == 0:
                        d = 1.0
                    else:
                        d = 1.0 - len(a.intersection(b)) / union_len
                    distances[v1, v2] = d
                    distances[v2, v1] = d

            self.distances['vote'] = distances

            if self.is_exported:
                exports.export_distances(self, object_type='vote')

            return distances
        else:
            raise ValueError(f'Unknown distance_id: {distance_id}')

    def _compute_distances_between_candidates(self, distance_id: str = 'hamming') -> np.ndarray:
        """
        Computes distances between the candidates (based on reverse approvals).
        Uses symmetry to halve computations.
        """
        self.compute_reverse_approvals()
        m = self.num_candidates
        distances = np.zeros((m, m), dtype=float)

        if distance_id == 'hamming':
            for c1 in range(m):
                a = self.reverse_approvals[c1]
                for c2 in range(c1, m):
                    b = self.reverse_approvals[c2]
                    d = hamming(a, b)
                    distances[c1, c2] = d
                    distances[c2, c1] = d

            self.distances['candidate'] = distances

            if self.is_exported:
                exports.export_distances(self, object_type='candidate')

            return distances
        elif distance_id == 'jaccard':
            for c1 in range(m):
                a = self.reverse_approvals[c1]
                for c2 in range(c1, m):
                    b = self.reverse_approvals[c2]
                    union_len = len(a.union(b))
                    if union_len == 0:
                        d = 1.0
                    else:
                        d = 1.0 - len(a.intersection(b)) / union_len
                    distances[c1, c2] = d
                    distances[c2, c1] = d

            self.distances['candidate'] = distances

            if self.is_exported:
                exports.export_distances(self, object_type='candidate')

            return distances
        else:
            raise ValueError(f'Unknown distance_id: {distance_id}')

    def get_candidatelikeness_original_vectors(self, is_recomputed: bool = False) -> np.ndarray:
        if self.candidatelikeness_original_vectors is not None and not is_recomputed:
            return self.candidatelikeness_original_vectors
        return self._voted_to_candidatelikeness_original_vectors()

    def _voted_to_candidatelikeness_original_vectors(self) -> np.ndarray:
        """
        Converts votes to candidate-likeness vectors: for each ordered pair (i,j) counts fraction of voters
        who approve exactly one of the two candidates (i xor j).
        """
        matrix = np.zeros((self.num_candidates, self.num_candidates), dtype=float)

        for c_1 in range(self.num_candidates):
            for c_2 in range(self.num_candidates):
                count = 0
                for vote in self.votes:
                    if (c_1 in vote) != (c_2 in vote):
                        count += 1
                matrix[c_1, c_2] = count

        candidatelikeness_original_vectors = matrix / float(self.num_voters)
        self.candidatelikeness_original_vectors = candidatelikeness_original_vectors
        return candidatelikeness_original_vectors

    def _voted_to_candidatelikeness_original_vectors_vectorized(self) -> np.ndarray:
        """
        Vectorized implementation of candidate-likeness computation.
        Builds a boolean matrix A of shape (num_voters, num_candidates) where A[v, c] == 1 if voter v approves c.
        Then for candidates i,j: count_xor(i,j) = s[i] + s[j] - 2 * intersection[i,j]
        where s is column sums and intersection = A.T @ A.
        Returns the same normalized matrix (divided by num_voters).
        """
        n = int(self.num_voters)
        m = int(self.num_candidates)

        if n == 0 or m == 0:
            res = np.zeros((m, m), dtype=float)
            self.candidatelikeness_original_vectors = res
            return res

        # Build boolean matrix A (n x m)
        A = np.zeros((n, m), dtype=np.uint8)
        for v_idx, vote in enumerate(self.votes):
            for c in vote:
                A[v_idx, int(c)] = 1

        # column sums (number of voters approving each candidate)
        s = A.sum(axis=0).astype(np.int64)
        # intersection counts: number of voters approving both candidates i and j
        inter = A.T @ A  # shape (m, m), dtype=int

        # XOR counts: s_i + s_j - 2*inter_ij
        # use broadcasting
        matrix = s.reshape((m, 1)) + s.reshape((1, m)) - 2 * inter

        res = matrix.astype(float) / float(n)
        self.candidatelikeness_original_vectors = res
        return res

    def compute_distances(self, object_type: Optional[str] = None, distance_id: str = 'hamming') -> np.ndarray:
        """ Computes distances between the votes or candidates. """
        if object_type is None:
            object_type = self.object_type

        if object_type == 'vote':
            return self._compute_distances_between_votes(distance_id=distance_id)
        elif object_type == 'candidate':
            return self._compute_distances_between_candidates(distance_id=distance_id)
        else:
            raise ValueError(f'Unknown object_type: {object_type}')

    def set_microscope(
            self,
            radius: Optional[float] = None,
            alpha: float = 0.1,
            s=30,
            object_type: Optional[str] = None,
            double_gradient: bool = False,
            color: str = 'blue',
            marker: str = 'o',
            title_size = 20,
            annotate: bool = False
    ) -> Microscope:
        """Print a map of the election (i.e., microscope) using matplotlib's OO API."""

        if object_type is None:
            object_type = self.object_type

        fig, ax = plt.subplots(figsize=(6.4, 6.4))

        X = [elem[0] for elem in self.coordinates[object_type]]
        Y = [elem[1] for elem in self.coordinates[object_type]]

        if double_gradient:
            for i in range(len(X)):
                x = float(self.points['voters'][i][0])
                y = float(self.points['voters'][i][1])
                ax.scatter(X[i], Y[i], color=(0.0, y, x), s=s, alpha=alpha)
        else:
            ax.scatter(X, Y, color=color, s=s, alpha=alpha, marker=marker)

        if annotate:
            for i in range(len(X)):
                ax.annotate(str(i), (X[i], Y[i]), color='black')

        avg_x = float(np.mean(X))
        avg_y = float(np.mean(Y))

        if radius is not None:
            ax.set_xlim((avg_x - radius, avg_x + radius))
            ax.set_ylim((avg_y - radius, avg_y + radius))

        try:
            ax.set_title(self.texify_label(self.label), size=title_size)
        except Exception:
            pass

        ax.axis('off')

        plt.close(fig)

        self.microscope = Microscope(fig, ax, self.experiment_id, self.label, object_type)
        return self.microscope
