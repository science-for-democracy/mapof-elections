import logging
import math

import numpy as np

from mapof.elections.distances import ilp_other as lp


def voting_rule(election, method=None, committee_size=None) -> set:

    election.borda_points = get_borda_points(
        election.votes, election.num_voters, election.num_candidates)

    if method == 'sntv':
        winners = compute_sntv_voting_rule(election=election, committee_size=committee_size)
    elif method == 'borda':
        winners = compute_borda_voting_rule(election=election, committee_size=committee_size)
    elif method == 'stv':
        winners = compute_stv_voting_rule(election=election, committee_size=committee_size)
    elif method in {'approx_cc', 'approx_hb', 'approx_pav'}:
        winners = compute_standard_voting_rule(election=election, committee_size=committee_size)
    else:
        logging.warning(f"Method {method} is not supported.")
        winners = set()

    return winners


def compute_standard_voting_rule(election=None, committee_size=1, ballot="ordinal", type=None, name=None):
    votes, num_voters, num_candidates = election.votes, election.num_voters, election.num_candidates
    params = {"orders": committee_size,
              "pure": True,
              "elections": 1,
              'candidates': num_candidates,
              'voters': num_voters}
    rule = {'type_id': type,
            'name': name,
            'length': num_candidates}
    winners, total_time = get_winners(params, votes, rule, ballot)
    return winners, total_time


def randomize(vector, committee_size):
    scores = [x for x, _ in vector]
    ranking = [x for _, x in vector]
    last_value = scores[committee_size-1]
    # LEFT
    left = committee_size - 2
    while left >= 0 and scores[left] == last_value:
        left -= 1
    left += 1
    # RIGHT
    right = committee_size
    while right < len(scores) and scores[right] == last_value:
        right += 1
    if left < right:
        ranking[left:right] = np.random.choice(ranking[left:right], right - left,
                                               replace=False)
    return ranking


def compute_sntv_voting_rule(election=None, committee_size=1):
    """ Compute SNTV winners for a given election """
    scores = [0 for _ in range(election.num_candidates)]
    for vote in election.votes:
        scores[vote[0]] += 1
    candidates = [i for i in range(election.num_candidates)]
    results = sorted(zip(scores, candidates), reverse=True)
    ranking = randomize(results, committee_size)
    return ranking[0:committee_size]


def compute_borda_voting_rule(election=None, committee_size=1):
    """ Compute Borda winners for a given election """

    scores = [0 for _ in range(election.num_candidates)]
    for vote in election.votes:
        for i in range(election.num_candidates):
            scores[vote[i]] += election.num_candidates - i - 1
    candidates = [i for i in range(election.num_candidates)]
    results = sorted(zip(scores, candidates), reverse=True)
    ranking = randomize(results, committee_size)
    return ranking[0:committee_size]


def compute_stv_voting_rule(election=None, committee_size=1):
    """ Compute STV winners for a given election """

    winners = []
    active = [True] * election.num_candidates

    droop_quota = math.floor(election.num_voters / (committee_size + 1.)) + 1

    votes_on_1 = [0.] * election.num_candidates
    for i in range(election.num_voters):
        votes_on_1[election.votes[i][0]] += 1

    v_power = [1.] * election.num_voters

    while len(winners) + sum(active) > committee_size:

        ctr = election.num_candidates
        winner_id = 0
        while ctr > 0:
            if active[winner_id] and votes_on_1[winner_id] >= droop_quota:

                winners += [winner_id]

                total = 0
                for i in range(election.num_voters):
                    for j in range(election.num_candidates):
                        if active[election.votes[i][j]]:
                            if election.votes[i][j] == winner_id:
                                for k in range(j + 1, election.num_candidates):
                                    if active[election.votes[i][k]]:
                                        v_power[i] *= float(votes_on_1[winner_id] - droop_quota) / \
                                                      float(votes_on_1[winner_id])
                                        votes_on_1[election.votes[i][k]] += 1. * v_power[i]
                                        total += 1. * v_power[i]
                                        ctr = election.num_candidates
                                        break
                            break
                votes_on_1[winner_id] = 0
                active[winner_id] = False

            ctr -= 1
            winner_id += 1
            winner_id %= election.num_candidates

        loser_votes = droop_quota
        loser_id = 0
        for i in range(election.num_candidates):
            if active[i] and votes_on_1[i] < loser_votes:
                loser_votes = votes_on_1[i]
                loser_id = i

        votes_on_1[loser_id] = 0
        for i in range(election.num_voters):
            for j in range(election.num_candidates):
                if active[election.votes[i][j]]:
                    if election.votes[i][j] == loser_id:
                        for k in range(j+1, election.num_candidates):
                            if active[election.votes[i][k]]:
                                votes_on_1[election.votes[i][k]] += 1. * v_power[i]
                                break
                    break
        active[loser_id] = False

    for i in range(election.num_candidates):
        if active[i]:
            winners += [i]

    winners = sorted(winners)

    return winners


