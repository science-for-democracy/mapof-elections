import logging
from itertools import combinations, permutations
import numpy as np

from mapof.core.matchings import solve_matching_vectors, solve_matching_matrices
from mapof.elections.objects.OrdinalElection import OrdinalElection
import mapof.core.utils as utils
from mapof.core.distances import swap_distance
import mapof.elections.distances.ilp_isomorphic as ilp_iso
from mapof.elections.distances.ilp_subelections import maximum_common_voter_subelection

from mapof.elections.distances.register import register_ordinal_election_distance

try:
    import mapof.elections.distances.cppdistances as cppd
except:
    logging.warning("The quick C++ procedures for computing the swap and "
                    "Spearman distance is unavailable: using the (slow) python one instead")


@register_ordinal_election_distance("pos_swap")
def pos_swap_distance(
        election_1: OrdinalElection,
        election_2: OrdinalElection,
        inner_distance: callable
) -> (float, list):
    """ Compute Positionwise-Swap distance between ordinal elections """
    logging.warning("Positionwise-Swap distance wasn't properly tested.")
    cost_table = get_matching_cost_positionwise(election_1, election_2, inner_distance)
    obj_val, matching = solve_matching_vectors(cost_table)
    cost_table = get_matching_cost_pos_swap(election_1, election_2, matching)
    return solve_matching_vectors(cost_table)


@register_ordinal_election_distance("positionwise")
def positionwise_distance(
        election_1,
        election_2,
        inner_distance: callable
) -> (float, list):
    """
    Compute Positionwise distance between ordinal elections.

    Parameters
    ----------
        election_1 : OrdinalElection
            First election to compare.
        election_2 : OrdinalElection
            Second election to compare.
        inner_distance : callable
            Inner distance to use.

    Returns
    -------
        (float, list)
            Positionwise distance between the two elections and the optimal matching.
    """
    cost_table = get_matching_cost_positionwise(election_1, election_2, inner_distance)
    return solve_matching_vectors(cost_table)


@register_ordinal_election_distance("agg_voterlikeness")
def agg_voterlikeness_distance(election_1: OrdinalElection, election_2: OrdinalElection,
                                       inner_distance: callable) -> (float, list):
    """ Compute Aggregated-Voterlikeness distance between ordinal elections """
    logging.warning("Aggregated-Voterlikeness distance wasn't properly tested.")
    vector_1, num_possible_scores = election_1.votes_to_agg_voterlikeness_vector()
    vector_2, _ = election_2.votes_to_agg_voterlikeness_vector()
    return inner_distance(vector_1, vector_2, num_possible_scores)


@register_ordinal_election_distance("bordawise")
def bordawise_distance(
        election_1: OrdinalElection,
        election_2: OrdinalElection,
        inner_distance: callable
) -> (float, None):
    """
    Computes Bordawise distance between ordinal elections.

    Parameters
    ----------
        election_1 : OrdinalElection
            First election to compare.
        election_2 : OrdinalElection.
            Second election to compare.
        inner_distance : callable
            Inner distance to use.

    Returns
    -------
        (float, list | None)
            Bordawise distance between the two elections.
    """
    vector_1 = election_1.get_bordawise_vector()
    vector_2 = election_2.get_bordawise_vector()
    return inner_distance(vector_1, vector_2), None


@register_ordinal_election_distance("pairwise")
def pairwise_distance(
        election_1: OrdinalElection,
        election_2: OrdinalElection,
        inner_distance: callable
) -> (float, None):
    """
    Compute Pairwise distance between ordinal elections.

    Parameters
    ----------
        election_1 : OrdinalElection
            First election to compare.
        election_2 : OrdinalElection.
            Second election to compare.
        inner_distance : callable
            Inner distance to use.

    Returns
    -------
        (float, None)
            Pairwise distance between the two elections.
    """
    length = election_1.num_candidates
    matrix_1 = election_1.votes_to_pairwise_matrix()
    matrix_2 = election_2.votes_to_pairwise_matrix()
    return solve_matching_matrices(matrix_1, matrix_2, length, inner_distance), None


@register_ordinal_election_distance("voterlikeness")
def voterlikeness_distance(
        election_1: OrdinalElection,
        election_2: OrdinalElection,
        inner_distance: callable
) -> (float, list):
    """ Compute Voterlikeness distance between elections.

    Parameters
    ----------
        election_1 : OrdinalElection
            First election to compare.
        election_2 : OrdinalElection.
            Second election to compare.
        inner_distance : callable
            Inner distance to use.

    Returns
    -------
        (float, None)
            Voterlikeness distance between the two elections.
    """
    logging.warning("Voterlikeness distance wasn't properly tested.")
    length = election_1.num_voters
    matrix_1 = election_1.votes_to_voterlikeness_matrix()
    matrix_2 = election_2.votes_to_voterlikeness_matrix()
    return solve_matching_matrices(matrix_1, matrix_2, length, inner_distance), None


