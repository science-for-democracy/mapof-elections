import logging

from mapof.elections.features.register import register_approval_election_feature

try:
    from abcvoting.preferences import Profile
    from abcvoting import abcrules, properties
    from abcvoting.output import output, INFO
except ImportError:
    pass


@register_approval_election_feature("ejr", has_params=True, is_rule_related=True)
def test_ejr(election, feature_params):
    logging.warning("Computing EJR needs update. Do not use this function.")

    rule = feature_params["rule"]

    profile = Profile(election.num_candidates)
    profile.add_voters(election.votes)
    committee = election.winning_committee[rule]

    return properties.full_analysis(profile, committee)
