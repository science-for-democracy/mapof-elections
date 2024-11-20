import numpy as np

from prefsampling.ordinal import impartial as generate_ordinal_ic_votes
from prefsampling.ordinal import urn as generate_urn_votes
from mapof.core.features.mallows import phi_from_normphi
from mapof.elections.cultures.mallows import generate_mallows_votes

from mapof.elections.cultures.register import register_alliance_ordinal_culture


def get_alliances(num_candidates, num_alliances):
    while True:
        alliances = np.random.choice([i for i in range(num_alliances)],
                                     size=num_candidates, replace=True)
        if len(set(alliances)) > 1:
            return alliances


@register_alliance_ordinal_culture('impartial')
def generate_ordinal_alliance_ic_votes(num_voters: int = None,
                                       num_candidates: int = None,
                                       params: dict = None):
    """ Return: ordinal votes from Impartial Culture with alliances """
    votes = generate_ordinal_ic_votes(num_voters, num_candidates)

    alliances = get_alliances(num_candidates, params['num_alliances'])

    return np.array(votes), alliances


@register_alliance_ordinal_culture('urn')
def generate_ordinal_alliance_urn_votes(num_voters: int = None,
                                        num_candidates: int = None,
                                        params: dict = None):
    votes = generate_urn_votes(num_voters, num_candidates, params['alpha'])

    alliances = get_alliances(num_candidates, params['num_alliances'])

    return np.array(votes), alliances


@register_alliance_ordinal_culture('norm_mallows')
def generate_ordinal_alliance_norm_mallows_votes(num_voters: int = None,
                                                 num_candidates: int = None,
                                                 params: dict = None):
    params['phi'] = phi_from_normphi(num_candidates, params['normphi'])
    votes = generate_mallows_votes(num_voters, num_candidates, **params)

    alliances = get_alliances(num_candidates, params['num_alliances'])

    return np.array(votes), alliances


def _assign_to_closest_center(candidates, centers):
    """
    Assign each candidate to the closest center.

    Parameters:
    - candidates: (num_candidates, dim) array, coordinates for each candidate point.
    - centers: (num_alliances, dim) array, coordinates for each center point.

    Returns:
    - assignment: (num_candidates,) array, index of the closest center for each candidate.
    """
    distances = np.linalg.norm(candidates[:, None] - centers, axis=2)
    assignment = np.argmin(distances, axis=1)
    return assignment


@register_alliance_ordinal_culture('euclidean')
def generate_ordinal_alliance_euclidean_votes(
        num_voters: int = None,
        num_candidates: int = None,
        params: dict = None
):
    dim = params.get('dim', 2)
    num_alliances = params.get('num_alliances', 2)

    votes = np.zeros([num_voters, num_candidates], dtype=int)
    distances = np.zeros([num_voters, num_candidates], dtype=float)

    while True:
        voters = np.random.rand(num_voters, dim)
        centers = np.random.rand(num_alliances, dim)
        candidates = np.random.rand(num_candidates, dim)

        alliances = _assign_to_closest_center(candidates, centers)
        if len(set(alliances)) == num_alliances:
            break

    for v in range(num_voters):
        for c in range(num_candidates):
            votes[v][c] = c
            distances[v][c] = np.linalg.norm(voters[v] - candidates[c])

        votes[v] = [x for _, x in sorted(zip(distances[v], votes[v]))]

    return votes, alliances
