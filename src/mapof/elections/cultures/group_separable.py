import prefsampling.ordinal as pref_ordinal
import logging


def gs_mask(num_voters=None,
            num_candidates=None,
            tree_sampler=None,
            seed=None,
            **_kwargs):

    if type(tree_sampler) is str:
        logging.warning("group separable BALANCED & CATERPILLAR trees are temporarily unavailable")
        if tree_sampler.lower() == 'balanced':
            tree_sampler = pref_ordinal.TreeSampler.BALANCED
        elif tree_sampler.lower() == 'caterpillar':
            tree_sampler = pref_ordinal.TreeSampler.CATERPILLAR

    if tree_sampler is None:
        tree_sampler = pref_ordinal.TreeSampler.SCHROEDER

    return pref_ordinal.group_separable(num_voters=num_voters,
                                        num_candidates=num_candidates,
                                        tree_sampler=tree_sampler,
                                        seed=seed)
