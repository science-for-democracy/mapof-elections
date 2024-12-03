import itertools

import numpy as np

from mapof.elections.features.register import register_ordinal_election_feature

### AUXILLIARY FUNCTIONS ###

def _remove_diag(mtrx):
    """ Return: Input frequency_matrix with diagonal removed (shape[1] - 1) """
    res = np.zeros((mtrx.shape[0], mtrx.shape[1] - 1))
    for i in range(mtrx.shape[0]):
        for j in range(mtrx.shape[0]):
            if j < i:
                res[i, j] = mtrx[i, j]
            elif j > i:
                res[i, j - 1] = mtrx[i, j]
    return res


def _vote2pote(vote, m):
    reported = vote[vote != -1]
    part_pote = np.argsort(reported)
    res = []
    i = 0
    non_reported_pos = len(reported) + (m - 1 - len(reported)) / 2
    for c in range(m):
        if c in reported:
            res.append(part_pote[i])
            i = i + 1
        else:
            res.append(non_reported_pos)
    return np.array(res)


def _get_potes(election):
    if election.potes is not None:
        return election.potes
    else:
        res = []
        for v in election.votes:
            res.append(vote2pote(v, election.num_candidates))
        res = np.array(res)
        election.potes = res
        return res


def _swap_distance_between_potes(pote_1: list, pote_2: list, m: int) -> int:
    """ Return: Swap distance between two potes """
    swap_distance = 0
    for a in range(m):
        for b in range(m):
            if (pote_1[a] < pote_1[b] and pote_2[a] >= pote_2[b]):
                swap_distance += 0.5
            if (pote_1[a] <= pote_1[b] and pote_2[a] > pote_2[b]):
                swap_distance += 0.5
    return swap_distance


def _get_vote_dists(election):
    try:
        return election.vote_dists
    except:
        potes = get_potes(election)
        distances = np.zeros([election.num_voters, election.num_voters])
        for v1 in range(election.num_voters):
            for v2 in range(v1 + 1, election.num_voters):
                distances[v1][v2] = swap_distance_between_potes(potes[v1], potes[v2],
                                                                election.num_candidates)
                distances[v2][v1] = distances[v1][v2]
        election.vote_dists = distances
        return distances


def _get_candidate_dists(election):
    try:
        return election.candidate_dists
    except:
        potes = get_potes(election)
        distances = np.zeros([election.num_candidates, election.num_candidates])
        for a in range(election.num_candidates):
            for b in range(a + 1, election.num_candidates):
                for v in range(election.num_voters):
                    distances[a][b] += abs(potes[v][a] - potes[v][b])
                distances[b][a] = distances[a][b]
        election.candidate_dists = distances
        return distances


def _calculate_borda_scores(election):
    m = election.num_candidates
    borda = np.zeros(m, int)
    for v in election.votes:
        for i, c in enumerate(v):
            borda[c] = borda[c] + m - i - 1
    return borda

def _geom_mean(x):
    x = np.log(x)
    return np.exp(x.mean())

def _kemeny_ranking(election):
    m = election.num_candidates
    wmg = election.votes_to_pairwise_matrix()
    best_d = np.inf
    for test_ranking in itertools.permutations(list(range(m))):
        dist = 0
        for i in range(m):
            for j in range(i + 1, m):
                dist = dist + wmg[test_ranking[j], test_ranking[i]]
            if dist > best_d:
                break
        if dist < best_d:
            best = test_ranking
            best_d = dist
    return best, best_d
    

### AGREEMENT INDICES ###

@register_ordinal_election_feature('agreement')
def agreement_index(election) -> dict:
    """
    Calculates the agreement index of the election as defined in
    Faliszewski et al. 'Diversity, Agreement, and Polarization in Elections'.
    Agreement for a specific pair of candidates is defined as
    the difference between the number of their supporters
    divided by the total number of voters.
    Agreement index of an election is the average agreement
    between each pair of voters.


    Parameters
    ----------
        election : OrdinalElection

    Returns
    -------
        dict
            'value': agreement index
    """
    if election.is_pseudo:
        return {'value': None}
    potes = _get_potes(election)
    res = 0
    for a, b in itertools.combinations(range(election.num_candidates), 2):
        a_b = 0
        b_a = 0
        for p in potes:
            if p[a] < p[b]:
                a_b += 1
            elif p[b] < p[a]:
                b_a += 1
        res += max(abs(a_b - b_a), election.num_voters - a_b - b_a)
    return {'value': res / election.num_voters / (
                election.num_candidates - 1) / election.num_candidates * 2}


@register_ordinal_election_feature('borda_std')
def borda_std(election) -> dict:
    """
    Standard deviation of Borda scores of all candidates.
    """
    if election.is_pseudo:
        return {'value': None}
    all_scores = _calculate_borda_scores(election)
    return {'value': all_scores.std()}


