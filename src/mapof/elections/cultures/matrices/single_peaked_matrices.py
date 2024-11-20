import numpy as np
from scipy.special import binom

from mapof.elections.cultures.register import register_pseudo_ordinal_culture


# WALSH

def f(i, j):
    if i < 0: return 0
    return (1.0 / (2 ** (i + j))) * binom(i + j, i)


def probW(m, i, t):
    # probability that c_i is ranked process_id among m candidates
    return 0.5 * f(i - 1, m - t - (i - 1)) + 0.5 * f(i - t, m - i)

# CONITZER

def g(m, i, j):
    if i > j: return 0
    if i == j: return 1.0 / m
    if i == 1 and j < m: return g(m, 1, j - 1) + 0.5 * g(m, 2, j)
    if j == m and i > 1: return g(m, i + 1, m) + 0.5 * g(m, i, m - 1)
    if i == 1 and j == m: return 1.0
    return 1.0 / m



def probC(m, i, t):
    # probability that c_i is ranked process_id among m candidates
    p = 0.0
    if t == 1: return 1.0 / m

    if i - (t - 1) > 1:
        p += 0.5 * g(m, i - (t - 1), i - 1)
    elif i - (t - 1) == 1:
        p += g(m, i - (t - 1), i - 1)

    if i + (t - 1) < m:
        p += 0.5 * g(m, i + 1, i + (t - 1))
    elif i + (t - 1) == m:
        p += g(m, i + 1, i + (t - 1))

    return p


PRECISION = 1000
DIGITS = 4


@register_pseudo_ordinal_culture('pseudo_single_peaked_conitzer')
def get_conitzer_matrix(num_candidates=None, **_kwargs):
    """
    Gets a Conitzer matrix for a given number of candidates.
    """
    m = num_candidates
    P = np.zeros([m, m])
    for i in range(m):
        for j in range(m):
            P[i][j] = probC(m, i + 1, j + 1)
    return P


@register_pseudo_ordinal_culture('pseudo_single_peaked_walsh')
def get_walsh_matrix(num_candidates=None, **_kwargs):
    """
    Gets a Walsh matrix for a given number of candidates
    """
    m = num_candidates
    P = np.zeros([m, m])
    for i in range(m):
        for t in range(m):
            P[i][t] = probW(m, i + 1, t + 1)
    return P

#
# def generate_conitzer_mallows_votes(num_voters, num_candidates, params):
#     params['phi'] = phi_from_normphi(num_candidates, normphi=params['normphi'])
#
#     votes = generate_ordinal_sp_conitzer_votes(num_voters=num_voters, num_candidates=num_candidates)
#
#     votes = mallows_votes(votes, params['phi'])
#
#     return votes
#
#
# def generate_walsh_mallows_votes(num_voters, num_candidates, params):
#     params['phi'] = phi_from_normphi(num_candidates, normphi=params['normphi'])
#
#     votes = generate_ordinal_sp_walsh_votes(num_voters=num_voters, num_candidates=num_candidates)
#
#     votes = mallows_votes(votes, params['phi'])
#
#     return votes
