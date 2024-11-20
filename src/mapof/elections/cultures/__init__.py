import logging

import numpy as np

import mapof.elections.cultures.alliances
import mapof.elections.cultures.compass
import mapof.elections.cultures.mallows
import mapof.elections.cultures.matrices.group_separable_matrices
import mapof.elections.cultures.matrices.single_crossing_matrices
import mapof.elections.cultures.matrices.single_peaked_matrices
import mapof.elections.cultures.prefsampling_mask
import mapof.elections.cultures.pseudo_cultures
from mapof.elections.cultures.register import (
    registered_approval_election_cultures,
    registered_ordinal_election_cultures,
    registered_pseudo_ordinal_cultures,
    registered_alliance_ordinal_cultures,
)
from mapof.elections.other.glossary import is_pseudo_culture


def generate_approval_votes(
        culture_id: str = None,
        num_voters: int = None,
        num_candidates: int = None,
        params: dict = None
) -> list | np.ndarray:
    """
    Generates approval votes according to the given culture id.

    Parameters
    ----------
        culture_id : str
            Name of the culture.
        num_voters : int
            Number of Voters.
        num_candidates : int
            Number of Candidates
        params : dict
            Culture parameters.
    """
    if culture_id in registered_approval_election_cultures:
        return registered_approval_election_cultures.get(culture_id)(num_voters, num_candidates, **params)

    else:
        logging.warning(f'No such culture id: {culture_id}')
        return []


def generate_ordinal_votes(
        culture_id: str = None,
        num_candidates: int = None,
        num_voters: int = None,
        params: dict = None,
        **_kwargs
) -> list | np.ndarray:
    """
    Generates approval votes according to the given culture id.

    Parameters
    ----------
        culture_id : str
            Name of the culture.
        num_voters : int
            Number of Voters.
        num_candidates : int
            Number of Candidates
        params : dict
            Culture parameters.
    """

    if culture_id in registered_ordinal_election_cultures:
        votes = registered_ordinal_election_cultures.get(culture_id)(num_voters=num_voters,
                                                            num_candidates=num_candidates,
                                                            **params)

    elif is_pseudo_culture(culture_id):
        votes = [culture_id, num_candidates, num_voters, params]
    else:
        votes = []
        logging.warning(
            f'No such culture id: {culture_id} \n'
            f'If you are using your own instances then ignore this warning.')

    if not is_pseudo_culture(culture_id):
        votes = [[int(x) for x in row] for row in votes]

    return np.array(votes)


def approval_votes_to_vectors(votes, num_candidates=None, num_voters=None):
    vectors = np.zeros([num_candidates, num_candidates])
    for vote in votes:
        denom_in = len(vote)
        denom_out = num_candidates - denom_in
        for i in range(num_candidates):
            if i in vote:
                for j in range(denom_in):
                    vectors[i][j] += 1 / denom_in / num_voters
            else:
                for j in range(denom_out):
                    vectors[i][denom_in + j] += 1 / denom_out / num_voters
    return vectors


def from_approval(num_candidates: int = None,
                  num_voters: int = None,
                  params: dict = None):
    votes = generate_approval_votes(culture_id=params['pseudo_culture_id'],
                                    num_candidates=num_candidates, num_voters=num_voters,
                                    params=params)

    return approval_votes_to_vectors(votes, num_candidates=num_candidates, num_voters=num_voters)


def generate_ordinal_alliance_votes(
        culture_id: str = None,
        num_candidates: int = None,
        num_voters: int = None,
        params: dict = None
):
    if culture_id in registered_alliance_ordinal_cultures:
        votes, alliances = registered_alliance_ordinal_cultures.get(culture_id)(
            num_voters=num_voters,
            num_candidates=num_candidates,
            params=params)
    else:
        votes = []
        alliances = []
        logging.warning(f'No such alliance culture id: {culture_id}')

    return np.array(votes), alliances


def add_approval_culture(name, function) -> None:
    """
    Adds a new approval culture to the list of available approval cultures.

    Parameters
    ----------
        name:
            Name of the culture, which will be used as culture id.
        function : str
            Function that generates the votes.

    Returns
    -------
        None
    """
    registered_approval_election_cultures[name] = function


def add_ordinal_culture(name, function) -> None:
    """
    Adds a new ordinal culture to the list of available ordinal cultures.

    Parameters
    ----------
        name : str
            Name of the culture, which will be used as culture id.
        function : callable
            Function that generates the votes.

    Returns
    -------
        None
    """
    registered_ordinal_election_cultures[name] = function


def add_pseudo_ordinal_culture(name, function) -> None:
    """
    Adds a new ordinal culture to the list of available ordinal cultures.

    Parameters
    ----------
        name : str
            Name of the culture, which will be used as culture id.
        function : callable
            Function that generates the frequency matrix.

    Returns
    -------
        None
    """
    registered_pseudo_ordinal_cultures[name] = function


__all__ = [
    'generate_approval_votes',
    'generate_ordinal_votes',
    'generate_ordinal_alliance_votes',
    'add_approval_culture',
    'add_ordinal_culture',
    'add_pseudo_ordinal_culture',
    'approval_votes_to_vectors',
    'from_approval',
]
