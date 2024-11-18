from collections import Counter

import mapof.core.printing as pr

from mapof.elections.distances import get_distance
from mapof.elections.features import scores
from mapof.elections.objects.ApprovalElection import ApprovalElection
from mapof.elections.objects.ApprovalElectionExperiment import ApprovalElectionExperiment
from mapof.elections.objects.OrdinalElection import OrdinalElection
from mapof.elections.objects.OrdinalElectionExperiment import OrdinalElectionExperiment


def prepare_online_ordinal_experiment(**kwargs):
    """ Prepares an online ordinal experiment. """
    return prepare_experiment(
        instance_type='ordinal',
        is_exported=False,
        is_imported=False,
        **kwargs
    )


def prepare_offline_ordinal_experiment(**kwargs):
    """ Prepares an offline ordinal experiment. """
    return prepare_experiment(
        instance_type='ordinal',
        is_exported=True,
        is_imported=True,
        **kwargs
    )


def prepare_online_approval_experiment(**kwargs):
    """ Prepares an online approval experiment. """
    return prepare_experiment(
        instance_type='approval',
        is_exported=False,
        is_imported=False,
        **kwargs
    )


def prepare_offline_approval_experiment(**kwargs):
    """ Prepares an offline approval experiment. """
    return prepare_experiment(
        instance_type='approval',
        is_exported=True,
        is_imported=True,
        **kwargs
    )


def prepare_experiment(
        experiment_id=None,
        instances=None,
        distances=None,
        instance_type=None,
        coordinates=None,
        distance_id=None,
        coordinates_names=None,
        embedding_id=None,
        is_imported: bool = False,
        is_exported: bool = False,
        is_shifted: bool = False,
        fast_import: bool = False,
        with_matrix: bool = False,
        dim: int = 2
):
    if instance_type == 'ordinal':
        return OrdinalElectionExperiment(
            experiment_id=experiment_id,
            is_shifted=is_shifted,
            instances=instances,
            is_exported=is_exported,
            is_imported=is_imported,
            distances=distances,
            coordinates=coordinates,
            distance_id=distance_id,
            coordinates_names=coordinates_names,
            embedding_id=embedding_id,
            fast_import=fast_import,
            with_matrix=with_matrix,
            instance_type=instance_type,
            dim=dim
        )
    elif instance_type in ['approval', 'rule']:
        return ApprovalElectionExperiment(
            experiment_id=experiment_id,
            is_shifted=is_shifted,
            instances=instances,
            is_exported=is_exported,
            is_imported=is_imported,
            distances=distances,
            coordinates=coordinates,
            distance_id=distance_id,
            coordinates_names=coordinates_names,
            embedding_id=embedding_id,
            fast_import=fast_import,
            instance_type=instance_type,
            dim=dim
        )


def custom_div_cmap(**kwargs):
    return pr.custom_div_cmap(**kwargs)


def print_matrix(**kwargs):
    pr.print_matrix(**kwargs)


def generate_ordinal_election(**kwargs):
    """ Generates an ordinal election. """
    election = OrdinalElection(**kwargs, is_exported=False)
    election.prepare_instance()
    return election


def generate_approval_election(**kwargs):
    """ Generates an approval election. """
    election = ApprovalElection(**kwargs, is_exported=False)
    election.prepare_instance()
    return election


def generate_ordinal_election_from_votes(votes=None):
    """ Generates an ordinal election from votes. """
    election = OrdinalElection()
    election.num_candidates = len(votes[0])
    election.num_voters = len(votes)
    election.votes = votes
    election.is_exported = False
    c = Counter(map(tuple, votes))
    counted_votes = [[count, list(row)] for row, count in c.items()]
    counted_votes = sorted(counted_votes, reverse=True)
    election.quantities = [a[0] for a in counted_votes]
    election.distinct_votes = [a[1] for a in counted_votes]
    election.num_options = len(counted_votes)
    election.is_pseudo = False
    return election


def generate_approval_election_from_votes(
        votes=None,
        num_candidates=None
):
    """ Generates an approval election from votes. """
    election = ApprovalElection()
    if num_candidates is None:
        election.num_candidates = len(set().union(*votes))
    else:
        election.num_candidates = num_candidates
    election.num_voters = len(votes)
    election.votes = votes
    election.is_exported = False
    c = Counter(map(tuple, votes))
    counted_votes = [[count, list(row)] for row, count in c.items()]
    counted_votes = sorted(counted_votes, reverse=True)
    election.quantities = [a[0] for a in counted_votes]
    election.distinct_votes = [a[1] for a in counted_votes]
    election.num_options = len(counted_votes)
    return election


def compute_distance(*args, **kwargs):
    return get_distance(*args, **kwargs)


__all__ = [
    'prepare_online_ordinal_experiment',
    'prepare_offline_ordinal_experiment',
    'prepare_online_approval_experiment',
    'prepare_offline_approval_experiment',
    'prepare_experiment',
    'custom_div_cmap',
    'print_matrix',
    'generate_ordinal_election',
    'generate_approval_election',
    'generate_ordinal_election_from_votes',
    'generate_approval_election_from_votes',
    'compute_distance'
]