
from mapof.elections.cultures.mallows import get_mallows_matrix
from mapof.elections.cultures.matrices.single_peaked_matrices \
    import get_walsh_matrix, get_conitzer_matrix
from mapof.elections.cultures.params import *


def get_pseudo_multiplication(num_candidates, params, model):
    params['weight'] = 0.
    params['normphi'] = params['alpha']
    main_matrix = []
    if model == 'conitzer_path':
        main_matrix = get_conitzer_vectors(num_candidates).transpose()
    elif model == 'walsh_path':
        main_matrix = get_walsh_vectors(num_candidates).transpose()
    mallows_matrix = get_mallows_vectors(num_candidates, params).transpose()
    output = np.matmul(main_matrix, mallows_matrix).transpose()
    return output


def get_frequency_matrix_for_guardian(pseudo_culture_id, num_candidates, params=None):
    if params is None:
        params = {}

    vectors = np.zeros([num_candidates, num_candidates])

    if pseudo_culture_id == 'pseudo_identity':
        for i in range(num_candidates):
            vectors[i][i] = 1

    elif pseudo_culture_id == 'pseudo_uniformity':
        for i in range(num_candidates):
            for j in range(num_candidates):
                vectors[i][j] = 1. / num_candidates

    elif pseudo_culture_id == 'pseudo_stratification':
        weight = params.get('weight', 0.5)
        half = int(num_candidates*weight)
        for i in range(half):
            for j in range(half):
                vectors[i][j] = 1. / half
        for i in range(half, num_candidates):
            for j in range(half, num_candidates):
                vectors[i][j] = 1. / half

    elif pseudo_culture_id == 'pseudo_antagonism':
        for i in range(num_candidates):
            for _ in range(num_candidates):
                vectors[i][i] = 0.5
                vectors[i][num_candidates - i - 1] = 0.5

    return vectors


def get_pseudo_convex(pseudo_culture_id, num_candidates, num_voters, params, function_name):
    if pseudo_culture_id == 'pseudo_unid':
        base_1 = function_name('pseudo_uniformity', num_candidates)
        base_2 = function_name('pseudo_identity', num_candidates)
    elif pseudo_culture_id == 'pseudo_anid':
        base_1 = function_name('pseudo_antagonism', num_candidates)
        base_2 = function_name('pseudo_identity', num_candidates)
    elif pseudo_culture_id == 'pseudo_stid':
        base_1 = function_name('pseudo_stratification', num_candidates)
        base_2 = function_name('pseudo_identity', num_candidates)
    elif pseudo_culture_id == 'pseudo_anun':
        base_1 = function_name('pseudo_antagonism', num_candidates)
        base_2 = function_name('pseudo_uniformity', num_candidates)
    elif pseudo_culture_id == 'pseudo_stun':
        base_1 = function_name('pseudo_stratification', num_candidates)
        base_2 = function_name('pseudo_uniformity', num_candidates)
    elif pseudo_culture_id == 'pseudo_stan':
        base_1 = function_name('pseudo_stratification', num_candidates)
        base_2 = function_name('pseudo_antagonism', num_candidates)
    else:
        raise NameError('No such pseudo_culture_id!')

    return convex_combination(base_1, base_2, length=num_candidates, params=params)


def convex_combination(base_1, base_2, length=0, params=None):
    alpha = params.get('alpha', 1)
    if base_1.ndim == 1:
        output = np.zeros([length])
        for i in range(length):
            output[i] = alpha * base_1[i] + (1 - alpha) * base_2[i]
    elif base_1.ndim == 2:
        output = np.zeros([length, length])
        for i in range(length):
            for j in range(length):
                output[i][j] = alpha * base_1[i][j] + (1 - alpha) * base_2[i][j]
    else:
        raise NameError('Unknown base!')
    return output



def get_pseudo_matrix_single(pseudo_culture_id, num_candidates, weight=0.5):
    matrix = np.zeros([num_candidates, num_candidates])

    if pseudo_culture_id == 'pseudo_identity':
        for i in range(num_candidates):
            for j in range(i + 1, num_candidates):
                matrix[i][j] = 1

    elif pseudo_culture_id in {'pseudo_uniformity', 'pseudo_antagonism'}:
        for i in range(num_candidates):
            for j in range(num_candidates):
                if i != j:
                    matrix[i][j] = 0.5

    elif pseudo_culture_id == 'pseudo_stratification':
        for i in range(int(num_candidates*weight)):
            for j in range(int(num_candidates*weight), num_candidates):
                matrix[i][j] = 1
        for i in range(int(num_candidates*weight)):
            for j in range(int(num_candidates*weight)):
                if i != j:
                    matrix[i][j] = weight
        for i in range(int(num_candidates*weight), num_candidates):
            for j in range(int(num_candidates*weight), num_candidates):
                if i != j:
                    matrix[i][j] = 1-weight

    return matrix


def get_pseudo_borda_vector(pseudo_culture_id, num_candidates, num_voters):
    borda_vector = np.zeros([num_candidates])

    m = num_candidates
    n = num_voters

    if pseudo_culture_id == 'pseudo_identity':
        for i in range(m):
            borda_vector[i] = n * (m - 1 - i)

    elif pseudo_culture_id in {'pseudo_uniformity', 'pseudo_antagonism'}:
        for i in range(m):
            borda_vector[i] = n * (m - 1) / 2

    elif pseudo_culture_id == 'pseudo_stratification':
        for i in range(int(m / 2)):
            borda_vector[i] = n * (m - 1) * 3 / 4
        for i in range(int(m / 2), m):
            borda_vector[i] = n * (m - 1) / 4

    return borda_vector
