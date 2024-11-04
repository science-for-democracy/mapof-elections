import logging
import numpy as np

import prefsampling.approval as pref_approval
import prefsampling.ordinal as pref_ordinal

import mapof.elections.cultures.prefsampling_mask as mask
import mapof.elections.cultures.compass as compass
import mapof.elections.cultures.mallows as mallows
import mapof.elections.cultures.matrices.single_crossing_matrices as sc_matrices
import mapof.elections.cultures.matrices.single_peaked_matrices as sp_matrices
import mapof.elections.cultures.pseudo_cultures as pseudo
from mapof.elections.cultures.alliances import (
    generate_ordinal_alliance_ic_votes,
    generate_ordinal_alliance_urn_votes,
    generate_ordinal_alliance_euclidean_votes,
    generate_ordinal_alliance_allied_euclidean_votes,
    generate_ordinal_alliance_norm_mallows_votes,
)
from mapof.elections.other.glossary import is_pseudo_culture

registered_approval_cultures = {
    'identity': mask.identity_approval_mask,
    'id': mask.identity_approval_mask,  # deprecated name
    'ic': mask.impartial_approval_mask,  # deprecated name
    'impartial': mask.impartial_approval_mask,
    'impartial_culture': mask.impartial_approval_mask,  # deprecated name
    'resampling': pref_approval.resampling,
    'disjoint_resampling': pref_approval.disjoint_resampling,
    'moving_resampling': pref_approval.moving_resampling,
    'noise': pref_approval.noise,
    'euclidean': mask.euclidean_approval_mask,
    'full': pref_approval.full,
    'empty': pref_approval.empty,
    'approval_full': pref_approval.full,  # deprecated name
    'approval_empty': pref_approval.empty,  # deprecated name
    'truncated_urn': mask.truncated_urn_mask,
    'urn_partylist': pref_approval.urn_partylist,

    # 'truncated_mallows': mallows.generate_approval_truncated_mallows_votes,  # unsupported culture
}

registered_ordinal_cultures = {
    'identity': pref_ordinal.identity,
    'id': pref_ordinal.identity,  # deprecated name
    'ic': pref_ordinal.impartial,  # deprecated name
    'impartial': pref_ordinal.impartial,
    'impartial_culture': pref_ordinal.impartial,
    'iac': pref_ordinal.impartial_anonymous,
    'antagonism': compass.generate_antagonism_votes,
    'an': compass.generate_antagonism_votes,  # deprecated name
    'didi': pref_ordinal.didi,
    'plackett-luce': pref_ordinal.plackett_luce,
    'urn': pref_ordinal.urn,
    'single-crossing': pref_ordinal.single_crossing,
    'single-peaked_conitzer': pref_ordinal.single_peaked_conitzer,
    'single-peaked_walsh': pref_ordinal.single_peaked_walsh,
    'spoc': pref_ordinal.single_peaked_circle,

    'un_from_matrix': compass.generate_approx_uniformity_votes,  # deprecated name
    'approx_uniformity': compass.generate_approx_uniformity_votes,
    'approx_stratification': compass.generate_approx_stratification_votes,

    'euclidean': mask.euclidean_ordinal_mask,
    'group-separable': mask.group_separable_mask,
    'mallows': pref_ordinal.mallows,
    'norm-mallows': mask.norm_mallows_mask,


    'idan_part': compass.generate_idan_part_votes,
    'idun_part': compass.generate_idun_part_votes,
    'idst_part': compass.generate_idst_part_votes,
    'anun_part': compass.generate_anun_part_votes,
    'anst_part': compass.generate_anst_part_votes,
    'unst_part': compass.generate_unst_part_votes,

    'idst_blocks': compass.generate_idst_blocks_votes,  # unsupported culture
    'unst_topsize': compass.generate_unst_topsize_votes,  # unsupported culture
    'un_from_list': compass.generate_un_from_list,  # unsupported culture
    'norm-mallows_mixture': mallows.generate_norm_mallows_mixture_votes,  # unsupported culture
}


registered_pseudo_ordinal_cultures = {
    'pseudo_uniformity': pseudo.pseudo_uniformity,
    'pseudo_stratification': pseudo.pseudo_stratification,
    'pseudo_identity': pseudo.pseudo_identity,
    'pseudo_antagonism': pseudo.pseudo_antagonism,
    'pseudo_unid': pseudo.pseudo_unid,
    'pseudo_anid': pseudo.pseudo_anid,
    'pseudo_stid': pseudo.pseudo_stid,
    'pseudo_anun': pseudo.pseudo_anun,
    'pseudo_stun': pseudo.pseudo_stun,
    'pseudo_stan': pseudo.pseudo_stan,
    'pseudo_sp_conitzer': sp_matrices.get_conitzer_matrix,
    'pseudo_sp_walsh': sp_matrices.get_walsh_matrix,
    'pseudo_single-crossing': sc_matrices.get_single_crossing_matrix,
}


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
    if culture_id in registered_approval_cultures:
        return registered_approval_cultures.get(culture_id)(num_voters, num_candidates, **params)

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

    if culture_id in registered_ordinal_cultures:
        votes = registered_ordinal_cultures.get(culture_id)(num_voters=num_voters,
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


LIST_OF_ORDINAL_ALLIANCE_MODELS = {
    'ic': generate_ordinal_alliance_ic_votes,
    'urn': generate_ordinal_alliance_urn_votes,
    'euc': generate_ordinal_alliance_euclidean_votes,
    'allied_euc': generate_ordinal_alliance_allied_euclidean_votes,
    'norm-mallows': generate_ordinal_alliance_norm_mallows_votes,
}


def generate_ordinal_alliance_votes(culture_id: str = None,
                                    num_candidates: int = None,
                                    num_voters: int = None,
                                    params: dict = None):
    if culture_id in LIST_OF_ORDINAL_ALLIANCE_MODELS:
        votes, alliances = LIST_OF_ORDINAL_ALLIANCE_MODELS.get(culture_id)(
            num_voters=num_voters,
            num_candidates=num_candidates,
            params=params)
    else:
        votes = []
        alliances = []
        logging.warning(f'No such culture id: {culture_id}')

    return np.array(votes), alliances


def add_approval_culture(name, function):
    """
    Adds a new approval culture to the list of available approval cultures.

    Parameters
    ----------
        name:
            Name of the culture, which will be used as culture id.
        function : str
            Function that generates the votes.
    """
    registered_approval_cultures[name] = function


def add_ordinal_culture(name, function):
    """
    Adds a new ordinal culture to the list of available ordinal cultures.

    Parameters
    ----------
        name:
            Name of the culture, which will be used as culture id.
        function : str
            Function that generates the votes.
    """
    registered_ordinal_cultures[name] = function


def add_pseudo_ordinal_culture(name, function):
    """
    Adds a new ordinal culture to the list of available ordinal cultures.

    Parameters
    ----------
        name:
            Name of the culture, which will be used as culture id.
        function : str
            Function that generates the frequency matrix.
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
    'from_approval'
]
