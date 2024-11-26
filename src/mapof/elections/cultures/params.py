import mapof.core.features.mallows as mallows
import numpy as np
from scipy.stats import gamma

# from mapof.elections.cultures.register import registered_approval_cultures


def update_params_ordinal_mallows(params: dict):
    """ Updates parameters for ordinal Mallows model. """
    if 'phi' in params and type(params['phi']) is list:
        params['phi'] = np.random.uniform(low=params['phi'][0], high=params['phi'][1])
    elif 'phi' not in params:
        params['phi'] = np.random.random()


def update_params_ordinal_norm_mallows(params: dict, num_candidates: int):
    """ Updates parameters for ordinal Norm-Mallows model. """
    if 'normphi' not in params:
        params['normphi'] = np.random.random()
    params['phi'] = mallows.phi_from_normphi(num_candidates, normphi=params['normphi'])
    if 'weight' not in params:
        params['weight'] = 0.


def update_params_ordinal_urn_model(params: dict):
    """ Updates parameters for ordinal Urn model. """
    if 'alpha' not in params:
        params['alpha'] = gamma.rvs(0.8)


def update_params_ordinal_mallows_matrix_path(params: dict, num_candidates: int):
    params['normphi'] = params['alpha']
    params['phi'] = mallows.phi_from_normphi(num_candidates, normphi=params['normphi'])


def update_params_ordinal_mallows_triangle(params: dict, num_candidates: int):
    params['normphi'] = 1 - np.sqrt(np.random.uniform())
    params['phi'] = mallows.phi_from_normphi(num_candidates, normphi=params['normphi'])
    params['weight'] = np.random.uniform(0, 0.5)
    params['alpha'] = params['normphi']
    params['tint'] = params['weight']  # for tint on plots


def update_params_ordinal_alpha(printing_params: dict):
    if 'alpha' not in printing_params:
        printing_params['alpha'] = None
    elif type(printing_params['alpha']) is list:
        printing_params['alpha'] = np.random.uniform(low=printing_params['alpha'][0],
                                                     high=printing_params['alpha'][1])


def update_params_ordinal(
        params: dict,
        culture_id: str,
        num_candidates: int
):
    if culture_id.lower() == 'mallows':
        update_params_ordinal_mallows(params)
    elif 'norm_mallows' in culture_id.lower() or 'norm-mallows' in culture_id.lower() \
            or 'mallows_urn' in culture_id.lower():
        update_params_ordinal_norm_mallows(params, num_candidates)
    elif 'urn' in culture_id.lower():
        update_params_ordinal_urn_model(params)
    elif culture_id.lower() == 'mallows_matrix_path':
        update_params_ordinal_mallows_matrix_path(params, num_candidates)
    elif culture_id.lower() == 'mallows_triangle':
        update_params_ordinal_mallows_triangle(params, num_candidates)
    return params


def update_params_approval_rel_size_central_vote(params: dict, culture_id: str):
    if 'p' in params and culture_id in \
            ['resampling', 'disjoint_resampling', 'moving_resampling', 'noise']:
        params['rel_size_central_vote'] = params['p']
        params.pop('p')


# def update_params_approval_alpha(printing_params: dict):
#     if 'alpha' not in printing_params:
#         printing_params['alpha'] = 1
#     elif type(printing_params['alpha']) is list:
#         printing_params['alpha'] = np.random.uniform(low=printing_params['alpha'][0],
#                                                      high=printing_params['alpha'][1])


# def update_params_approval_p(params: dict):
#     if 'p' not in params:
#         params['p'] = np.random.rand()
#     elif type(params['p']) is list:
#         params['p'] = np.random.uniform(low=params['p'][0], high=params['p'][1])


def update_params_approval_resampling(params: dict):
    if 'phi' in params and type(params['phi']) is list:
        params['phi'] = np.random.uniform(low=params['phi'][0], high=params['phi'][1])
    elif 'phi' not in params:
        params['phi'] = np.random.random()

    if 'p' in params and type(params['p']) is list:
        params['p'] = np.random.uniform(low=params['p'][0], high=params['p'][1])
    elif 'p' not in params:
        params['p'] = np.random.random()


def update_params_approval_disjoint(params: dict):
    if 'phi' in params and type(params['phi']) is list:
        params['phi'] = np.random.uniform(low=params['phi'][0], high=params['phi'][1])
    elif 'phi' not in params:
        params['phi'] = np.random.random()

    if 'p' in params and type(params['p']) is list:
        params['p'] = np.random.uniform(low=params['p'][0], high=params['p'][1])
    elif 'p' not in params:
        params['p'] = np.random.random() / params['g']


def update_params_approval(
        params: dict,
        variable,
        culture_id: str,
):
    if variable is not None:
        del params['variable']
    else:
        if culture_id.lower() == 'resampling':
            update_params_approval_resampling(params)
        elif culture_id.lower() == 'disjoint':
            update_params_approval_disjoint(params)
        update_params_approval_rel_size_central_vote(params, culture_id.lower())

    return params


def get_params_for_paths(path, size, j, extremes=False):

    variable = path['variable']

    if 'extremes' in path:
        extremes = path['extremes']

    params = {'variable': variable}
    if extremes:
        params[variable] = j / (size - 1)
    elif not extremes:
        params[variable] = (j + 1) / (size + 1)

    if 'scale' in path:
        params[variable] *= path['scale']

    if 'start' in path:
        params[variable] += path['start']
    else:
        path['start'] = 0.

    if 'step' in path:
        params[variable] = path['start'] + j * path['step']

    return params, variable
