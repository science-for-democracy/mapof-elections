registered_ordinal_election_features = {}

registered_approval_election_features = {}

features_with_params = {}

features_rule_related = {}


def register_ordinal_election_feature(feature_id: str):

    def decorator(func):
        registered_ordinal_election_features[feature_id] = func
        return func

    return decorator


def register_approval_election_feature(feature_id: str, has_params=False, is_rule_related=False):

    def decorator(func):
        registered_approval_election_features[feature_id] = func
        if has_params:
            features_with_params[feature_id] = func
        if is_rule_related:
            features_rule_related[feature_id] = func
        return func

    return decorator


