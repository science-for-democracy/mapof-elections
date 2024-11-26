import itertools as it
import logging
import math

import numpy as np

import mapof.elections.cultures.sampling.samplemat as smpl
from mapof.elections.cultures.register import register_ordinal_election_culture


def _distribute_in_matrix(n, m):
    if m == 0:
        return []
    k = n // m
    r = n - k * m
    matrix = []
    for i in range(m):
        row = [k for _ in range(m)]
        for j in range(i, i + r):
            if j >= m:
                j = j - m
            row[j] = row[j] + 1
        matrix.append(row)
    return matrix


def _distribute_in_block_matrix(n, blocks):
    before = 0
    after = sum(blocks)
    matrix = []
    for b in blocks:
        after = after - b
        block = _distribute_in_matrix(n, b)
        for row in block:
            matrix.append([0 for _ in range(before)] + row + [0 for _ in range(after)])
        before = before + b
    return (matrix)


def _draw_election(matrix):
    return smpl.sample_election_using_permanent(matrix)


@register_ordinal_election_culture('un_from_list')
def generate_un_from_list(num_voters: int = None, num_candidates: int = None):
    id_perm = list(range(num_candidates))
    m_fac = math.factorial(num_candidates)
    alls = num_voters // m_fac
    rest = num_voters - alls * m_fac
    res = []
    for _ in range(alls):
        res = res + [list(v) for v in it.permutations(id_perm)]
    res = res + [list(v) for v in it.permutations(id_perm)][:rest]
    return res


@register_ordinal_election_culture('approx_uniformity')
def generate_approx_uniformity_votes(num_voters: int = None, num_candidates: int = None) -> list:
    """

    Generates real election that have UN positionwise frequency_matrix.

    Parameters
    ----------
        num_voters : int
            Number of voters.
        num_candidates : int
            Number of candidates.

    Returns
    -------
        list
            Votes
    """
    matrix = _distribute_in_matrix(num_voters, num_candidates)
    return _draw_election(matrix)


