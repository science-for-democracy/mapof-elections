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
   * - ``Agreement``
     - :py:func:`~mapof.elections.features.diversity.agreement_index`
   * - ``Diversity``
     - :py:func:`~mapof.elections.features.diversity.diversity_index`
   * - ``Polarization``
     - :py:func:`~mapof.elections.features.diversity.polarization_index`
   * - ``AgreementApprox``
     - :py:func:`~mapof.elections.features.dap_approximate.agreement_index`
   * - ``DiversityApprox``
     - :py:func:`~mapof.elections.features.dap_approximate.diversity_index`
   * - ``PolarizationApprox``
     - :py:func:`~mapof.elections.features.dap_approximate.polarization_index`
   * - ``is_condorcet``
     - :py:func:`~mapof.elections.features.simple_ordinal.is_condorcet`



List of Approval Features
------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - feature_id
     - implementation
   * - ``max_approval_score``
     - :py:func:`~mapof.elections.features.simple_approval.max_approval_score`

