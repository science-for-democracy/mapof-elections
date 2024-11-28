.. _list_of_distances:


List of Distances
=================

List of Ordinal Distances
-------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - distance_id
     - implementation
   * - ``emd-postionwise``
     - :py:func:`~mapof.elections.distances.main_ordinal_distances.positionwise_distance`
   * - ``l1-postionwise``
     - :py:func:`~mapof.elections.distances.main_ordinal_distances.positionwise_distance`
   * - ``emd-bordawise``
     - :py:func:`~mapof.elections.distances.main_ordinal_distances.bordawise_distance`
   * - ``l1-pairwise``
     - :py:func:`~mapof.elections.distances.main_ordinal_distances.pairwise_distance`
    * - ``maximum_common_voter_subelection``
     - :py:func:`~mapof.elections.distances.ilp_subelections.maximum_common_voter_subelection`


List of Approval Distances
--------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - distance_id
     - implementation
   * - ``l1-approvalwise``
     - :py:func:`~mapof.elections.distances.main_approval_distances.approvalwise_distance`