@register_ordinal_election_feature('avg_vote_dist')
def avg_vote_dist(election) -> dict:
    """
    Average swap distance between voters.
    """
    if election.is_pseudo:
        return {'value': None}
    distances = _get_vote_dists(election)
    return {'value': distances.sum() / election.num_voters / (election.num_voters - 1)}


@register_ordinal_election_feature('max_vote_dist')
def max_vote_dist(election) -> dict:
    """
    Maximum swap distance between voters.
    """
    if election.is_pseudo:
        return {'value': None}
    distances = _get_vote_dists(election)
    return {'value': distances.max()}

@register_ordinal_election_feature('karpov_index')
def karpov_index(election):
    """
    Geometric mean based index proposed in
    Karpov's 'Preference diversity orderings' paper.
    """
    if election.is_pseudo:
        return {'value': None}
    distances = _get_vote_dists(election)
    distances = _remove_diag(distances)
    distances = distances + 0.5
    distances[distances == 0.5] = 1
    return {'value': _geom_mean(distances)}

@register_ordinal_election_feature('avg_dist_to_kemeny')
def avg_dist_to_kemeny(election):
    """
    Average swap distance between each voter and the Kemeny ranking.
    """
    if election.is_pseudo:
        return {'value': None}
    _, dist = _kemeny_ranking(election)
    return dist / election.num_voters

@register_ordinal_election_feature('avg_dist_to_borda')
def avg_dist_to_bord(election) -> dict:
    """
    Average swap distance between each voter and the Borda ranking.
    """
    if election.is_pseudo:
        return {'value': None}
    m = election.num_candidates
    borda = _calculate_borda_scores(election)
    ranking = np.argsort(-borda)
    wmg = election.votes_to_pairwise_matrix()
    dist = 0
    for i in range(m):
        for j in range(i + 1, m):
            dist = dist + wmg[ranking[j], ranking[i]]
    return {'value': dist / election.num_voters}


### DIVERSITY INDICES ###

@register_ordinal_election_feature('cand_pos_dist_std')
def cand_pos_dist_std(election) -> dict:
    """
    For each pair of candidates we calculate the average difference
    in positions across all voters. Then we take the standard deviation
    of the values for all pairs.
    """
    if election.is_pseudo:
        return {'value': None}
    distances = _get_candidate_dists(election)
    distances = _remove_diag(distances)
    return {'value': - distances.std() / election.num_voters}


def _distances_to_rankings(rankings, distances):
    dists = distances[rankings]
    return np.sum(dists.min(axis=0))


def _find_improvement(distances, d, starting, rest, k, l):
    for cut in itertools.combinations(range(k), l):
        for paste in itertools.combinations(rest, l):
            ranks = []
            j = 0
            for i in range(k):
                if i in cut:
                    ranks.append(paste[j])
                    j = j + 1
                else:
                    ranks.append(starting[i])
            # check if unique
            if len(set(ranks)) == len(ranks):
                # check if better
                d_new = _distances_to_rankings(ranks, distances)
                if d > d_new:
                    return ranks, d_new, True
    return starting, d, False



def local_search_kKemeny_single_k(election, k, l, starting=None) -> dict:
    if starting is None:
        starting = list(range(k))
    distances = _get_vote_dists(election)

    n = election.num_voters

    d = _distances_to_rankings(starting, distances)
    iter = 0
    check = True
    while (check):
        iter = iter + 1
        rest = [i for i in range(n) if i not in starting]
        for j in range(l):
            starting, d, check = _find_improvement(distances, d, starting, rest, k, j + 1)
            if check:
                break
    return {'value': d}


def kkemeny_diversity_upto_l(election, l) -> dict:
    if election.is_pseudo:
        return {'value': None}
    
    res = 0
    for k in range(l):
        res += local_search_kKemeny_single_k(election, k, 1)['value']

    k_1 = 
    k_2 = local_search_kKemeny_single_k(election, 2, 1)['value']
    k_3 = local_search_kKemeny_single_k(election, 3, 1)['value']
    k_4 = local_search_kKemeny_single_k(election, 4, 1)['value']
    k_5 = local_search_kKemeny_single_k(election, 5, 1)['value']

    max_dist = (election.num_candidates) * (election.num_candidates - 1) / 2
    return {'value': (k_1 + k_2 + k_3 + k_4 + k_5) / election.num_voters / max_dist}



@register_ordinal_election_feature('PolarizationApprox')
def polarization_index(election) -> dict:
    """
    Calculates the approx. polarization index of the election.

    Parameters
    ----------
        election : OrdinalElection

    Returns
    -------
        dict
            'value': approx. polarization index
    """
    if election.is_pseudo:
        return {'value': None}

    distances = get_vote_dists(election)
    best_1 = np.argmin(distances.sum(axis=1))
    best_vec = distances[best_1]
    first_kemeny = best_vec.sum()
    second_kemeny = local_search_kKemeny_single_k(election, 2, 1)['value']

    max_dist = (election.num_candidates) * (election.num_candidates - 1) / 2
    return {'value': 2 * (first_kemeny - second_kemeny) / election.num_voters / max_dist}