import logging
import math

import numpy as np

from mapof.elections.distances import ilp_other as lp


def voting_rule(
        election,
        method=None,
        committee_size: int = None
) -> set:

    election.borda_points = get_borda_points(
        election.votes, election.num_voters, election.num_candidates)

    if method == 'sntv':
        winners = compute_sntv_voting_rule(election=election, committee_size=committee_size)
    elif method == 'borda':
        winners = compute_borda_voting_rule(election=election, committee_size=committee_size)
    elif method == 'stv':
        winners = compute_stv_voting_rule(election=election, committee_size=committee_size)
    else:
        logging.warning(f"Method {method} is not supported.")
        winners = set()

    return winners


def compute_standard_voting_rule(
        election=None,
        committee_size: int = 1,
        type=None,
        name=None
):
    rule = {'type_id': type,
            'name': name}
    winners = get_winners(election, committee_size, rule)
    return winners


def _randomize(
        vector,
        committee_size
):
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


def compute_sntv_voting_rule(
        election=None,
        committee_size: int = 1
):
    """ Compute SNTV winners for a given election """
    scores = [0 for _ in range(election.num_candidates)]
    for vote in election.votes:
        scores[vote[0]] += 1
    candidates = [i for i in range(election.num_candidates)]
    results = sorted(zip(scores, candidates), reverse=True)
    ranking = _randomize(results, committee_size)
    return ranking[0:committee_size]

#
def compute_borda_voting_rule(
        election=None,
        committee_size: int = 1
):
    """ Compute Borda winners for a given election """

    scores = [0 for _ in range(election.num_candidates)]
    for vote in election.votes:
        for i in range(election.num_candidates):
            scores[vote[i]] += election.num_candidates - i - 1
    candidates = [i for i in range(election.num_candidates)]
    results = sorted(zip(scores, candidates), reverse=True)
    ranking = _randomize(results, committee_size)
    return ranking[0:committee_size]


def compute_stv_voting_rule(
        election=None,
        committee_size: int = 1
):
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


def get_winners(election, committee_size, rule):
    return _get_ordinal_winners(election, committee_size, rule)


# Need update
def _get_ordinal_winners(election, committee_size, rule):
    if rule['type_id'] == 'scoring':
        scoring = _get_rule(rule['name'], election.num_candidates)
        winners = get_winners_scoring(election, committee_size, scoring)

    elif rule['type_id'] == 'borda_owa':
        owa = _get_rule(rule['name'], election.num_candidates)
        winners, total_time = _get_winners_borda_owa(election, committee_size, owa)

    elif rule['type_id'] == 'bloc_owa':
        owa = _get_rule(rule['name'], election.num_candidates)
        winners, total_time = _get_winners_bloc_owa(election, committee_size, owa)

    else:
        logging.warning('Unknown rule type')
        winners = None

    return winners


def _get_rule(name, length):
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


def get_winners_scoring(election, committee_size: int, scoring):

    points = [0 for _ in range(election.num_candidates)]
    candidates = [c for c in range(election.num_candidates)]

    for i in range(election.num_voters):
        for j in range(election.num_candidates):
            points[int(election.votes[i][j])] += scoring[j]

    tmp_candidates = [x for _, x in sorted(zip(points, candidates))]
    winners = tmp_candidates[election.num_candidates - committee_size: election.num_candidates]

    points = sorted(points)

    if committee_size > 1:
        breaking_point = election.num_candidates - committee_size
        if points[breaking_point-1] == points[breaking_point]:
            left = -1
            while points[breaking_point-1 + left] == points[breaking_point + left]:
                left -= 1
            right = 0

            while right < committee_size-2 \
                    and points[breaking_point+right] == points[breaking_point+right+1]:
                right += 1
            while right >= 0:
                r = np.random.randint(left,right)
                tmp_candidate = winners[right]
                winners[right] = tmp_candidates[breaking_point+r]
                tmp_candidates[breaking_point + r] = tmp_candidate
                right -= 1
    winners = sorted(winners)
    return winners


def _get_winners_borda_owa(*args):
    return lp.solve_lp_borda_owa(*args)


def _get_winners_bloc_owa(*args):
    return lp.solve_lp_bloc_owa(*args)
