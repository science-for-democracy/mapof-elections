import numpy as np

from mapof.elections.distances.register import register_ordinal_election_distance


def _feature_distance(election_1, election_2, feature_ids: list[str], ord: int):
    vector_1 = []
    vector_2 = []
    for feature_id in feature_ids:
        try:
            vector_1.append(election_1.get_feature(feature_id, compute_if_missing=False))
            vector_2.append(election_2.get_feature(feature_id, compute_if_missing=False))
        except Exception:
            raise Exception(f"Feature {feature_id} not found in the election objects")
    return np.linalg.norm(vector_1 - vector_2, ord=ord)


@register_ordinal_election_distance("feature_l1")
def features_vector_l1(election_1, election_2, feature_ids: list[str]) -> float:
    """
    Computes ell_1 distance between two feature vectors.

    Parameters
    ----------
        election_1 : OrdinalElection
            First election.
        election_2 : OrdinalElection
            Second election.
        feature_ids : list[str]
            List of feature ids.

    Returns
    -------
        float
            ell_2 distance between two feature vectors.

    """
    return _feature_distance(election_1, election_2, feature_ids, 1)


@register_ordinal_election_distance("feature_l2")
def features_vector_l2(election_1, election_2, feature_ids: list[str]) -> float:
    """
    Computes ell_2 distance between two feature vectors.

    Parameters
    ----------
        election_1 : OrdinalElection
            First election.
        election_2 : OrdinalElection
            Second election.
        feature_ids : list[str]
            List of feature ids.

    Returns
    -------
        float
            ell_2 distance between two feature vectors.

    """
    return _feature_distance(election_1, election_2, feature_ids, 2)



