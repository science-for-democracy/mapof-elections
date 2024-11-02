.. _list_of_cultures:


List of Cultures
=================

Note that many of the cultures are implemented in the :py:mod:`prefsampling` Python package.

List of Approval Cultures
-------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - culture_id
     - Implementation
   * - ``impartial``
     - :py:func:`~prefsampling.approval.impartial.impartial`
   * - ``identity``
     - :py:func:`~prefsampling.approval.identity.identity`, :py:func:`~mapof.elections.cultures.prefsampling_mask.identity_mask`
   * - ``empty``
     - :py:func:`~prefsampling.approval.identity.empty`
   * - ``full``
     - :py:func:`~prefsampling.approval.identity.full`
   * - ``resampling``
     - :py:func:`~prefsampling.approval.resampling.resampling`
   * - ``disjoint_resampling``
     - :py:func:`~prefsampling.approval.resampling.disjoint_resampling`
   * - ``moving_resampling``
     - :py:func:`~prefsampling.approval.resampling.moving_resampling`
   * - ``noise``
     - :py:func:`~prefsampling.approval.noise.noise`
   * - ``urn_partylist``
     - :py:func:`~prefsampling.approval.urn.urn_partylist`
   * - ``truncated_urn``
     - :py:func:`~prefsampling.approval.truncated_ordinal.truncated_ordinal`, :py:func:`~mapof.elections.cultures.prefsampling_mask.truncated_urn_mask`
   * - ``euclidean``
     - :py:func:`~prefsampling.approval.euclidean.euclidean_vcr`, :py:func:`~mapof.elections.cultures.prefsampling_mask.euclidean_approval_mask`


List of Ordinal Cultures
------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - culture_id
     - Implementation
   * - ``identity``
     - :py:func:`~prefsampling.ordinal.identity.identity`
   * -  ``impartial``
     - :py:func:`~prefsampling.ordinal.impartial.impartial`
   * - ``iac``
     - :py:func:`~prefsampling.ordinal.impartial.impartial_anonymous`
   * - ``stratification``
     - :py:func:`~prefsampling.ordinal.impartial.impartial_anonymous`
   * - ``antagonism``
     - :py:func:`~prefsampling.ordinal.compass.generate_antagonism_votes`
   * - ``urn``
     - :py:func:`~prefsampling.ordinal.urn.urn`
   * - ``didi``
     - :py:func:`~prefsampling.ordinal.didi.didi`
   * - ``plackett-luce``
     - :py:func:`~prefsampling.ordinal.plackettluce.plackett_luce`
   * - ``walsh``
     - :py:func:`~prefsampling.ordinal.singlepeaked.single_peaked_walsh`
   * - ``conitzer``
     - :py:func:`~prefsampling.ordinal.singlepeaked.single_peaked_conitzer`
   * - ``spoc``
     - :py:func:`~prefsampling.ordinal.singlepeaked.single_peaked_circle`
   * - ``spoc``
     - :py:func:`~prefsampling.ordinal.singlecrossing.single_crossing`
   * - ``approx_uniformity``
     - :py:func:`~mapof.elections.cultures.compass.generate_approx_uniformity_votes`
   * - ``approx_stratification``
     - :py:func:`~mapof.elections.cultures.compass.generate_approx_stratification_votes`
   * - ``euclidean``
     - :py:func:`~prefsampling.ordinal.euclidean.euclidean`, :py:func:`~mapof.elections.cultures.prefsampling_mask.euclidean_ordinal_mask`
   * - ``group-separable``
     - :py:func:`~prefsampling.ordinal.groupseparable.group_separable`, :py:func:`~mapof.elections.cultures.prefsampling_mask.group_separable_mask`
   * - ``mallows``
     - :py:func:`~prefsampling.ordinal.mallows.mallows`
   * - ``norm-mallows``
     - :py:func:`~prefsampling.ordinal.mallows.norm_mallows`, :py:func:`~mapof.elections.cultures.prefsampling_mask.norm_mallows_mask`



List of Pseudo Ordinal Cultures
-------------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - culture_id
     - Implementation

   * - ``pseudo_uniformity``
     - :py:func:`~mapof.elections.cultures.pseudo_cultures.pseudo_identity`
   * - ``pseudo_uniformity``
     - :py:func:`~mapof.elections.cultures.pseudo_cultures.pseudo_uniformity`
   * - ``pseudo_antagonism``
     - :py:func:`~mapof.elections.cultures.pseudo_cultures.pseudo_antagonism`
   * - ``pseudo_stratification``
     - :py:func:`~mapof.elections.cultures.pseudo_cultures.pseudo_stratification`
   * - ``pseudo_unid``
     - :py:func:`~mapof.elections.cultures.pseudo_cultures.pseudo_unid`
   * - ``pseudo_anid``
     - :py:func:`~mapof.elections.cultures.pseudo_cultures.pseudo_anid`
   * - ``pseudo_stid``
     - :py:func:`~mapof.elections.cultures.pseudo_cultures.pseudo_unid`
   * - ``pseudo_unid``
     - :py:func:`~mapof.elections.cultures.pseudo_cultures.pseudo_anun`
   * - ``pseudo_stun``
     - :py:func:`~mapof.elections.cultures.pseudo_cultures.pseudo_stun`
   * - ``pseudo_stan``
     - :py:func:`~mapof.elections.cultures.pseudo_cultures.pseudo_unid`
   * - ``pseudo_sp_conitzer``
     - :py:func:`~mapof.elections.cultures.sp_matrices.get_conitzer_matrix`
   * - ``pseudo_sp_walsh``
     - :py:func:`~mapof.elections.cultures.sp_matrices.get_walsh_matrix`
   * - ``pseudo_single-crossing``
     - :py:func:`~mapof.elections.cultures.sc_matrices.get_single_crossing_matrix`
