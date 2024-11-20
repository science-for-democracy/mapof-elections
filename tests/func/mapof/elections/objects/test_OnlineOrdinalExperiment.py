import pytest 

import mapof.elections as mapof

@pytest.fixture
def experiment():
    return mapof.prepare_online_ordinal_experiment()

@pytest.fixture
def two_fam_experiment(experiment):
    def add_families():
        """Helper method to add default families to the experiment."""
        experiment.add_family(
            culture_id='impartial',
            num_candidates=5,
            num_voters=10,
            size=10,
            color='green',
            marker='x',
            label='IC'
        )

        experiment.add_family(
            culture_id='norm_mallows',
            num_candidates=5,
            num_voters=10,
            size=10,
            params={'normphi': 0.5},
            color='blue',
            marker='o',
            label='Norm-Mallows'
        )
    add_families()
    return experiment

class TestOnlineOrdinalExperiment:

    def test_experiment_creation(self, experiment):
        assert experiment is not None, "Experiment should be created successfully"

    def test_adding_elections(self, experiment):
        experiment.add_election(
            culture_id='impartial',
            num_candidates=5,
            num_voters=50
        )
        experiment.add_election(
            culture_id='urn',
            num_candidates=5,
            num_voters=50,
            params={'alpha': 0.1},
        )
        assert experiment.num_elections == 2, "Two elections should be added"

    def test_adding_families(self, two_fam_experiment):
        assert len(two_fam_experiment.families) == 2, "Two families should be added"

    def test_computing_distances(self, two_fam_experiment):
        two_fam_experiment.compute_distances(distance_id='emd-positionwise')
        assert two_fam_experiment.distances is not None, "Distances should be computed"

    def test_embedding(self, two_fam_experiment):
        two_fam_experiment.compute_distances(distance_id='emd-positionwise')
        two_fam_experiment.embed_2d(embedding_id='fr')
        assert two_fam_experiment.coordinates is not None, "Embedding should be performed"

    def test_print_map(self, two_fam_experiment):
        two_fam_experiment.compute_distances(distance_id='emd-positionwise')
        two_fam_experiment.embed_2d(embedding_id='fr')
        two_fam_experiment.print_map_2d(show=False)

    def test_compute_feature(self, two_fam_experiment):
        two_fam_experiment.compute_distances(distance_id='emd-positionwise')
        two_fam_experiment.embed_2d(embedding_id='fr')

        feature_id = 'highest_borda_score'
        two_fam_experiment.compute_feature(feature_id=feature_id)
        assert len(two_fam_experiment.features) > 0, "Features should be computed"

    def test_print_map_colored_by_feature(self, two_fam_experiment):
        two_fam_experiment.compute_distances(distance_id='emd-positionwise')
        two_fam_experiment.embed_2d(embedding_id='fr')

        feature_id = 'highest_borda_score'
        two_fam_experiment.compute_feature(feature_id=feature_id)
        two_fam_experiment.print_map_2d_colored_by_feature(
            show=False,
            feature_id=feature_id
        )

    def test_compute_voting_rule(self, two_fam_experiment):

        for method in ['sntv', 'borda', 'stv']:
            two_fam_experiment.compute_voting_rule(method=method, committee_size=2)
