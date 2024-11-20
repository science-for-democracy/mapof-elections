import os
import pickle

import mapof.core.features.mallows as ml
import numpy as np

from mapof.elections.cultures.register import register_pseudo_ordinal_culture


def generate_mallows_votes(*args, **kwargs):
    return ml.generate_mallows_votes(*args, **kwargs)


def _calculateZpoly(m):
    res = [1]
    for i in range(1, m + 1):
        mult = [1] * i
        res2 = [0] * (len(res) + len(mult) - 1)
        for o1, i1 in enumerate(res):
            for o2, i2 in enumerate(mult):
                res2[o1 + o2] += i1 * i2
        res = res2
    return res


def _evaluatePolynomial(coeff, x):
    res = 0
    for i, c in enumerate(coeff):
        res += c * (x ** i)
    return res


def _calculateZ(m, phi):
    coeff = _calculateZpoly(m)
    return _evaluatePolynomial(coeff, phi)


# mat[i][j] is the probability with which candidate i ends up in position j
def mallows_matrix(num_candidates, lphi, pos, normalize=True):
    mat = np.zeros([num_candidates, num_candidates])
    if normalize:
        phi = ml.phi_from_normphi(num_candidates, lphi)
    else:
        phi = lphi
    Z = _calculateZ(num_candidates, phi)
    for i in range(num_candidates):
        for j in range(num_candidates):
            freqs = [pos[k][i][j] for k in
                     range(1 + int(num_candidates * (num_candidates - 1) / 2))]
            unnormal_prob = _evaluatePolynomial(freqs, phi)
            mat[i][j] = unnormal_prob / Z
    return mat


def get_mallows_matrix_help(num_candidates, params, normalize=True):
    lphi = params['normphi']
    if 'weight' not in params:
        weight = 0
    else:
        weight = params['weight']

    if 'sec_normphi' not in params:
        lphi_2 = lphi
    else:
        lphi_2 = params['sec_normphi']

    try:
        current_file_path = os.path.abspath(__file__)
        current_file_dir = os.path.dirname(current_file_path)
        path = os.path.join(current_file_dir, 'mallows_positionmatrices',
                            str(num_candidates) + "_matrix.txt")
        with open(path, "rb") as file:
            pos = pickle.load(file)
    except FileNotFoundError:
        print("Mallows frequency_matrix only supported for up to 30 candidates")
    mat1 = mallows_matrix(num_candidates, lphi, pos, normalize)
    mat2 = mallows_matrix(num_candidates, lphi_2, pos, normalize)
    res = np.zeros([num_candidates, num_candidates])
    for i in range(num_candidates):
        for j in range(num_candidates):
            res[i][j] = (1. - weight) * mat1[i][j] + (weight) * mat2[i][num_candidates - 1 - j]
    return res


@register_pseudo_ordinal_culture("pseudo_norm_mallows")
def get_mallows_matrix(
        num_candidates: int,
        params: dict
):
    return get_mallows_matrix_help(num_candidates, params).transpose()
