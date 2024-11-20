import prefsampling.approval as pref_approval
import prefsampling.ordinal as pref_ordinal

# Some cultures are added via decorators
registered_approval_election_cultures = {
    'resampling': pref_approval.resampling,
    'disjoint_resampling': pref_approval.disjoint_resampling,
    'moving_resampling': pref_approval.moving_resampling,
    'noise': pref_approval.noise,
    'full': pref_approval.full,
    'empty': pref_approval.empty,
    'urn_partylist': pref_approval.urn_partylist,

    'approval_full': pref_approval.full,  # deprecated name
    'approval_empty': pref_approval.empty,  # deprecated name

    # 'truncated_mallows': mallows.generate_approval_truncated_mallows_votes,  # unsupported culture
}

# Some cultures are added via decorators
registered_ordinal_election_cultures = {
    'identity': pref_ordinal.identity,
    'impartial': pref_ordinal.impartial,
    'impartial_culture': pref_ordinal.impartial,
    'iac': pref_ordinal.impartial_anonymous,
    'didi': pref_ordinal.didi,
    'plackett_luce': pref_ordinal.plackett_luce,
    'urn': pref_ordinal.urn,
    'single_crossing': pref_ordinal.single_crossing,
    'single_peaked_conitzer': pref_ordinal.single_peaked_conitzer,
    'single_peaked_walsh': pref_ordinal.single_peaked_walsh,
    'spoc': pref_ordinal.single_peaked_circle,
    'mallows': pref_ordinal.mallows,

    'id': pref_ordinal.identity,  # deprecated name
    'ic': pref_ordinal.impartial,  # deprecated name
}

# Some cultures are added via decorators
registered_pseudo_ordinal_cultures = {
}

# Some cultures are added via decorators
registered_alliance_ordinal_cultures = {
}


def register_approval_election_culture(feature_id: str):

    def decorator(func):
        registered_approval_election_cultures[feature_id] = func
        return func

    return decorator


def register_ordinal_election_culture(feature_id: str):

    def decorator(func):
        registered_ordinal_election_cultures[feature_id] = func
        return func

    return decorator


def register_pseudo_ordinal_culture(feature_id: str):

    def decorator(func):
        registered_pseudo_ordinal_cultures[feature_id] = func
        return func

    return decorator


def register_alliance_ordinal_culture(feature_id: str):

    def decorator(func):
        registered_alliance_ordinal_cultures[feature_id] = func
        return func

    return decorator