@register_ordinal_election_distance("swap_bf")
def swap_distance_bf(election_1: OrdinalElection,
                             election_2: OrdinalElection) -> (int, list):
    """ Compute swap distance between elections via brute force, in Python.
    This is mostly as a fallback to the C++ implementation, which might
    ocassionally be unavailable for some due to envorinoment issues
    (lack of proper tools under MS Windows, old compilers, etc.)"""
    obj_values = []
    for mapping in permutations(range(election_1.num_candidates)):
        cost_table = get_matching_cost_swap_bf(election_1, election_2, mapping)
        obj_values.append(solve_matching_vectors(cost_table)[0])
    return min(obj_values), None


@register_ordinal_election_distance("swap")
def swap_distance(election_1: OrdinalElection,
                          election_2: OrdinalElection) -> (int, list):
    """ Compute swap distance between elections (using the C++ extension) """
    if not utils.is_module_loaded("mapof.elections.distances.cppdistances"):
        logging.warning("Using Python implementation instead of the C++ one")
        return swap_distance_bf(election_1, election_2), None

    if election_1.num_candidates < election_2.num_candidates:
        swapd = cppd.tswapd(election_1.votes.tolist(),
                            election_2.votes.tolist())
    elif election_1.num_candidates > election_2.num_candidates:
        swapd = cppd.tswapd(election_2.votes.tolist(),
                            election_1.votes.tolist())
    else:
        swapd = cppd.swapd(election_1.votes.tolist(),
                           election_2.votes.tolist())

    return swapd, None


@register_ordinal_election_distance("truncated_swap")
def truncated_swap_distance(election_1: OrdinalElection,
                                    election_2: OrdinalElection) -> (int, list):
    """ Compute truncated swap distance between elections """
    obj_values = []
    for mapping in permutations(range(election_1.num_candidates)):
        cost_table = get_matching_cost_truncated_swap_bf(election_1, election_2, mapping)
        obj_values.append(solve_matching_vectors(cost_table)[0])
    return min(obj_values), None


@register_ordinal_election_distance("spearman")
def spearman_distance(election_1: OrdinalElection,
                              election_2: OrdinalElection) -> (int, list):
    """ Compute Spearman distance between elections (using the C++ extension) """
    if not utils.is_module_loaded("mapof.elections.distances.cppdistances"):
        return spearman_distance_ilp_py(election_1, election_2), None
    speard = cppd.speard(election_1.votes.tolist(),
                         election_2.votes.tolist())
    return speard, None


@register_ordinal_election_distance("spearman_aa")
def spearman_distance_fastmap(
        election_1: OrdinalElection,
        election_2: OrdinalElection,
        method: str = "aa"
) -> tuple[int, list | None]:
    """Computes Isomorphic Spearman distance between elections using `fastmap` library.

    Args:
        election_1: First ordinal election. election_2: Second ordinal election. method: Method used
        to compute the distance. Should be one of the
                `"bf"` - uses brute-force to solve the equivalent Bilinear Assignment Problem (BAP).
                    Generates all permutations σ of the set {0,..,min(nv-1,nc-1)} using Heap's
                    algorithm and for each generated permutation σ solves the Linear Assignment
                    Problem (LAP) to obtain the optimal permutation v of {0,..,max(nv-1,nc-1)}. Time
                    complexity of this method is O(min(nv,nc)! * max(nv,nc)**3)

                    NOTE: This method returns exact value but if one of the nv, nc is greater than
                    10 it is extremely slow.

                `"aa"` - implements Alternating Algorithm heuristic described in arXiv:1707.07057
                    which solves the equivalent Bilinear Assignment Problem (BAP). The algorithm
                    first generates a feasible solution to the BAP by sampling from a uniform
                    distribution two permutations σ, v and then performs a coordinate-descent-like
                    refinment by interchangeably fixing one of the permutations, solving the
                    corresponding Linear Assignment Problem (LAP) and updating the other permutation
                    with the matching found in LAP, doing so until convergence. Time complexity of
                    this method is O(N * (nv**3 + nc**3)) where N is the number of iterations it
                    takes for the algorithm to converge.

                    NOTE: This method is much faster in practice than "bf" but there are no
                    theoretical guarantees on the approximation ratio for the used heuristic.

                `"bb"` - implements Branch-and-Bound algorithm to solve exactly the equivalent
                    Bilinear Assigmnent Problem (BAP).

                    NOTE: Performance of this method highly depends on the cultures from which the
                    elections were sampled. In the worst case scenario it may be significantly
                    slower than "bf". Also due to the implemented bounding function this method is
                    not suited for instances with more than few dozen voters.  

    Raises:
        ImportError: Raises exception if `fastmap` module is not found.

    Returns:
        Tuple of Isomorphic Spearman distance value and None.
    """
    try:
        import fastmap
    except ImportError as e:
        raise ImportError("`fastmap` library module not found") from e

    U, V = np.array(election_1.votes), np.array(election_2.votes)
    d = fastmap.spearman(U=U, V=V, method=method)

    return d, None


