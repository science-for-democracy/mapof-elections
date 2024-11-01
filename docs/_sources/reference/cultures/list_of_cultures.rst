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
     - (PrefSampling) Implementation
   * - ``ic`` ``impartial`` ``impartial_culture``
     - :py:func:`~prefsampling.approval.impartial.impartial`
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


List of Ordinal Cultures
------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - culture_id
     - Implementation
   * - ``id`` ``identity``
     - :py:func:`~prefsampling.ordinal.identity.identity`
   * - ``ic`` ``impartial`` ``impartial_culture``
     - :py:func:`~prefsampling.ordinal.impartial.impartial`
   * - ``iac``
     - :py:func:`~prefsampling.ordinal.impartial.impartial_anonymous`
   * - ``stratification``
     - :py:func:`~prefsampling.ordinal.impartial.impartial_anonymous`
   * - ``an`` ``antagonism``
     - :py:func:`~prefsampling.ordinal.compass.antagonism`
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
   * - ``euclidean``
     - :py:func:`~prefsampling.ordinal.groupseparable.group_separable`, :py:func:`~mapof.elections.cultures.prefsampling_mask.group_separable_mask`
   * - ``mallows``
     - :py:func:`~prefsampling.ordinal.mallows.mallows`
   * - ``norm-mallows``
     - :py:func:`~mapof.elections.cultures.mallows.generate_mallows_votes`



List of Pseudo Ordinal Cultures
------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - culture_id
     - Implementation

   * - ``pseudo_uniformity``
     - :py:func:`~mapof.elections.cultures.compass.pseudo_identity`
   * - ``pseudo_uniformity``
     - :py:func:`~mapof.elections.cultures.compass.pseudo_uniformity`
   * - ``pseudo_antagonism``
     - :py:func:`~mapof.elections.cultures.compass.pseudo_antagonism`
   * - ``pseudo_stratification``
     - :py:func:`~mapof.elections.cultures.compass.pseudo_stratification`
