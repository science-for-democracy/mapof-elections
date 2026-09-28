"""
Pipeline for experimenting with feature distances and maps they produce.

Currently set for Diversity, Agreement and Polarization features, but can be used for any features one might want.

"""

import os

import mapof.elections as mapof
from mapof.elections.features import dap_approx

EXPERIMENT_ID = 'dap_sample'

# Specify the features you wish to run the experiment with here
DAP = ['diversity_approx', 'agreement_approx', 'polarization_approx']


def dap_experiment():
    # make sure the correct folder with experiment is found
    #if you run this pipeline from a different location relative to your Mapof Installation and your experiment folder, you might need to tweak this
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Load offline experiment
    experiment = mapof.prepare_offline_ordinal_experiment(experiment_id=EXPERIMENT_ID)

    # Regenerate the elections from map.csv (overwrites the stored ones):
    # experiment.prepare_elections()
    # !!! do not run if you have your election instances already generated

    # Compute the approximate DAP features (stored in `features/<feature_id>.csv`)
    for feature_id in DAP:
        experiment.compute_feature(feature_id)

    # Alternatively load them from precomputed csv files instead of computing them:
    # for feature_id in DAP:
    #     experiment.features[feature_id] = experiment.import_feature(feature_id)

    # Compute the DAP distance ('feature_l1' gives the l1 variant, 'feature_l2' gives the l2 variant)
    experiment.compute_distances(distance_id='feature_l2', feature_ids=DAP)
    experiment.embed_2d(embedding_id='mds')
    experiment.print_map_2d(legend=True, saveas='dap_sample_mds', show=False)

    # Compute correlation with some other distance if it interests you, comment out otherwise (here I compute the correlation with positionwise distance)
    experiment.compute_distances(distance_id='emd-positionwise')
    print("Test correlation between: feature_l2 (DAP) and emd-positionwise: \n")
    experiment.print_correlation_between_distances(distance_id_1='emd-positionwise',
                                                   distance_id_2='feature_l2')


    # If you wrote a function computing a feature yourself and wish to add it manually, do the following:

    # This adds features under custom names, e.g. d, a, p in this case
    # experiment.add_feature('d', dap_approx.diversity_index)
    # experiment.add_feature('a', dap_approx.agreement_index)
    # experiment.add_feature('p', dap_approx.polarization_index)
    # for feature_id in ['d', 'a', 'p']:
    #     experiment.compute_feature(feature_id)

    # Alternatively if you want to load features from csv files under custom names:
    # experiment.features['d'] = experiment.import_feature('diversity_approx')
    # experiment.features['a'] = experiment.import_feature('agreement_approx')
    # experiment.features['p'] = experiment.import_feature('polarization_approx')

    # Then you can compute the feature distance as before
    # experiment.compute_distances(distance_id='feature_l1', feature_ids=['d', 'a', 'p'])

if __name__ == "__main__":
    dap_experiment()