import logging

import prefsampling.approval as pref_approval
import prefsampling.ordinal as pref_ordinal

import mapof.elections.cultures.prefsampling_mask as mask
import mapof.elections.cultures.compass_approx as compass_approx
import mapof.elections.cultures.compass_true as compass_true
import mapof.elections.cultures.mallows as mallows
import mapof.elections.cultures.matrices.single_crossing_matrices as sc_matrices
import mapof.elections.cultures.matrices.single_peaked_matrices as sp_matrices
import mapof.elections.cultures.pseudo_cultures as pseudo
import mapof.elections.cultures.nonstandard.unused as unused
from mapof.elections.cultures.nonstandard.alliances import *
from mapof.elections.cultures.preflib import generate_preflib_votes
from mapof.elections.other.glossary import is_pseudo_culture, LIST_OF_PREFLIB_MODELS

registered_approval_cultures = {
    'identity': mask.identity_mask,
    'id': mask.identity_mask,
    'ic': pref_approval.impartial,
    'impartial': pref_approval.impartial,
    'impartial_culture': pref_approval.impartial,

    'resampling': pref_approval.resampling,
    'disjoint_resampling': pref_approval.disjoint_resampling,
    'moving_resampling': pref_approval.moving_resampling,
    'noise': pref_approval.noise,
    'euclidean': mask.euclidean_app_mask,
    'full': pref_approval.full,
    'empty': pref_approval.empty,
    'truncated_urn': mask.truncated_urn_mask,
    'urn_partylist': pref_approval.urn_partylist,

    'truncated_mallows': mallows.generate_approval_truncated_mallows_votes,  # unsupported culture

    'approval_full': pref_approval.full,  # deprecated name
    'approval_empty': pref_approval.empty,  # deprecated name
}

registered_ordinal_cultures = {
    'identity': pref_ordinal.identity,
    'id': pref_ordinal.identity,  # deprecated name
    'ic': pref_ordinal.impartial,  # deprecated name
    'impartial': pref_ordinal.impartial,
    'impartial_culture': pref_ordinal.impartial,

    'iac': pref_ordinal.impartial_anonymous,
    'real_antagonism': compass_true.generate_real_antagonism_votes,
    'antagonism': compass_true.generate_real_antagonism_votes,
    'an': compass_true.generate_real_antagonism_votes,  # deprecated name

    'urn': pref_ordinal.urn,
    'single-crossing': pref_ordinal.single_crossing,
    'conitzer': pref_ordinal.single_peaked_conitzer,
    'walsh': pref_ordinal.single_peaked_walsh,
    'spoc': pref_ordinal.single_peaked_circle,
    'mallows': pref_ordinal.mallows,
    'didi': pref_ordinal.didi,
    'plackett-luce': pref_ordinal.plackett_luce,

    'approx_stratification': compass_approx.generate_approx_stratification_votes,
    'approx_uniformity': compass_approx.generate_approx_uniformity_votes,
    'un_from_matrix': compass_approx.generate_approx_uniformity_votes,  # deprecated name

    'group-separable': mask.gs_mask,
    'euclidean': mask.euclidean_ord_mask,

    'norm-mallows': mallows.generate_mallows_votes,

    'idan_part': compass_approx.generate_idan_part_votes,  # unsupported culture
    'idun_part': compass_approx.generate_idun_part_votes,  # unsupported culture
    'idst_part': compass_approx.generate_idst_part_votes,  # unsupported culture
    'anun_part': compass_approx.generate_anun_part_votes,  # unsupported culture
    'anst_part': compass_approx.generate_anst_part_votes,  # unsupported culture
    'unst_part': compass_approx.generate_unst_part_votes,  # unsupported culture

    'idan_mallows': compass_approx.generate_idan_mallows_votes,  # unsupported culture
    'idst_mallows': compass_approx.generate_idst_mallows_votes,  # unsupported culture
    'anun_mallows': compass_approx.generate_anun_mallows_votes,  # unsupported culture
    'unst_mallows': compass_approx.generate_unst_mallows_votes,  # unsupported culture

    'unst_topsize': compass_approx.generate_unst_topsize_votes,  # unsupported culture
    'idst_blocks': compass_approx.generate_idst_blocks_votes,
    'norm-mallows_mixture': mallows.generate_norm_mallows_mixture_votes,  # unsupported culture

    # 'walsh_mallows': sp_matrices.generate_walsh_mallows_votes,  # unsupported culture
    # 'conitzer_mallows': sp_matrices.generate_conitzer_mallows_votes,  # unsupported culture
    'mallows_triangle': mallows.generate_mallows_votes,  # unsupported culture
    'walsh_party': unused.generate_sp_party,  # unsupported culture
    'conitzer_party': unused.generate_sp_party,  # unsupported culture
    'mallows_party': mallows.generate_mallows_party,  # unsupported culture
    'ic_party': unused.generate_ic_party,  # unsupported culture
    'un_from_list': compass_approx.generate_un_from_list,  # unsupported culture
    'urn_model': pref_ordinal.urn,  # deprecated name
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
        **kwargs
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

    if culture_id in LIST_OF_PREFLIB_MODELS:
        try:
            votes = generate_preflib_votes(culture_id=culture_id,
                                           num_candidates=num_candidates,
                                           num_voters=num_voters,
                                           params=params)
        except:
            votes = []
            logging.warning(
                f'You are trying to create an election based on Preflib '
                f'without having the original source election. '
                f'Please use different pseudo_culture_id than: {culture_id}')

    elif culture_id in registered_ordinal_cultures:
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
