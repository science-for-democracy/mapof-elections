"""
Implementation of the positionwise infinity distance.
Code name: 'ep' (as in 'extended positionwise')
"""
import math

import numpy as np

from mapof.core.matchings import solve_matching_vectors
from mapof.elections.objects import Election

from mapof.elections.distances.register import register_ordinal_election_distance


def emd_infty(xx, yy):
    """
    Wasserstein distance calculation
    """
    m = len(xx)
    cum_x = 0
    cum_y = 0
    res = 0
    for x, y in zip(xx, yy):
        cum_x_ = cum_x
        cum_y_ = cum_y
        cum_x += x
        cum_y += y

        if np.sign(cum_x_ - cum_y_) == np.sign(cum_x - cum_y):
            # Trapezoid case
            res += (abs(cum_x_ - cum_y_) + abs(cum_x - cum_y)) / m / 2
        else:
            # Two triangles case (works also for one triangle)
            d_1 = abs(cum_x_ - cum_y_)
            d_2 = abs(cum_x - cum_y)
            res += (d_1 * d_1 + d_2 * d_2) / (d_1 + d_2) / m / 2

    return res


"""
Stretch the frequency frequency_matrix by the required factor.
"""


def stretch_matrix(matrix, matrix_size, factor):
    stretched = np.zeros([matrix_size * factor, matrix_size * factor])
    column_to_fill = 0
    for col_idx in range(0, matrix_size):
        row_to_fill = 0
        for row_idx in range(0, matrix_size):
            for i in range(0, factor):
                stretched[row_to_fill][column_to_fill] = matrix[row_idx][col_idx] / factor
                row_to_fill += 1
        column_to_fill += 1
        # copy filled col
        for i in range(0, factor - 1):
            for j in range(0, matrix_size * factor):
                stretched[j][column_to_fill] = stretched[j][column_to_fill - 1]
            column_to_fill += 1
    return stretched





def memoization(e1_stretched, e1_original_columns, e2_stretched, e2_original_columns):
    """
    Create memoization table of all the distances that need to be computed and compute them.
    """
    pairs = set()
    mem_table = dict()
    for el1 in e1_original_columns:
        for el2 in e2_original_columns:
            pairs.add((el1, el2))
    for pair in pairs:
        mem_table[pair] = emd_infty(e1_stretched[:, pair[0]], e2_stretched[:, pair[1]])
    return mem_table


def find_copies(matrix_size, factor):
    """
    Calculate indexes of copies.
    """
    table = dict()
    for i in range(0, matrix_size):
        table[i * factor] = [i for i in range(i * factor + 1, (i + 1) * factor)]
    return table


def copy_to_original_mapping(original_to_copies: dict):
    """
    Map copy votes to their original votes.
    """
    copy_to_original = dict()
    for key, val in original_to_copies.items():
        for v in val:
            copy_to_original[v] = key
        copy_to_original[key] = key
    return copy_to_original


def memoization_to_cost_table(mem_table, num_cols, e1_copies_to_original, e2_copies_to_original):
    """
    Convert the memoization table to cost table.
    """
    cost_table = list()
    for i in range(0, num_cols):
        cost_table.append([])
    for e1_column_idx in range(0, num_cols):  # cols in e1
        for e2_column_idx in range(0, num_cols):  # cols in e2
            key = (e1_copies_to_original[e1_column_idx], e2_copies_to_original[e2_column_idx])
            value = mem_table[key]
            cost_table[e1_column_idx].append(value)
    return cost_table


def lcm(a, b):
    """
    Lcm implementation to make the code runnable with older versions of Python
    which do not have it in their math library.
    """
    return abs(a * b) // math.gcd(a, b)


@register_ordinal_election_distance("positionwise_infty")
def positionwise_size_independent(e1: Election, e2: Election):
    """
    Main function of the positionwise infinity distance, pointer to this function is added to the experiment when I wish to compute the positionwise infinity distance for an experiment.
    """
    election_lcm = lcm(e1.num_candidates, e2.num_candidates)
    e1_stretched = stretch_matrix(e1.get_frequency_matrix(), e1.num_candidates, int(election_lcm / e1.num_candidates))
    e2_stretched = stretch_matrix(e2.get_frequency_matrix(), e2.num_candidates, int(election_lcm / e2.num_candidates))
    e1_original_to_copies = find_copies(matrix_size=e1.num_candidates, factor=int(election_lcm / e1.num_candidates))
    e2_original_to_copies = find_copies(matrix_size=e2.num_candidates, factor=int(election_lcm / e2.num_candidates))
    e1_copies_to_original = copy_to_original_mapping(e1_original_to_copies)
    e2_copies_to_original = copy_to_original_mapping(e2_original_to_copies)
    e1_original_columns = e1_original_to_copies.keys()
    e2_original_columns = e2_original_to_copies.keys()

    memoization_table = memoization(e1_stretched, e1_original_columns, e2_stretched, e2_original_columns)
    cost_table = memoization_to_cost_table(memoization_table, election_lcm, e1_copies_to_original,
                                           e2_copies_to_original)
    distance, mapping = solve_matching_vectors(cost_table)
    normalized_distance = distance / (e1.num_candidates * int(election_lcm / e1.num_candidates))
    return normalized_distance, mapping
