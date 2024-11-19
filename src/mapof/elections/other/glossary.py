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
    if culture_id is not None and (culture_id in ORDINAL_PSEUDO_MODELS or 'pseudo' in culture_id):
        return True
    return False
