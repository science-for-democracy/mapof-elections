
import mapof.elections as mapof


class TestOnlineOrdinalExperiment:

    def test_experiment_creation(self):
        experiment = mapof.prepare_online_ordinal_experiment()

    def test_adding_families(self):
        experiment = mapof.prepare_online_ordinal_experiment()
        experiment.add_family(culture_id='ic', size=10,
                              color='green', marker='x', label='IC')
        experiment.add_family(culture_id='norm-mallows', size=10,
                              normphi=0.5,
                              color='blue', marker='o',
                              label='Norm-Mallows')

    def test_computing_distances(self):
        experiment = mapof.prepare_online_ordinal_experiment()
        experiment.add_family(culture_id='ic', size=10,
                              color='green', marker='x', label='IC')
        experiment.add_family(culture_id='norm-mallows', size=10,
                              normphi=0.5,
                              color='blue', marker='o',
                              label='Norm-Mallows')
        experiment.compute_distances(distance_id='emd-positionwise')

    def test_embedding(self):
        experiment = mapof.prepare_online_ordinal_experiment()
        experiment.add_family(culture_id='ic', size=10,
                              color='green', marker='x', label='IC')
        experiment.add_family(culture_id='norm-mallows', size=10,
                              normphi=0.5,
                              color='blue', marker='o',
                              label='Norm-Mallows')
        experiment.compute_distances(distance_id='emd-positionwise')
        experiment.embed_2d(embedding_id='fr')

    def test_print_map(self):
        experiment = mapof.prepare_online_ordinal_experiment()
        experiment.add_family(culture_id='ic', size=10,
                              color='green', marker='x', label='IC')
        experiment.add_family(culture_id='norm-mallows', size=10,
                              normphi=0.5,
                              color='blue', marker='o',
                              label='Norm-Mallows')
        experiment.compute_distances(distance_id='emd-positionwise')
        experiment.embed_2d(embedding_id='fr')
        experiment.print_map_2d(show=False)




