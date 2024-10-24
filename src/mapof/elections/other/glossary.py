ELECTION_GLOBAL_FEATURES = {
    'clustering',
    'clustering_kmeans',
    'distortion_from_all',
    'id_vs_un',
    'an_vs_st'
}

NOT_ABCVOTING_RULES = {'borda_c4', 'random'}

APPROVAL_FAKE_MODELS = {'approval_half_1', 'approval_half_2', 'approval_skeleton'}

APPROVAL_MODELS = {
    'impartial_culture',
    'ic',
    'resampling',
    'id',
    'empty',
    'full',
    'truncated_urn',
    'urn',
    'euclidean',
    'noise',
    'zeros',
    'ones',
    'id_0.5',
    'ic_0.5',
    'half_1',
    'half_2',
    'disjoint_resampling',
    'simplex_resampling',
    'vcr',
    'truncated_mallows',
    'moving_resampling',
    'jaccard',
    'skeleton',
    'anti_pjr',
    'partylist'
}

ORDINAL_PSEUDO_MODELS = {
    'pseudo_uniformity',
    'pseudo_stratification',
    'pseudo_identity',
    'pseudo_antagonism',
    'pseudo_unid',
    'pseudo_anid',
    'pseudo_stid',
    'pseudo_anun',
    'pseudo_stun',
    'pseudo_stan',

    'mallows_matrix_path',
    'walsh_matrix',
    'conitzer_matrix',
    'single-crossing_matrix',
    'gs_caterpillar_matrix',
    'norm-mallows_matrix',
    'sushi_matrix',
    'walsh_path',
    'conitzer_path',
    'from_approval',
    'from_matrix',
    "frequency_matrix",
}

PATHS = {
    'pseudo_unid',
    'pseudo_stan',
    'pseudo_anid',
    'pseudo_stid',
    'pseudo_anun',
    'pseudo_stun',

    'mallows_matrix_path',
    'walsh_path',
    'conitzer_path'
}

LIST_OF_PREFLIB_MODELS = {
    'sushi',
    'irish',
    'glasgow',
    'skate',
    'formula',
    'tshirt',
    'cities_survey',
    'aspen',
    'ers',
    'marble',
    'cycling_tdf',
    'cycling_gdi',
    'ice_races',
    'grenoble',
    'speed_skating',
    'irish_bis',
    'speed_skating_bis',
    'skate_bis'
}


def is_pseudo_culture(culture_id: str) -> bool:
    if culture_id is None or \
            culture_id in ORDINAL_PSEUDO_MODELS or \
            'pseudo' in culture_id:
        return True
    return False
