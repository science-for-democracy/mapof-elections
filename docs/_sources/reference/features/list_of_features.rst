.. _list_of_features:


List of Features
================

List of Ordinal Features
------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - feature_id
     - implementation
   * - ``highest_plurality_score``
     - :py:func:`~mapof.elections.features.scores.highest_plurality_score`
   * - ``highest_borda_score``
     - :py:func:`~mapof.elections.features.scores.highest_borda_score`
   * - ``highest_copeland_score``
     - :py:func:`~mapof.elections.features.scores.highest_copeland_score`
   * - ``lowest_dodgson_score``
     - :py:func:`~mapof.elections.features.scores.lowest_dodgson_score`
   * - ``borda_spread``
     - :py:func:`~mapof.elections.features.scores.borda_spread`
   * - ``highest_cc_score``
     - :py:func:`~mapof.elections.features.scores.highest_cc_score`
   * - ``highest_hb_score``
     - :py:func:`~mapof.elections.features.scores.highest_hb_score`
   * - ``highest_pav_score``
     - :py:func:`~mapof.elections.features.scores.highest_pav_score`


   * - ``Agreement``
     - :py:func:`~mapof.elections.features.diversity.agreement_index`
   * - ``Diversity``
     - :py:func:`~mapof.elections.features.diversity.diversity_index`
   * - ``Polarization``
     - :py:func:`~mapof.elections.features.diversity.polarization_index`
   * - ``AgreementApprox``
     - :py:func:`~mapof.elections.features.dap.agreement_index`
   * - ``DiversityApprox``
     - :py:func:`~mapof.elections.features.dap.diversity_index`
   * - ``PolarizationApprox``
     - :py:func:`~mapof.elections.features.dap.polarization_index`
   * - ``PolarizationApprox``
     - :py:func:`~mapof.elections.features.dap.borda_std`
   * - ``PolarizationApprox``
     - :py:func:`~mapof.elections.features.dap.avg_vote_dist`
   * - ``PolarizationApprox``
     - :py:func:`~mapof.elections.features.dap.max_vote_dist`
   * - ``PolarizationApprox``
     - :py:func:`~mapof.elections.features.dap.karpov_index`
   * - ``PolarizationApprox``
     - :py:func:`~mapof.elections.features.dap.avg_dist_to_kemeny`
   * - ``PolarizationApprox``
     - :py:func:`~mapof.elections.features.dap.avg_dist_to_borda`
   * - ``is_condorcet``
     - :py:func:`~mapof.elections.features.simple_ordinal.is_condorcet`
   * - ``effective_num_candidates``
     - :py:func:`~mapof.elections.features.simple_ordinal.get_effective_num_candidates`


List of Approval Features
-------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - feature_id
     - implementation
   * - ``max_approval_score``
     - :py:func:`~mapof.elections.features.simple_approval.max_approval_score`
   * - ``abstract``
     - :py:func:`~mapof.elections.features.simple_approval.abstract`
   * - ``justified_ratio``
     - :py:func:`~mapof.elections.features.simple_approval.justified_ratio`
   * - ``cohesiveness``
     - :py:func:`~mapof.elections.features.cohesive.count_largest_cohesiveness_level_l_of_cohesive_group`
   * - ``number_of_cohesive_groups``
     - :py:func:`~mapof.elections.features.cohesive.count_number_of_cohesive_groups`
   * - ``number_of_cohesive_groups_brute``
     - :py:func:`~mapof.elections.features.cohesive.count_number_of_cohesive_groups_brute`
   * - ``proportionality_degree_av``
     - :py:func:`~mapof.elections.features.proportionality_degree.proportionality_degree_av`
   * - ``proportionality_degree_pav``
     - :py:func:`~mapof.elections.features.proportionality_degree.proportionality_degree_pav`
   * - ``proportionality_degree_cc``
     - :py:func:`~mapof.elections.features.proportionality_degree.proportionality_degree_cc`

