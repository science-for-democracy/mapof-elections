try:
    from abcvoting.preferences import Profile
    from abcvoting import abcrules, properties
    from abcvoting.output import output, INFO
except ImportError:
    pass

try:
    import gurobipy as gb
except ImportError:
    pass

from mapof.elections.features.register import register_approval_election_feature

ACCURACY = 1e-8  # 1e-9 causes problems (some unit tests fail)
CMP_ACCURACY = 10 * ACCURACY  # when comparing float numbers obtained from a MIP


def _set_gurobi_model_parameters(model):
    model.setParam("OutputFlag", False)
    model.setParam("FeasibilityTol", ACCURACY)
    model.setParam("OptimalityTol", ACCURACY)
    model.setParam("IntFeasTol", ACCURACY)
    model.setParam("MIPGap", ACCURACY)
    model.setParam("PoolSearchMode", 0)
    model.setParam("MIPFocus", 2)  # focus more attention on proving optimality
    model.setParam("IntegralityFocus", 1)


def _check_core_gurobi(profile, committee, committeesize):

    if not gb:
        raise ImportError("Gurobi (gurobipy) not available.")

    model = gb.Model()

    set_of_voter = model.addVars(range(len(profile)), vtype=gb.GRB.BINARY)
    set_of_candidates = model.addVars(range(profile.num_cand), vtype=gb.GRB.BINARY)

    model.addConstr(
        gb.quicksum(set_of_candidates) * len(profile) <= gb.quicksum(set_of_voter) * committeesize)
    model.addConstr(gb.quicksum(set_of_voter) >= 1)
    for i, voter in enumerate(profile):
        approved = [(c in voter.approved) * set_of_candidates[i] for i, c in
                    enumerate(profile.candidates)]
        model.addConstr(
            (set_of_voter[i] == 1) >>
            (gb.quicksum(approved) >= len(voter.approved & committee) + 1)
        )

    _set_gurobi_model_parameters(model)
    model.optimize()

    if model.Status == gb.GRB.OPTIMAL:
        return False
    elif model.Status == gb.GRB.INFEASIBLE:
        return True
    else:
        raise RuntimeError(f"Gurobi returned an unexpected status code: {model.Status}")


def _check_priceability_gurobi(profile, committee, stable=False):

    if len(
            [cand for cand in profile.candidates if
             any(cand in voter.approved for voter in profile)]
    ) < len(committee):
        return True

    if not gb:
        raise ImportError("Gurobi (gurobipy) not available.")

    model = gb.Model()

    budget = model.addVar(vtype=gb.GRB.CONTINUOUS)
    payment = {}
    for voter in profile:
        payment[voter] = {}
        for candidate in profile.candidates:
            payment[voter][candidate] = model.addVar(vtype=gb.GRB.CONTINUOUS)

    # condition 1
    for voter in profile:
        model.addConstr(
            gb.quicksum(payment[voter][candidate] for candidate in profile.candidates) <= budget)

    # condition 2
    for voter in profile:
        for candidate in profile.candidates:
            if candidate not in voter.approved:
                model.addConstr(payment[voter][candidate] == 0)

    # condition 3
    for candidate in profile.candidates:
        if candidate in committee:
            model.addConstr(gb.quicksum(payment[voter][candidate] for voter in profile) == 1)
        else:
            model.addConstr(gb.quicksum(payment[voter][candidate] for voter in profile) == 0)

    if stable:
        # condition 4*
        for candidate in profile.candidates:
            if candidate not in committee:
                extrema = []
                for voter in profile:
                    if candidate in voter.approved:
                        extremum = model.addVar(vtype=gb.GRB.CONTINUOUS)
                        extrema.append(extremum)
                        r = model.addVar(vtype=gb.GRB.CONTINUOUS)
                        max_Payment = model.addVar(vtype=gb.GRB.CONTINUOUS)
                        model.addConstr(r == budget - gb.quicksum(
                            payment[voter][committee_member] for committee_member in committee))
                        model.addGenConstrMax(max_Payment,
                                              [payment[voter][committee_member] for committee_member
                                               in committee])
                        model.addGenConstrMax(extremum, [max_Payment, r])
                model.addConstr(
                    gb.quicksum(extrema) <= 1
                )
    else:
        # condition 4
        for candidate in profile.candidates:
            if candidate not in committee:
                model.addConstr(
                    gb.quicksum(
                        budget - gb.quicksum(
                            payment[voter][committee_member] for committee_member in committee)
                        for voter in profile if candidate in voter.approved
                    ) <= 1)

    model.setObjective(budget)
    _set_gurobi_model_parameters(model)
    model.optimize()

    if model.Status == gb.GRB.OPTIMAL:
        output.details(f"Budget: {budget.X}")

        column_widths = {candidate: max(len(str(payment[voter][candidate].X)) for voter in payment)
                         for candidate in profile.candidates}
        column_widths["voter"] = len(str(len(profile)))
        output.details(" " * column_widths["voter"] + " | " + " | ".join(
            str(i).rjust(column_widths[candidate]) for i, candidate in
            enumerate(profile.candidates)))
        for i, voter in enumerate(profile):
            output.details(str(i).rjust(column_widths["voter"]) + " | " + " | ".join(
                str(pay.X).rjust(column_widths[candidate]) for candidate, pay in
                payment[voter].items()))

        return True
    elif model.Status == gb.GRB.INFEASIBLE:
        output.details(f"No feasible budget and payment function")
        return False
    else:
        raise RuntimeError(f"Gurobi returned an unexpected status code: {model.Status}")


@register_approval_election_feature("priceability", has_params=True, is_rule_related=True)
def get_priceability(election, feature_params):
    """ Computes priceability using ABC Python package. """

    rule = feature_params['rule']

    profile = Profile(election.num_candidates)
    profile.add_voters(election.votes)
    committee = election.winning_committee[rule]

    return {'value': int(_check_priceability_gurobi(profile, committee))}


@register_approval_election_feature("core", has_params=True, is_rule_related=True)
def get_core(election, feature_params):
    """ Computes the core using ABC Python package. """

    rule = feature_params['rule']

    profile = Profile(election.num_candidates)
    profile.add_voters(election.votes)
    committee = election.winning_committee[rule]

    return {'value': int(_check_core_gurobi(profile, committee, feature_params['committee_size']))}