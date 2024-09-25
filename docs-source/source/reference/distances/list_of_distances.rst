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
     - :py:func:`~mapof.elections.distances.main_ordinal_distances.compute_positionwise_distance`
   * - ``l1-postionwise``
     - :py:func:`~mapof.elections.distances.main_ordinal_distances.compute_positionwise_distance`
   * - ``emd-bordawise``
     - :py:func:`~mapof.elections.distances.main_ordinal_distances.compute_bordawise_distance`
   * - ``l1-pairwise``
     - :py:func:`~mapof.elections.distances.main_ordinal_distances.compute_pairwise_distance`


List of Approval Distances
--------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - distance_id
     - implementation
   * - ``l1-approvalwise``
     - :py:func:`~mapof.elections.distances.main_approval_distances.compute_approvalwise_distance`


