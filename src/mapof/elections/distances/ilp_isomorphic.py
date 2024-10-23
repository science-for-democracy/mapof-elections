import logging

from gurobipy import Model, GRB


# THIS FUNCTION HAS NOT BEEN TESTED SINCE CONVERSION TO GUROBI
def solve_ilp_spearman_distance(votes_1, votes_2, params):
    model = Model("spearman_distance")
    model.setParam('Threads', 1)
    model.ModelSense = GRB.MINIMIZE

    P = {}
    M = {}
    N = {}

    # Define the P variables
    for k in range(params['voters']):
        for l in range(params['voters']):
            for i in range(params['candidates']):
                for j in range(params['candidates']):
                    weight = abs(list(votes_1[k]).index(i) - list(votes_2[l]).index(j))
                    P[k, l, i, j] = model.addVar(vtype=GRB.BINARY, name=f"P_{k}_{l}_{i}_{j}", obj=weight)

    # Define the M variables
    for i in range(params['candidates']):
        for j in range(params['candidates']):
            M[i, j] = model.addVar(vtype=GRB.BINARY, name=f"M_{i}_{j}")

    # Define the N variables
    for k in range(params['voters']):
        for l in range(params['voters']):
            N[k, l] = model.addVar(vtype=GRB.BINARY, name=f"N_{k}_{l}")

    model.update()

    # Add the constraints
    for k in range(params['voters']):
        for l in range(params['voters']):
            for i in range(params['candidates']):
                for j in range(params['candidates']):
                    model.addConstr(P[k, l, i, j] <= M[i, j], name=f"c1_{k}_{l}_{i}_{j}_1")
                    model.addConstr(P[k, l, i, j] <= N[k, l], name=f"c1_{k}_{l}_{i}_{j}_2")

    # N constraints for voters
    for k in range(params['voters']):
        model.addConstr(sum(N[k, l] for l in range(params['voters'])) == 1, name=f"c2_{k}")

    for l in range(params['voters']):
        model.addConstr(sum(N[k, l] for k in range(params['voters'])) == 1, name=f"c3_{l}")

    # M constraints for candidates
    for i in range(params['candidates']):
        model.addConstr(sum(M[i, j] for j in range(params['candidates'])) == 1, name=f"c4_{i}")

    for j in range(params['candidates']):
        model.addConstr(sum(M[i, j] for i in range(params['candidates'])) == 1, name=f"c5_{j}")

    # P constraints for voters and candidates
    for k in range(params['voters']):
        for i in range(params['candidates']):
            model.addConstr(sum(P[k, l, i, j] for l in range(params['voters']) for j in range(params['candidates'])) == 1, name=f"c6_{k}_{i}")

    for l in range(params['voters']):
        for j in range(params['candidates']):
            model.addConstr(sum(P[k, l, i, j] for k in range(params['voters']) for i in range(params['candidates'])) == 1, name=f"c7_{l}_{j}")

    # Solve the model
    model.optimize()

    if model.status != GRB.OPTIMAL:
        logging.warning("No optimal solution found")

    return model.objVal
