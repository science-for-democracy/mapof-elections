import logging

import prefsampling.ordinal as pref_ordinal
import prefsampling.approval as pref_approval

from prefsampling.point import cube, sphere_uniform, gaussian, ball_uniform

from prefsampling.core.euclidean import EuclideanSpace


def euclidean_ord_mask(num_voters=None,
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

    if space is None:
        point_sampler = EuclideanSpace.UNIFORM_CUBE

    return pref_ordinal.euclidean(
        num_voters=num_voters,
        num_candidates=num_candidates,
        num_dimensions=num_dimensions,
        voters_positions=point_sampler,
        candidates_positions=point_sampler,
        **kwargs)


def euclidean_app_mask(num_voters=None,
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

    if space is None:
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
