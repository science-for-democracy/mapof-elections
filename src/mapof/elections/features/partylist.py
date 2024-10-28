import logging

from mapof.elections.features.register import register_ordinal_election_feature

try:
    import gurobipy as gb
except ImportError:
    logging.warning("Gurobi library not found. Some features may not work.")

try:
    from abcvoting import fileio
    from abcvoting.preferences import Profile, Voter
except ImportError:
    logging.warning("ABC Voting library not found. Some features may not work.")


def convert_election_to_profile(election):
    profile = Profile(num_cand=election.num_candidates)

    voters = []
    for i, vote in enumerate(election.votes):
        voter = Voter(vote)
        voters.append(voter)

    profile._voters = voters
    return profile


@register_ordinal_election_feature('partylist')
def partylistdistance(election, feature_params=None):

    if feature_params is None:
        feature_params = {}

    if 'largepartysize' in feature_params:
        largepartysize = feature_params['largepartysize']
    else:
        largepartysize = 2

    if 'time_limit' in feature_params:
        time_limit = feature_params['time_limit']
    else:
        time_limit = 10

    profile = convert_election_to_profile(election)

    model = gb.Model()
    model.setParam("OutputFlag", False)
    model.setParam('TimeLimit', time_limit)  # in seconds

    same_party = {}
    for c1 in profile.candidates:
        for c2 in range(c1):
            same_party[(c1, c2)] = model.addVar(vtype=gb.GRB.BINARY)

    edit = {}
    for v, _ in enumerate(profile):
        for c in profile.candidates:
            edit[(v, c)] = model.addVar(vtype=gb.GRB.BINARY)

    for v, vote in enumerate(profile):
        for c1 in profile.candidates:
            for c2 in range(c1):
                if c1 in vote.approved and c2 in vote.approved:
                    model.addConstr(
                        (same_party[(c1, c2)] == 1) >> (edit[(v, c1)] == edit[(v, c2)])
                    )
                    model.addConstr(
                        # (same_party[(c1, c2)] == 0) >> (edit[(v, c1)] + edit[(v, c2)] >= 1)
                        (same_party[(c1, c2)] + edit[(v, c1)] + edit[(v, c2)] >= 1)
                    )
                elif c1 not in vote.approved and c2 not in vote.approved:
                    model.addConstr(
                        (same_party[(c1, c2)] == 1) >> (edit[(v, c1)] == edit[(v, c2)])
                    )
                    model.addConstr(
                        # (same_party[(c1, c2)] == 0) >> (edit[(v, c1)] + edit[(v, c2)] <= 1)
                        (edit[(v, c1)] + edit[(v, c2)] <= 1 + same_party[(c1, c2)])
                    )
                else:
                    model.addConstr(
                        (same_party[(c1, c2)] == 1) >> (edit[(v, c1)] + edit[(v, c2)] == 1)
                    )
                    if c1 in vote.approved:
                        model.addConstr(
                            (same_party[(c1, c2)] + edit[(v, c1)] >= edit[(v, c2)])
                            # (same_party[(c1, c2)] == 0) >> (edit[(v, c1)] >= edit[(v, c2)])
                        )
                    else:
                        model.addConstr(
                            (same_party[(c1, c2)] + edit[(v, c2)] >= edit[(v, c1)])
                            # (same_party[(c1, c2)] == 0) >> (edit[(v, c2)] >= edit[(v, c1)])
                        )

    model.setObjective(
        gb.quicksum(edit[(v, c)] for v, _ in enumerate(profile) for c in profile.candidates),
        gb.GRB.MINIMIZE,
    )

    model.optimize()

    newprofile = Profile(num_cand=profile.num_cand)
    for v, vote in enumerate(profile):
        new_approved = {
            c
            for c in profile.candidates
            if (c in vote.approved and edit[(v, c)].X <= 0.1)
               or (c not in vote.approved and edit[(v, c)].X >= 0.9)
        }
        newprofile.add_voter(new_approved)

    parties = set(profile.candidates)
    for c1 in profile.candidates:
        for c2 in range(c1):
            if same_party[(c1, c2)].X >= 0.9:
                parties.discard(c2)
    num_large_parties = 0
    for party in parties:
        support = len([voter for voter in newprofile if party in voter.approved])
        if support >= largepartysize:
            num_large_parties += 1

    return model.objVal, model.objbound, num_large_parties

