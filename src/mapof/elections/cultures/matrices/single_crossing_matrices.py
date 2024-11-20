import numpy as np

from mapof.elections.cultures.register import register_pseudo_ordinal_culture


@register_pseudo_ordinal_culture('pseudo_single_crossing')
def get_single_crossing_matrix(num_candidates: int, **kwargs) -> np.ndarray:
    """
    Gets a single crossing matrix for a given number of candidates.
    """
    matrix = np.zeros([num_candidates, num_candidates])

    for i in range(num_candidates):
        for j in range(num_candidates - i):
            matrix[i][j] = i + j

    for i in range(num_candidates):
        for j in range(i):
            matrix[i][j] += 1

    sums = [1]
    for i in range(num_candidates):
        sums.append(sums[i] + i)

    for i in range(num_candidates):
        matrix[i][i] += sums[i]
        matrix[i][num_candidates - i - 1] -= i

    for i in range(num_candidates):
        denominator = sum(matrix[i])
        for j in range(num_candidates):
            matrix[i][j] /= denominator

    return matrix