def get_borda_points(votes, num_voters, num_candidates):
    points = np.zeros([num_candidates])
    scoring = [num_candidates - i - 1 for i in range(num_candidates)]

    for i in range(num_voters):
        for j in range(num_candidates):
            points[int(votes[i][j])] += scoring[j]

    return points


def get_winners(params, votes, rule, ballot='ordinal'):
    if ballot == "ordinal":
        return get_ordinal_winners(params, votes, rule)
    elif ballot == "approval":
        return get_approval_winners(params, votes, rule)


def get_approval_winners(params, elections, rule):
    if rule['type_id'] == 'app_cc':
        all_winners = []
        for i in range(params['elections']):
            winners = get_winners_app_cc(params, elections['votes'][i], elections['candidates'][i])
            all_winners += winners
        return all_winners


# Need update
def get_ordinal_winners(params, votes, rule):
    if rule['type_id'] == 'scoring':
        scoring = get_rule(rule['name'], rule['length'])
        all_winners = []
        for i in range(params['elections']):
            winners = get_winners_scoring(params, votes[i], params['candidates'], scoring)
            all_winners += winners
        return all_winners

    elif rule['type_id'] == 'borda_owa':
        owa = get_rule(rule['name'], rule['length'])
        all_winners = []
        for i in range(params['elections']):
            winners, total_time = get_winners_borda_owa(params, votes, owa)
            all_winners += winners
        # print(obj_vaue)
        return all_winners, total_time

    elif rule['type_id'] == 'bloc_owa':
        owa = get_rule(rule['name'], rule['length'])
        # t_bloc = rule['special']
        t_bloc = params["orders"]
        all_winners = []
        for i in range(params['elections']):
            winners, total_time = get_winners_bloc_owa(params, votes, owa, t_bloc)
            all_winners += winners
        # print(winners)
        return all_winners, total_time

    elif rule['type_id'] == 'election':
        all_winners = []
        for i in range(params['elections']):
            winners = []
            for j in range(params['voters']):
                winners += [votes[i][j]]

            all_winners += winners
        return all_winners
    #
    # elif rule['type_id'] == "approx_cc":
    #     all_winners = []
    #     winners = get_winners_approx_cc(votes, params)
    #     all_winners += winners
    #     return all_winners
    #
    # elif rule['type_id'] == "approx_hb":
    #     all_winners = []
    #     winners = get_winners_approx_hb(votes, params, 'greedy')
    #     all_winners += winners
    #     return all_winners
    #
    # elif rule['type_id'] == "approx_pav":
    #     all_winners = []
    #     winners = get_winners_approx_pav(votes, params, 'greedy')
    #     all_winners += winners
    #     return all_winners


def get_rule(name, length):

    rule = [0.] * length
    if name == "borda":
        for i in range(length):
            rule[i] = (length - float(i) - 1.) / (length - 1.)
    elif name == 'sntv':
        rule[0] = 1.
    elif name == 'cc':
        rule[0] = 1.
    elif name == 'hb':
        for i in range(length):
            rule[i] = 1. / (i + 1.)
    else:
        return name
    return rule


def get_winners_app_cc(params, votes, candidates):

    points = [0 for _ in range(params["candidates"])]

    for i in range(params['voters']):
        for j in range(len(votes[i])):
            points[int(votes[i][j])] += 1.

    tmp_candidates = [x for _, x in sorted(zip(points, candidates))]
    winners = tmp_candidates[params['candidates'] - params['orders']: params['candidates']]

    winners = sorted(winners)
    return winners


def get_winners_scoring(params, votes, candidates, scoring):

    points = [0 for _ in range(params["candidates"])]

    for i in range(params['voters']):
        for j in range(params['candidates']):
            points[int(votes[i][j])] += scoring[j]

    tmp_candidates = [x for _, x in sorted(zip(points, candidates))]
    winners = tmp_candidates[params['candidates'] - params['orders']: params['candidates']]

    points = sorted(points)
    ### DRAW ###
    if params['orders'] > 1:
        breaking_point = params['candidates'] - params['orders']
        if points[breaking_point-1] == points[breaking_point]:
            left = -1
            while points[breaking_point-1 + left] == points[breaking_point + left]:
                left -= 1
            right = 0

            while right < params['orders']-2 and points[breaking_point+right] == points[breaking_point+right+1]:
                right += 1
            while right >= 0:
                r = np.random.randint(left,right)
                tmp_candidate = winners[right]
                winners[right] = tmp_candidates[breaking_point+r]
                tmp_candidates[breaking_point + r] = tmp_candidate
                right -= 1
    winners = sorted(winners)
    return winners


def get_winners_borda_owa(params, votes, owa):
    return lp.solve_lp_borda_owa(params, votes, owa)


def get_winners_bloc_owa(params, votes, owa, t_bloc):
    return lp.solve_lp_bloc_owa(params, votes, owa, t_bloc)
