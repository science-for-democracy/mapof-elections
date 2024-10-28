from mapof.core.glossary import MAIN_GLOBAL_FEATUERS
import mapof.core.features as core_features

import mapof.elections.features.approx as approx
import mapof.elections.features.banzhaf_cc as banzhaf_cc
import mapof.elections.features.cohesive as cohesive
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
import mapof.elections.features.abc_features as approval_rule_features

from mapof.elections.features.register import \
    registered_ordinal_election_features, \
    registered_approval_election_features


def get_global_feature(feature_id):
    """ Global feature depends on all instances """
    if feature_id in MAIN_GLOBAL_FEATUERS:
        return core_features.feature_id


def get_local_feature(feature_id):
    """ Local feature depends only on a single instance """

    if feature_id in registered_approval_election_features:
        return registered_approval_election_features.get(feature_id)
    elif feature_id in registered_ordinal_election_features:
        return registered_ordinal_election_features.get(feature_id)
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
    registered_approval_election_features[name] = function


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
    registered_ordinal_election_features[name] = function


__all__ = [
    'get_global_feature',
    'get_local_feature',
    'add_approval_feature',
    'add_ordinal_feature'
]