@register_ordinal_election_distance("ilp_spearman")
def spearman_distance_ilp_py(election_1: OrdinalElection,
                                     election_2: OrdinalElection) -> (int, list):
    """ Computes Spearman distance between elections """
    logging.warning("ilp_spearman wasn't properly tested.")
    votes_1 = election_1.votes
    votes_2 = election_2.votes
    params = {'voters': election_1.num_voters,
              'candidates': election_1.num_candidates}

    objective_value = ilp_iso.solve_ilp_spearman_distance(votes_1, votes_2, params)
    objective_value = int(round(objective_value, 0))
    return objective_value, None


@register_ordinal_election_distance("discrete")
def discrete_distance(election_1: OrdinalElection,
                              election_2: OrdinalElection) -> (int, list):
    """ Computes Discrete distance between elections """
    return election_1.num_voters - maximum_common_voter_subelection(election_1, election_2), None


# HELPER FUNCTIONS #
def get_matching_cost_pos_swap(election_1: OrdinalElection, election_2: OrdinalElection,
                               matching) -> list[list]:
    """ Return: Cost table """
    votes_1 = election_1.votes
    votes_2 = election_2.votes
    size = election_1.num_voters
    return [[swap_distance(votes_1[i], votes_2[j], matching=matching) for i in range(size)]
            for j in range(size)]


def get_matching_cost_positionwise(election_1: OrdinalElection, election_2: OrdinalElection,
                                   inner_distance: callable) -> list[list]:
    """ Return: Cost table """

    matrix_1 = election_1.get_frequency_matrix()
    matrix_2 = election_2.get_frequency_matrix()
    size = election_1.num_candidates
    return [[inner_distance(matrix_1[i], matrix_2[j]) for i in range(size)] for j in range(size)]


def get_matching_cost_swap_bf(election_1: OrdinalElection, election_2: OrdinalElection,
                              mapping):
    """ Return: Cost table """
    cost_table = np.zeros([election_1.num_voters, election_1.num_voters])

    election_1.get_potes()
    election_2.get_potes()

    for v1 in range(election_1.num_voters):
        for v2 in range(election_2.num_voters):
            swap_distance = 0
            for i, j in combinations(election_1.potes[0], 2):
                if (election_1.potes[v1][i] > election_1.potes[v1][j] and
                    election_2.potes[v2][mapping[i]] < election_2.potes[v2][mapping[j]]) or \
                        (election_1.potes[v1][i] < election_1.potes[v1][j] and
                         election_2.potes[v2][mapping[i]] > election_2.potes[v2][mapping[j]]):
                    swap_distance += 1
            cost_table[v1][v2] = swap_distance
    return cost_table


def get_matching_cost_truncated_swap_bf(election_1: OrdinalElection,
                                        election_2: OrdinalElection,
                                        mapping):
    """ Return: Cost table """
    cost_table = np.zeros([election_1.num_voters, election_1.num_voters])

    election_1.get_potes()
    election_2.get_potes()

    for v1 in range(election_1.num_voters):
        for v2 in range(election_2.num_voters):
            swap_distance = 0
            for i, j in combinations(election_1.potes[0], 2):
                if (election_1.potes[v1][i] > election_1.potes[v1][j] and
                    election_2.potes[v2][mapping[i]] < election_2.potes[v2][mapping[j]]) or \
                        (election_1.potes[v1][i] < election_1.potes[v1][j] and
                         election_2.potes[v2][mapping[i]] > election_2.potes[v2][mapping[j]]):
                    swap_distance += 1
            cost_table[v1][v2] = swap_distance
    return cost_table


@register_ordinal_election_distance("blank")
def blank_distance(
        election_1: OrdinalElection,
        election_2: OrdinalElection
) -> (int, list):
    """ Computes blank distance for testing purposes. """
    return 1, None