@register_ordinal_election_culture('idan_part')
def generate_idan_part_votes(
        num_voters: int = None,
        num_candidates: int = None,
        part_share: float = None,
        **_kwargs
) -> list:
    """
    Generates election between (ID) and (AN).

    Parameters
    ----------
        num_voters : int
            Number of voters.
        num_candidates : int
            Number of candidates.
        part_share : float
            Share of ID voters.

    Returns
    -------
        list
            Votes
    """

    if part_share is None:
        print("IDAN_part generation : params None : random param generated")
        part_size = np.random.choice(range(num_voters))
    else:
        part_size = part_share * (num_voters)
    part_size = int(round(part_size))
    id_share = num_voters - (part_size // 2)
    op_share = part_size // 2
    votes = [[j for j in range(num_candidates)] for _ in range(id_share)]
    votes = votes + [[(num_candidates - j - 1) for j in range(num_candidates)] for _ in
                     range(op_share)]
    return votes


@register_ordinal_election_culture('idun_part')
def generate_idun_part_votes(
        num_voters: int = None,
        num_candidates: int = None,
        part_share: float = None,
        **_kwargs
) -> list:
    """ Generate elections realizing linear combinations of pos-matrices between (ID) and (UN).

    Parameters
    ----------
        num_voters : int
            Number of voters.
        num_candidates : int
            Number of candidates.
        part_share : float
            Share of ID voters.

    Returns
    -------
        list
            Votes
    """
    if part_share is None:
        print("IDUN_part generation : params None : random param generated")
        part_size = np.random.choice(range(num_voters))
    else:
        part_size = part_share * (num_voters)
    part_size = int(round(part_size))
    id_share = num_voters - part_size
    un_share = part_size
    votes = [[j for j in range(num_candidates)] for _ in range(id_share)]
    votes = votes + _draw_election(_distribute_in_matrix(un_share, num_candidates))
    return votes


@register_ordinal_election_culture('idst_part')
def generate_idst_part_votes(
        num_voters: int = None,
        num_candidates: int = None,
        part_share: float = None,
        **_kwargs
) -> list:
    """
    Generates elections realizing linear combinations of pos-matrices between (ID) and (ST)

    Parameters
    ----------
        num_voters : int
            Number of voters.
        num_candidates : int
            Number of candidates.
        part_share : float
            Share of ID voters.

    Returns
    -------
        list
            Votes
    """
    if part_share is None:
        print("IDST_part generation : params None : random param generated")
        part_size = np.random.choice(range(num_voters))
    else:
        part_size = part_share * (num_voters)
    part_size = int(round(part_size))
    id_share = num_voters - part_size
    st_share = part_size
    topsize = num_candidates // 2
    bottomsize = num_candidates - topsize
    votes_id = [[j for j in range(num_candidates)] for _ in range(id_share)]
    votes_st = _draw_election(_distribute_in_block_matrix(st_share, [topsize, bottomsize]))
    return votes_id + votes_st


@register_ordinal_election_culture('anun_part')
def generate_anun_part_votes(
        num_voters: int = None,
        num_candidates: int = None,
        part_share: float = None,
        **_kwargs
) -> list:
    """
    Generates elections realizing linear combinations of pos-matrices between (AN) and (UN).

    Parameters
    ----------
        num_voters : int
            Number of voters.
        num_candidates : int
            Number of candidates.
        part_share : float
            Share of AN voters.

    Returns
    -------
        list
            Votes
    """
    if part_share is None:
        print("ANUN_part generation : params None : random param generated")
        part_size = np.random.choice(range(num_voters))
    else:
        part_size = part_share * (num_voters)
    part_size = int(round(part_size))
    id_share = (num_voters - part_size) // 2
    op_share = num_voters - part_size - id_share
    un_share = num_voters - id_share - op_share
    votes = [[j for j in range(num_candidates)] for _ in range(id_share)]
    votes = votes + [[(num_candidates - j - 1) for j in range(num_candidates)] for _ in
                     range(op_share)]
    votes = votes + _draw_election(_distribute_in_matrix(un_share, num_candidates))
    return votes


@register_ordinal_election_culture('anst_part')
def generate_anst_part_votes(
        num_voters: int = None,
        num_candidates: int = None,
        part_share: float = None,
        **_kwargs
) -> list:
    """
    Generates elections realizing linear combinations of pos-matrices between (AN) and (ST)

    Parameters
    ----------
        num_voters : int
            Number of voters.
        num_candidates : int
            Number of candidates.
        part_share : float
            Share of AN voters.

    Returns
    -------
        list
            Votes
    """
    if part_share is None:
        print("ANST_part generation : params None : random param generated")
        part_size = np.random.choice(range(num_voters))
    else:
        part_size = part_share * (num_voters)
    part_size = int(round(part_size))
    id_share = (num_voters - part_size) // 2
    op_share = num_voters - part_size - id_share
    st_share = num_voters - id_share - op_share
    topsize = num_candidates // 2
    bottomsize = num_candidates - topsize
    votes = [[j for j in range(num_candidates)] for _ in range(id_share)]
    votes = votes + [[(num_candidates - j - 1) for j in range(num_candidates)] for _ in
                     range(op_share)]
    votes = votes + _draw_election(_distribute_in_block_matrix(st_share, [topsize, bottomsize]))
    return votes


@register_ordinal_election_culture('unst_part')
def generate_unst_part_votes(
        num_voters: int = None,
        num_candidates: int = None,
        part_share: float = None,
        **_kwargs
) -> list:
    """
    Generates elections realizing linear combinations of pos-matrices between (UN) and (ST).

    Parameters
    ----------
        num_voters : int
            Number of voters.
        num_candidates : int
            Number of candidates.
        part_share : float
            Share of UN voters.

    Returns
    -------
        list
            Votes
    """
    if part_share is None:
        print("UNST_part generation : params None : random param generated")
        part_size = np.random.choice(range(num_voters))
    else:
        part_size = part_share * (num_voters)
    part_size = int(round(part_size))
    un_share = num_voters - part_size
    st_share = part_size
    topsize = num_candidates // 2
    bottomsize = num_candidates - topsize
    votes = _draw_election(_distribute_in_matrix(un_share, num_candidates))
    votes = votes + _draw_election(_distribute_in_block_matrix(st_share, [topsize, bottomsize]))
    return votes


@register_ordinal_election_culture('unst_topsize')
def generate_unst_topsize_votes(
        num_voters: int = None,
        num_candidates: int = None,
        top_share: float = None,
        **_kwargs
):
    """ Generates kind of real elections between (UN) and (ST) """
    if top_share is None:
        print("UNST_topsize generation : params None : random param generated")
        top_share = np.random.random()
    else:
        top_share = top_share
    top_size = int(round(top_share * num_candidates))
    better = top_size
    worse = num_candidates - top_size
    matrix = _distribute_in_block_matrix(num_voters, [better, worse])
    return _draw_election(matrix)


@register_ordinal_election_culture('idst_blocks')
def generate_idst_blocks_votes(
        num_voters: int = None,
        num_candidates: int = None,
        num_blocks: int = None,
        **_kwargs
):
    """ Generates kind of real elections between (ID) and (ST) """
    if num_blocks is None:
        print("IDST_blocks generation : params None : random param generated")
        num_blocks = np.random.choice(range(num_candidates + 1))

    num_blocks = max(int(round(num_blocks)), 1)
    k = num_candidates // num_blocks
    r = num_candidates - k * num_blocks
    blocks = [k for _ in range(num_blocks)]
    with_one_more = list(np.random.choice(range(num_blocks), r, replace=False))
    for i in with_one_more:
        blocks[i] = blocks[i] + 1
    matrix = _distribute_in_block_matrix(num_voters, blocks)
    return _draw_election(matrix)


@register_ordinal_election_culture('approx_stratification')
def generate_approx_stratification_votes(
        num_voters: int = None,
        num_candidates: int = None,
        weight: float = 0.5
):
    """ Generates real election that approximates stratification (ST) """

    first_group_size = int(num_candidates * weight)

    votes_1 = generate_approx_uniformity_votes(num_voters, first_group_size)
    votes_2 = generate_approx_uniformity_votes(num_voters, num_candidates - first_group_size)

    for i in range(len(votes_2)):
        for j in range(len(votes_2[i])):
            votes_2[i][j] += first_group_size

    return [votes_1[i] + votes_2[i] for i in range(num_voters)]


@register_ordinal_election_culture('antagonism')
def generate_antagonism_votes(
        num_voters: int = None,
        num_candidates: int = None
) -> list:
    """
    Generates antagonism election.

    Parameters
    ----------
        num_voters : int
            Number of voters.
        num_candidates : int
            Number of candidates.

    Returns
    -------
        list
            Votes.

    """
    if num_voters % 2 != 0:
        logging.warning("Antagonism is not properly defined for odd number of voters")

    return [[j for j in range(num_candidates)] for _ in range(int(num_voters / 2))] + \
           [[num_candidates - j - 1 for j in range(num_candidates)] for _ in
            range(int(num_voters / 2))]
