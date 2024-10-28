
registered_ordinal_election_features = {}

registered_approval_election_features = {}


def register_ordinal_election_feature(feature_id: str):

    def decorator(func):
        registered_ordinal_election_features[feature_id] = func
        return func

    return decorator


def register_approval_election_feature(feature_id: str):

    def decorator(func):
        registered_approval_election_features[feature_id] = func
        return func

    return decorator
