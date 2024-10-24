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

registered_ordinal_features = {
    'highest_borda_score': scores.highest_borda_score,
    'highest_plurality_score': scores.highest_plurality_score,
    'highest_copeland_score': scores.highest_copeland_score,
    'lowest_dodgson_score': scores.lowest_dodgson_score,
    'highest_cc_score': scores.highest_cc_score,
    'highest_hb_score': scores.highest_hb_score,
    'highest_pav_score': scores.highest_pav_score,
    'greedy_approx_cc_score': approx.get_greedy_approx_cc_score,
    'removal_approx_cc_score': approx.get_removal_approx_cc_score,
    'greedy_approx_hb_score': approx.get_greedy_approx_hb_score,
    'removal_approx_hb_score': approx.get_removal_approx_hb_score,
    'greedy_approx_pav_score': approx.get_greedy_approx_pav_score,
    'removal_approx_pav_score': approx.get_removal_approx_pav_score,
    'banzhaf_cc_score': banzhaf_cc.get_banzhaf_cc_score,
    'ranging_cc_score': ranging_cc.get_ranging_cc_score,
    'num_of_diff_votes': vcd.num_of_diff_votes,
    'borda_diversity': vcd.borda_diversity,
    'borda_std': diversity.borda_std,
    'borda_range': diversity.borda_range,
    'borda_gini': diversity.borda_gini,
    'borda_meandev': diversity.borda_meandev,
    'cand_dom_dist_mean': diversity.cand_dom_dist_mean,
    'cand_dom_dist_std': diversity.cand_dom_dist_std,
    'cand_pos_dist_std': diversity.cand_pos_dist_std,
    'cand_pos_dist_gini': diversity.cand_pos_dist_gini,
    'cand_pos_dist_meandev': diversity.cand_pos_dist_meandev,
    'med_cands_summed': diversity.med_cands_summed,
    'vote_dist_mean': diversity.vote_dist_mean,
    'vote_dist_max': diversity.vote_dist_max,
    'vote_dist_med': diversity.vote_dist_med,
    'vote_dist_gini': diversity.vote_dist_gini,
    'vote_sqr_dist_mean': diversity.vote_sqr_dist_mean,
    'vote_sqr_dist_med': diversity.vote_sqr_dist_med,
    'vote_diversity_Karpov': diversity.vote_diversity_Karpov,
    'greedy_kKemenys_summed': diversity.greedy_kKemenys_summed,
    'greedy_2kKemenys_summed': diversity.greedy_2kKemenys_summed,
    'greedy_kKemenys_divk_summed': diversity.greedy_kKemenys_divk_summed,
    'polarization_1by2Kemenys': diversity.polarization_1by2Kemenys,
    'greedy_kmeans_summed': diversity.greedy_kmeans_summed,
    'support_pairs': diversity.support_pairs,
    'support_triplets': diversity.support_triplets,
    'support_votes': diversity.support_votes,
    'support_diversity_summed': diversity.support_diversity_summed,
    'support_diversity_normed_summed': diversity.support_diversity_normed_summed,
    'support_diversity_normed2_summed': diversity.support_diversity_normed2_summed,
    'support_diversity_normed3_summed': diversity.support_diversity_normed3_summed,
    'dist_to_Borda_mean': diversity.dist_to_Borda_mean,
    'dist_to_Kemeny_mean': diversity.dist_to_Kemeny_mean,
    'borda_spread': scores.borda_spread,
    'Entropy': entropy.entropy,
    'Agreement': diversity.agreement_index,
    'Diversity': diversity.diversity_index,
    'Polarization': diversity.polarization_index,
    'AgreementApprox': dap_approx.agreement_index,
    'DiversityApprox': dap_approx.diversity_index,
    'PolarizationApprox': dap_approx.polarization_index,
    'partylist': partylist.partylistdistance,

    'rand_approx_pav_score': approx.get_rand_approx_pav_score,  # unsupported feature
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
    elif feature_id in registered_ordinal_features:
        return registered_ordinal_features.get(feature_id)
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
    registered_ordinal_features[name] = function


__all__ = [
    'get_global_feature',
    'get_local_feature',
    'add_approval_feature',
    'add_ordinal_feature'
]
