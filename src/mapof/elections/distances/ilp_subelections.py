import logging

import gurobipy as gp
from gurobipy import GRB

from mapof.elections.distances.register import register_ordinal_election_distance


# THIS FUNCTION HAS NOT BEEN TESTED SINCE CONVERSION TO GUROBI
@register_ordinal_election_distance("maximum_common_voter_subelection")
def maximum_common_voter_subelection(election_1, election_2, metric_name='0') -> int:
    """
    This function solves the maximum common voter subelection problem between two elections.

    Parameters
    ----------
        election_1 : Election
            The first election.
        election_2 : Election
            The second election.
        metric_name : str

    Returns
    -------
        int
            The maximum number of common voters between the two elections.
    """
    # Initialize model
    model = gp.Model()

    # Limit the number of threads
    model.setParam('Threads', 1)

    # OBJECTIVE FUNCTION
    names = []
    for v1 in range(election_1.num_voters):
        for v2 in range(election_2.num_voters):
            names.append('N' + str(v1) + '_' + str(v2))

    # Add variables
    N_vars = model.addVars(names, vtype=GRB.BINARY, obj=1.0, name="N")

    # Set objective to maximize
    model.ModelSense = GRB.MAXIMIZE

    # FIRST CONSTRAINT FOR VOTERS
    for v1 in range(election_1.num_voters):
        model.addConstr(gp.quicksum(
            N_vars['N' + str(v1) + '_' + str(v2)] for v2 in range(election_2.num_voters)) <= 1.0,
                        name='C1_' + str(v1))

    # SECOND CONSTRAINT FOR VOTERS
    for v2 in range(election_2.num_voters):
        model.addConstr(gp.quicksum(
            N_vars['N' + str(v1) + '_' + str(v2)] for v1 in range(election_1.num_voters)) <= 1.0,
                        name='C2_' + str(v2))

    # ADD VARIABLES FOR CANDIDATES
    M_names = []
    for c1 in range(election_1.num_candidates):
        for c2 in range(election_2.num_candidates):
            M_names.append('M' + str(c1) + '_' + str(c2))

    M_vars = model.addVars(M_names, vtype=GRB.BINARY, name="M")

    # FIRST CONSTRAINT FOR CANDIDATES
    for c1 in range(election_1.num_candidates):
        model.addConstr(gp.quicksum(M_vars['M' + str(c1) + '_' + str(c2)] for c2 in
                                    range(election_2.num_candidates)) == 1.0,
                        name='C3_' + str(c1))

    # SECOND CONSTRAINT FOR CANDIDATES
    for c2 in range(election_2.num_candidates):
        model.addConstr(gp.quicksum(M_vars['M' + str(c1) + '_' + str(c2)] for c1 in
                                    range(election_1.num_candidates)) == 1.0,
                        name='C4_' + str(c2))

    # MAIN CONSTRAINT FOR VOTES
    potes_1 = election_1.get_potes()
    potes_2 = election_2.get_potes()

    for v1 in range(election_1.num_voters):
        for v2 in range(election_2.num_voters):
            M_constr = gp.LinExpr()
            for c1 in range(election_1.num_candidates):
                for c2 in range(election_2.num_candidates):
                    if abs(potes_1[v1][c1] - potes_2[v2][c2]) <= int(metric_name):
                        M_constr += M_vars['M' + str(c1) + '_' + str(c2)]
            M_constr -= N_vars['N' + str(v1) + '_' + str(v2)] * election_1.num_candidates
            model.addConstr(M_constr >= 0.0, name='C5_' + str(v1) + '_' + str(v2))

    # Optimize the model
    model.optimize()

    # Return the objective value
    if model.status == GRB.OPTIMAL:
        return model.objVal
    else:
        logging.warning("No optimal solution found")
