import prefsampling.approval as pref_approval
import prefsampling.ordinal as pref_ordinal
import logging

from prefsampling.core.euclidean import EuclideanSpace

from mapof.elections.cultures.register import register_ordinal_election_culture
from mapof.elections.cultures.register import register_approval_election_culture


@register_approval_election_culture('truncated_urn')
def truncated_urn_mask(num_voters=None,
                       num_candidates=None,
                       p=None,
                       alpha=None,
                       **kwargs):
    """ Mask for the urn culture. """
    return pref_approval.truncated_ordinal(num_voters=num_voters,
                                           num_candidates=num_candidates,
                                           rel_num_approvals=p,
                                           ordinal_sampler=pref_ordinal.urn,
                                           ordinal_sampler_parameters={'alpha': alpha},
                                           **kwargs)


@register_approval_election_culture('identity')
def identity_approval_mask(num_voters=None,
                           num_candidates=None,
                           p=0.5,
                           **kwargs):
    """ Mask for the ID culture. """
    return pref_approval.identity(num_voters=num_voters,
                                  num_candidates=num_candidates,
                                  rel_num_approvals=p,
                                  **kwargs)


@register_approval_election_culture('impartial')
def impartial_approval_mask(num_voters=None,
                            num_candidates=None,
                            p=0.5,
                            **kwargs):
    """ Mask for the ID culture. """
    return pref_approval.impartial(num_voters=num_voters,
                                   num_candidates=num_candidates,
                                   p=p,
                                   **kwargs)


@register_ordinal_election_culture('group_separable')
def group_separable_mask(num_voters=None,
                         num_candidates=None,
                         tree_sampler=None,
                         seed=None,
                         **_kwargs):
    """ Mask for the group-separable culture. """

    if type(tree_sampler) is str:
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


@register_ordinal_election_culture('euclidean')
def euclidean_ordinal_mask(num_voters=None,
                           num_candidates=None,
                           space=None,
                           dim=2,
                           **kwargs):
    """ Euclidean Ordinal Masked"""

    num_dimensions = dim

    if type(space) is str:
        if space.lower() == 'uniform':
            point_sampler = EuclideanSpace.UNIFORM_CUBE
        elif space.lower() == 'sphere':
            point_sampler = EuclideanSpace.UNIFORM_SPHERE
        elif space.lower() == 'ball':
            point_sampler = EuclideanSpace.UNIFORM_BALL
        elif space.lower() == 'gaussian':
            point_sampler = EuclideanSpace.GAUSSIAN_CUBE
        else:
            logging.warning("Invalid space type. Using default uniform cube.")
            point_sampler = EuclideanSpace.UNIFORM_CUBE
    else:
        logging.warning("Invalid space type. Using default uniform cube.")
        point_sampler = EuclideanSpace.UNIFORM_CUBE

    return pref_ordinal.euclidean(
        num_voters=num_voters,
        num_candidates=num_candidates,
        num_dimensions=num_dimensions,
        voters_positions=point_sampler,
        candidates_positions=point_sampler,
        **kwargs)


@register_approval_election_culture('euclidean')
def euclidean_approval_mask(num_voters=None,
                            num_candidates=None,
                            space=None,
                            dim=2,
                            radius=0.2,
                            **kwargs):
    """ Euclidean Approval Masked"""

    num_dimensions = dim

    if type(space) is str:
        if space.lower() == 'uniform':
            point_sampler = EuclideanSpace.UNIFORM_CUBE
        elif space.lower() == 'sphere':
            point_sampler = EuclideanSpace.UNIFORM_SPHERE
        elif space.lower() == 'ball':
            point_sampler = EuclideanSpace.UNIFORM_BALL
        elif space.lower() == 'gaussian':
            point_sampler = EuclideanSpace.GAUSSIAN_CUBE
        else:
            logging.warning("Invalid space type. Using default uniform cube.")
            point_sampler = EuclideanSpace.UNIFORM_CUBE
    else:
        logging.warning("Invalid space type. Using default uniform cube.")
        point_sampler = EuclideanSpace.UNIFORM_CUBE

    return pref_approval.euclidean_vcr(
        num_voters=num_voters,
        num_candidates=num_candidates,
        voters_radius=radius,
        candidates_radius=0,
        num_dimensions=num_dimensions,
        voters_positions=point_sampler,
        candidates_positions=point_sampler,
        **kwargs)


@register_ordinal_election_culture('norm_mallows')
def norm_mallows_mask(num_voters=None,
                      num_candidates=None,
                      normphi=None,
                      phi=None,
                      weight=None,
                      **kwargs):
    """ Mask for the norm mallows culture. """

    return pref_ordinal.norm_mallows(num_voters=num_voters,
                                     num_candidates=num_candidates,
                                     norm_phi=normphi,
                                     **kwargs)
