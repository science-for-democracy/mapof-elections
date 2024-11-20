import logging
import math
import os
from contextlib import suppress

from gurobipy import LinExpr, Model, GRB


# THIS FUNCTION HAS NOT BEEN TESTED SINCE CONVERSION TO GUROBI
def solve_lp_matching_vector_with_lp(cost_table, length):

    # Create a new model
    model = Model("vectors_matching")
    model.setParam('Threads', 1)

    # Length of the cost table
    length = len(cost_table)

    # Variables
    x = {}
    for i in range(length):
        for j in range(length):
            x[i, j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")

    # Objective function
    model.setObjective(
        sum(cost_table[i][j] * x[i, j] for i in range(length) for j in range(length)), GRB.MINIMIZE)

    # First group of constraints
    for i in range(length):
        model.addConstr(sum(x[i, j] for j in range(length)) == 1, name=f"row_{i}")

    # Second group of constraints
    for j in range(length):
        model.addConstr(sum(x[i, j] for i in range(length)) == 1, name=f"col_{j}")

    # Solve the model
    model.optimize()

    # If a solution was found, return the objective value
    if model.status == GRB.OPTIMAL:
        objective_value = model.objVal
        print(f"Objective Value: {objective_value}")
    else:
        print("No optimal solution found")


# THIS FUNCTION HAS NOT BEEN TESTED SINCE CONVERSION TO GUROBI
def solve_lp_matching_interval(cost_table, length_1, length_2):
    precision = length_1 * length_2

    # Create a new model
    model = Model("lp_matching_interval")
    model.setParam('Threads', 1)

    # Variables
    x = {}
    for i in range(length_1):
        for j in range(length_2):
            x[i, j] = model.addVar(vtype=GRB.INTEGER, name=f"x_{i}_{j}")

    # Objective function
    model.setObjective(sum(cost_table[i][j] * x[i, j] for i in range(length_1) for j in range(length_2)), GRB.MINIMIZE)

    # First group of constraints
    for i in range(length_1):
        model.addConstr(sum(x[i, j] for j in range(length_2)) == length_2, name=f"c1_{i}")

    # Second group of constraints
    for j in range(length_2):
        model.addConstr(sum(x[i, j] for i in range(length_1)) == length_1, name=f"c2_{j}")

    # Save the model to files
    model.write('interval.lp')
    model.write('interval.mps')

    # Solve the model
    model.optimize()

    # If a solution was found, return the objective value divided by precision
    if model.status == GRB.OPTIMAL:
        result = model.objVal / precision
        return result
    else:
        print("No optimal solution found")
        return None


# THIS FUNCTION HAS NOT BEEN TESTED SINCE CONVERSION TO GUROBI
def solve_lp_file_dodgson_score(N=None, e=None, D=None) -> float:
    # Create a new model
    model = Model("dodgson_score")
    model.setParam('Threads', 1)

    # Objective function variables and coefficients
    names = []
    obj = []
    for i in range(len(N)):
        for j in range(1, len(D)):
            var_name = f"y_{i}_{j}"
            names.append(var_name)
            obj.append(j)
            model.addVar(vtype=GRB.INTEGER, name=var_name, obj=j)

    # Add missing variables for j=0
    for i in range(len(N)):
        var_name = f"y_{i}_0"
        model.addVar(vtype=GRB.INTEGER, name=var_name)

    model.update()

    # Objective function
    model.setObjective(sum(model.getVarByName(f"y_{i}_{j}") * j
                           for i in range(len(N))
                           for j in range(1, len(D))), GRB.MINIMIZE)

    # First group of constraints
    for i in range(len(N)):
        model.addConstr(model.getVarByName(f"y_{i}_0") == N[i], name=f"C1_{i}")

    # Second group of constraints
    for k in range(len(D)):
        val = []
        ind = []
        for i in range(len(N)):
            for j in range(1, len(D)):
                ind.append(model.getVarByName(f"y_{i}_{j}"))
                value = e[i][j][k] - e[i][j - 1][k]
                val.append(value)
        model.addConstr(sum(ind[l] * val[l] for l in range(len(ind))) >= D[k], name=f"C2_{k}")

    # Third group of constraints
    for i in range(len(N)):
        for j in range(1, len(D)):
            model.addConstr(model.getVarByName(f"y_{i}_{j - 1}") - model.getVarByName(f"y_{i}_{j}") >= 0,
                            name=f"C3_{i}_{j}")

    # Solve the model
    model.optimize()

    # If a solution was found, return the objective value
    if model.status == GRB.OPTIMAL:
        return model.objVal
    else:
        logging.warning("No optimal solution found")


# THIS FUNCTION HAS NOT BEEN TESTED SINCE CONVERSION TO GUROBI
def solve_lp_borda_owa(election, committee_size, owa):

    num_voters = election.num_voters
    num_candidates = election.num_candidates
    num_orders = committee_size

    # Create a new model
    model = Model("borda_owa")
    model.setParam('Threads', 1)

    # Objective function variables and coefficients
    x = {}
    for i in range(num_voters):
        for j in range(num_orders):
            for k in range(num_candidates):
                var_name = f"x_{i}_{j}_{k}"
                x[i, j, k] = model.addVar(vtype=GRB.BINARY, name=var_name, obj=owa[j])

    # Add variables for candidates
    y = {}
    for i in range(num_candidates):
        y[i] = model.addVar(vtype=GRB.BINARY, name=f"y_{i}")

    model.update()

    # Objective function
    model.ModelSense = GRB.MAXIMIZE

    # First group of constraints
    model.addConstr(sum(y[i] for i in range(num_candidates)) == num_orders, name="c1")

    # Second group of constraints
    for i in range(num_voters):
        for j in range(num_candidates):
            model.addConstr(sum(x[i, k, j] for k in range(num_orders))
                            <= sum(y[int(election.votes[i][k])] for k in range(0, j + 1)),
                            name=f"c2_{i}_{j}")

    # Solve the model
    model.setParam('OutputFlag', 0)
    start = model.getAttr(GRB.Attr.Runtime)
    model.optimize()
    stop = model.getAttr(GRB.Attr.Runtime)

    if model.status != GRB.OPTIMAL:
        print("Exception raised during solve")
        return None, stop-start

    # Extract winners
    result = [y[i].X for i in range(num_candidates)]
    winners = [i for i in range(num_candidates) if math.isclose(result[i], 1.0)]
    winners = sorted(winners)

    return winners, stop-start


# THIS FUNCTION HAS NOT BEEN TESTED SINCE CONVERSION TO GUROBI
def solve_lp_bloc_owa(election, committee_size, owa):
    """This function generates a Gurobi model and solves it."""

    # Create a new model
    model = Model("bloc_owa")
    model.setParam('Threads', 1)

    # Objective function variables and coefficients
    x = {}
    pos = 0
    for i in range(election.num_voters):
        for j in range(committee_size):
            for k in range(election.num_candidates):
                x[i, j, k] = model.addVar(vtype=GRB.BINARY, name=f"x_{pos}")
                if k == committee_size - 1:
                    model.setObjective(model.getObjective() + owa[j] * x[i, j, k], GRB.MAXIMIZE)
                pos += 1

    # Add variables for candidates
    y = {}
    for i in range(election.num_candidates):
        y[i] = model.addVar(vtype=GRB.BINARY, name=f"y_{i}")

    model.update()

    # First group of constraints
    model.addConstr(sum(y[i] for i in range(election.num_candidates)) == committee_size, name="c0")

    # Second group of constraints
    for i in range(election.num_voters):
        for j in range(election.num_candidates):
            expr = sum(x[i, k, j] for k in range(committee_size)) \
                   - sum(y[int(election.votes[i][k])] for k in range(0, j + 1))
            model.addConstr(expr <= 0, name=f"c_{i}_{j}")

    # Solve the model
    model.setParam('OutputFlag', 0)
    start = model.Runtime
    model.optimize()
    stop = model.Runtime

    if model.status != GRB.OPTIMAL:
        print("Exception raised during solve")
        return None, stop-start

    # Extract winners
    result = [y[i].X for i in range(election.num_candidates)]
    winners = [i for i in range(election.num_candidates) if math.isclose(result[i], 1.0)]
    winners = sorted(winners[:committee_size])

    return winners, stop-start
