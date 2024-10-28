#!/usr/bin/env python

from mapof.core.glossary import MAIN_GLOBAL_FEATUERS
import mapof.core.features as core_features

import mapof.elections.features.approx as approx
import mapof.elections.features.banzhaf_cc as banzhaf_cc
import mapof.elections.features.cohesive as cohesive
import mapof.elections.features.distortion as distortion
import mapof.elections.features.diversity as diversity
import mapof.elections.features.entropy as entropy
import mapof.elections.features.dap_approximate as dap_approx
import mapof.elections.features.justified_representation as jr
import mapof.elections.features.simple_ordinal as simple_ordinal
import mapof.elections.features.simple_approval as simple_approval
import mapof.elections.features.partylist as partylist
import mapof.elections.features.proportionality_degree as prop_deg
import mapof.elections.features.ranging_cc as ranging_cc
import mapof.elections.features.scores as scores
import mapof.elections.features.vc_diversity as vcd

from mapof.elections.features.register import registered_simple_ordinal_features

registered_approval_features = {
    'max_approval_score': simple_approval.max_approval_score,
    'number_of_cohesive_groups': cohesive.count_number_of_cohesive_groups,
    'number_of_cohesive_groups_brute': cohesive.count_number_of_cohesive_groups_brute,
    'proportionality_degree_av': prop_deg.proportionality_degree_av,
    'proportionality_degree_pav': prop_deg.proportionality_degree_pav,
    'proportionality_degree_cc': prop_deg.proportionality_degree_cc,

    'cohesiveness': cohesive.count_largest_cohesiveness_level_l_of_cohesive_group,
    'justified_ratio': simple_approval.justified_ratio,
    'abstract': simple_approval.abstract,  # unsupported feature

    'ejr': jr.test_ejr,  # unsupported feature
}


def get_global_feature(feature_id):
    """ Global feature depends on all instances """
    if feature_id in MAIN_GLOBAL_FEATUERS:
        return core_features.feature_id

    return {
            'distortion_from_all': distortion.distortion_from_all, # unsupported feature
            'avg_distortion_from_guardians': distortion.avg_distortion_from_guardians,
            # unsupported feature
            'worst_distortion_from_guardians': distortion.worst_distortion_from_guardians,
            # unsupported feature
            'distortion': distortion,  # unsupported feature
            'monotonicity_triplets': distortion.monotonicity_triplets,  # unsupported feature
            }.get(feature_id)


def get_local_feature(feature_id):
    """ Local feature depends only on a single instance """

    if feature_id in registered_approval_features:
        return registered_approval_features.get(feature_id)
    elif feature_id in registered_simple_ordinal_features:
        return registered_simple_ordinal_features.get(feature_id)
    else:
        raise ValueError(f'Incorrect feature id: {feature_id}')


def add_approval_feature(name: str, function: callable) -> None:
    """
    Adds a new approval feature to the list of available approval features.

    Parameters
    ----------
        name : str
            Name of the feature.
        function : callable
            function that calculates the feature.

    Returns
    -------
        None
    """
    registered_approval_features[name] = function


def add_ordinal_feature(name: str, function: callable) -> None:
    """
    Adds a new approval feature to the list of available approval features.

    Parameters
    ----------
        name : str
            Name of the feature.
        function : callable
            function that calculates the feature.

    Returns
    -------
        None
    """
    registered_simple_ordinal_features[name] = function


__all__ = [
    'get_global_feature',
    'get_local_feature',
    'add_approval_feature',
    'add_ordinal_feature'
]

