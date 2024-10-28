import itertools
import logging
import time
from collections import defaultdict

from mapof.elections.features.register import register_approval_election_feature

from numpy import ceil

try:
    import pulp
except Exception:
    logging.warning("Pulp not found. Some features may not work.")
    pulp = None


@register_approval_election_feature('number_of_cohesive_groups_brute', has_params=True)
def count_number_of_cohesive_groups_brute(
    election,
    feature_params: dict
):
    """
    Count the number of cohesive groups of size at least l in the election, using Brute Force.
    """
    l = feature_params.get('l', 1)
    committee_size = feature_params['committee_size']
    answer = 0
    min_size = int(ceil(l * election.num_voters / committee_size))
    voters = [i for i in range(0, election.num_voters)]
    for s in powerset(voters, min_size=min_size):
        if len(s) < min_size:
            continue
        cands = set(election.votes[s[0]])
        for v in s:
            cands &= election.votes[v]
        if len(cands) >= l:
            answer += 1
    return answer


####################################################################################################
####################################################################################################
####################################################################################################

def powerset(iterable, min_size=0):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(min_size, len(s) + 1))


def newton(n: int, k: int):
    if k > n:
        return 0
    answer = 1
    for i in range(n - k + 1, n + 1):
        answer *= i
    for i in range(1, k + 1):
        answer //= i
    return answer


@register_approval_election_feature('number_of_cohesive_groups', has_params=True)
def count_number_of_cohesive_groups(
    election,
    feature_params: dict
):
    l = feature_params.get('l', 1)
    committee_size = feature_params['committee_size']
    if l > 1:
        raise NotImplementedError()
    answer = 0
    d = defaultdict(lambda: 0)
    timeout = time.time() + 20 * 1  # 20s from now
    for v in range(election.num_voters):
        for s in powerset(election.votes[v], min_size=1):
            d[s] += 1
            if time.time() > timeout:
                return -1
    min_size = int(ceil(l * election.num_voters / committee_size))
    for s in d:
        for siz in range(min_size, d[s] + 1):
            sign = 2 * (len(s) % 2) - 1  # 1 for even, -1 for odd, comes from (-1) ^ (s-1)
            answer += newton(d[s], siz) * sign
    return answer


####################################################################################################
####################################################################################################
####################################################################################################

@register_approval_election_feature('cohesiveness', has_params=True)
def count_largest_cohesiveness_level_l_of_cohesive_group(
    election,
    feature_params: dict
):
    committee_size = feature_params['committee_size']
    l_ans = 0
    for l in range(1, election.num_voters + 1):
        if solve_ilp_instance(election, committee_size, l):
            l_ans = l
        else:
            break
    return l_ans


def solve_ilp_instance(election, committee_size: int, l: int = 1) -> bool:
    pulp.getSolver('GUROBI')
    model = pulp.LpProblem("cohesiveness_level_l", pulp.LpMaximize)
    X = [pulp.LpVariable("x_" + str(i), cat='Binary') for i in
         range(election.num_voters)]  # X[i] = 1 if we select i-th voter, otherwise 0
    Y = [pulp.LpVariable("y_" + str(j), cat='Binary') for j in
         range(election.num_candidates)]  # Y[j] = 1 if we select j-th candidate, otherwise 0
    s = int(ceil(
        l * election.num_voters / committee_size))  # If there is any valid l-cohesive group, then there is also at least one with minimum possible size

    objective = l
    model += objective  # We want to maximize cohesiveness level l (but l is constant, only convention)

    x_sum_eq = 0
    for x in X:
        x_sum_eq += x
    model += x_sum_eq == s  # We choose exactly s voters

    y_sum_ineq = 0
    for y in Y:
        y_sum_ineq += y
    model += y_sum_ineq >= l  # We choose at least l candidates (although l are sufficient in this case)

    cand_to_voters_variables_list = [[] for j in range(election.num_candidates)]
    for i, d in enumerate(election.votes):
        for j in d:
            cand_to_voters_variables_list[j].append(X[i])
    # We want to assert that the selected voters approve all the selected candidates.
    # For each candidate j,  we construct the following inequality:  a_{0,j} * x_0 + a_{1,j} * x_1 + ... + a_{n-1,j} * x_{n-1}  -   s * y_j    >=    0
    # We define a_{i, j} as the flag indicating whether i-th voter approves j-th candidate (1 if yes, otherwise 0)
    # Let us observe that if the j-th candidate is not selected, then s * y_j = 0 and the above inequality is naturally satisfied.
    # However, if j-th candidate is selected, then the above can be satisfied if and only if all s selected voters approve j-th candidate
    for j, y in enumerate(Y):
        y_ineq = 0
        for x in cand_to_voters_variables_list[j]:
            y_ineq += x
        y_ineq -= s * y
        model += y_ineq >= 0

    model.solve(pulp.PULP_CBC_CMD(msg=False))

    return pulp.LpStatus[model.status] == 'Optimal'
