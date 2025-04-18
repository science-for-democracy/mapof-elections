import logging

from numpy import ceil

from mapof.elections.features.register import register_approval_election_feature

try:
    import pulp
except Exception:
    logging.warning("Pulp Voting library not found. Some features may not work.")
    pulp = None

try:
    from abcvoting import abcrules, preferences
except ImportError:
    logging.warning("ABC Voting library not found. Some features may not work.")
    abcrules = None
    preferences = None


def calculate_committees(
        election,
        resolute=False,
        committee_size: int = 10,
        rule_name=None
) -> set:
    """ Calculate the committees using ABC Voting library. """

    profile = preferences.Profile(num_cand=election.num_candidates)
    profile.add_voters(election.votes)
    try:
        committees = abcrules.compute(rule_name, profile, committee_size, resolute=resolute)
    except Exception:
        committees = {}

    return committees


def count_proportionality_degree_of_a_committee(
        election,
        committee: set,
        committee_size: int = 10
) -> map:
    """ Counts proportionality degree of a given committee """
    f_map = dict()
    for l in range(1, committee_size + 1):
        val = solve_ilp_instance(election, committee, l, committee_size=committee_size)
        f_map[l] = val
    return f_map


def solve_ilp_instance(election, committee: set, l: int = 1,
                       committee_size: int = 10) -> float:
    model = pulp.LpProblem("pd_value_f", pulp.LpMinimize)
    X = [pulp.LpVariable("x_" + str(i), cat='Binary') for i in
         range(election.num_voters)]  # X[i] = 1 if we select i-th voter, otherwise 0
    Y = [pulp.LpVariable("y_" + str(j), cat='Binary') for j in
         range(election.num_candidates)]  # Y[j] = 1 if we select j-th candidate, otherwise 0
    s = int(ceil(
        l * election.num_voters / committee_size))  # If there is any valid l-cohesive group, then there is also at least one with minimum possible size

    objective = 0
    for v in range(election.num_voters):
        cands = election.votes[v]
        for c in committee:
            if c in cands:
                objective += X[v]
    model += objective  # We want to minimize the number of votes

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

    # pseudo_culture_id.solve()

    model.solve(pulp.PULP_CBC_CMD(msg=False))
    # if LpStatus[pseudo_culture_id.status] == 'Optimal':
    #     print([var.election_id + "=" + str(var.varValue) for var in pseudo_culture_id.variables() if var.varValue is not None and var.varValue > 0], sep=" ")    # prints result variables which have value > 0
    if pulp.LpStatus[model.status] == 'Optimal':
        return pulp.value(model.objective) / s
    else:
        # return np.inf
        return 0.


def proportionality_degree(election, feature_params):

    committee_size = feature_params.get('committee_size')
    rule_name = feature_params.get('rule_name', None)
    resolute = feature_params.get('resolute', False)

    committees = calculate_committees(election,
                                      committee_size=committee_size,
                                      rule_name=rule_name,
                                      resolute=resolute)

    if len(committees) == 0:
        return 0

    all_pd = []
    for committee in committees:
        pd_1 = solve_ilp_instance(election, committee, 1, committee_size=committee_size)
        all_pd.append(pd_1)
    return sum(all_pd) / len(all_pd)


@register_approval_election_feature("proportionality_degree_av")
def proportionality_degree_av(*args, feature_params, **kwargs):
    feature_params['rule_name'] = 'av'
    return proportionality_degree(*args, feature_params=feature_params, **kwargs)


@register_approval_election_feature("proportionality_degree_pav")
def proportionality_degree_pav(*args, feature_params, **kwargs):
    feature_params['rule_name'] = 'pav'
    return proportionality_degree(*args, feature_params=feature_params, **kwargs)


@register_approval_election_feature("proportionality_degree_cc")
def proportionality_degree_cc(*args, feature_params, **kwargs):
    feature_params['rule_name'] = 'cc'
    feature_params['resolute'] = True
    return proportionality_degree(*args, feature_params=feature_params, **kwargs)
