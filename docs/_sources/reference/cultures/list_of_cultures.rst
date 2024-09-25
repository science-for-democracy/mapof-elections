.. _list_of_cultures:


List of Cultures
=================

List of Ordinal Cultures
------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - culture_id
     - PrefSampling implementation
   * - ``id`` ``identity``
     - :py:func:`~prefsampling.ordinal.identity.identity`
   * - ``ic`` ``impartial`` ``impartial_culture``
     - :py:func:`~prefsampling.ordinal.impartial.impartial`
   * - ``iac``
     - :py:func:`~prefsampling.ordinal.impartial.impartial_anonymous`
   * - ``stratification``
     - :py:func:`~prefsampling.ordinal.impartial.stratification`
   * - ``urn``
     - :py:func:`~prefsampling.ordinal.urn.urn`
   * - ``didi``
     - :py:func:`~prefsampling.ordinal.didi.didi`
   * - ``plackett-luce``
     - :py:func:`~prefsampling.ordinal.plackettluce.plackett_luce`
   * - ``conitzer``
     - :py:func:`~prefsampling.ordinal.singlepeaked.single_peaked_conitzer`
   * - ``walsh``
     - :py:func:`~prefsampling.ordinal.singlepeaked.single_peaked_walsh`
   * - ``spoc``
     - :py:func:`~prefsampling.ordinal.singlepeaked.single_peaked_circle`
   * - ``plackett-luce``
     - :py:func:`~prefsampling.ordinal.plackettluce.plackett_luce`


List of Approval Cultures
-------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - culture_id
     - PrefSampling implementation
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
