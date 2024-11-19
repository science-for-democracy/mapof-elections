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

# def register_ordinal_election_distance(feature_id: str):
#
#     def decorator(func):
#         registered_ordinal_election_distances[feature_id] = func
#         return func
#
#     return decorator
#
#
# def register_approval_election_distance(feature_id: str):
#
#     def decorator(func):
#         registered_approval_election_distances[feature_id] = func
#         return func
#
#     return decorator
