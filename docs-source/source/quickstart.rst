.. _quickstart:

Quick Start
===========

Import
------

To import mapof-elections python package:

.. code-block:: python

    import mapof.elections as mapof



General Tasks
-------------

.. _generate_ordinal_election:

Generate Ordinal Election from Statistical Culture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this section, you will learn how to generate ordinal elections from different statistical cultures. We will start by defining what we mean by an election.

Formally, an ordinal election is a pair :math:`E=(C,V)` that consists of a set of candidates :math:`C` and a collection of voters :math:`V`, where each voter has a strict preference order (vote), that is, each voter ranks all the candidates in :math:`C` from the most to the least desirable one. We use terms voter and vote interchangeably. In practice, an ``OrdinalElection`` is an abstract object that, among other fields, contains:

.. code-block:: python

    election.num_candidates     # number of candidates
    election.num_voters         # number of voters
    election.votes              # preference orders

By ``votes``, we refer to a two-dimensional array, where each row represents a single vote.

.. _example_oridnal_election:

.. rubric:: Example

E.g., ``votes = [[0,1,2,3],[2,0,3,1],[3,1,2,0]]`` refers to an election with three following votes:

::

    0 ≻ 1 ≻ 2 ≻ 3
    2 ≻ 0 ≻ 3 ≻ 1
    3 ≻ 1 ≻ 2 ≻ 0


**Objective:**
Generate impartial culture election with 5 candidates and 50 voters.

**Solution:**
To generate an election we use the ``generate_ordinal_election()`` function:

.. code-block:: python

    election = mapof.generate_ordinal_election(
                                        culture_id='ic',
                                        num_candidates=5,
                                        num_voters=50)




.. _generate_approval_election:

Generate Approval Election from Statistical Culture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. role:: python(code)
   :language: python


In this section, you will learn how to generate approval elections from different statistical cultures. We will start by defining what we mean by an election.

Formally, an approval election is a pair :math:`E=(C,V)` that consists of a set of candidates :math:`C` and a collection of voters :math:`V`, where each voter approves a certain subset of candidates. In practice, an ``ApprovalElection`` is an abstract object that, among others, contains the following fields:

.. code-block:: python

   election.num_candidates     # number of candidates
   election.num_voters         # number of voters
   election.votes              # list of sets

By ``votes``, we refer to a list of sets, where each set represents a single vote.

.. _example_approval_election:

.. rubric:: Example

For example, ``votes = [{0,1},{1,2,3},{2}]`` refers to an election with three following votes:

.. centered::
   :math:`{0, 1}`,
   :math:`{1, 2, 3}`,
   :math:`{2}`.


**Objective:**
Generate impartial culture election with 20 candidates and 100 voters


**Solution:**
To generate an election, we use the ``generate_approval_election()`` function:

.. code-block:: python

   election = mapof.generate_approval_election(
                                      culture_id='ic',
                                      num_candidates=20,
                                      num_voters=100)

Generate Ordinal Election from Votes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of using a statistical culture, you can also generate elections based on your own votes using the :python:`generate_ordinal_election_from_votes` function.

.. code-block:: python

   votes = [[0, 1, 2, 3], [2, 0, 3, 1], [3, 1, 2, 0]]
   election = mapof.generate_ordinal_election_from_votes(votes)

Generate Approval Election from Votes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of using a statistical culture, you can also generate elections based on your own votes using the :python:`generate_approval_election_from_votes` function.

.. code-block:: python

   votes = [{0, 1}, {1, 2, 3}, {2}]
   election = mapof.generate_approval_election_from_votes(votes)


Compute Borda Score
~~~~~~~~~~~~~~~~~~~
**Objective:**
Implement a function that, for a given ordinal election, returns Borda scores of all candidates.

First, we need to create a ``scores`` list and fill it with zeros.

.. code-block:: python

   scores = [0 for _ in range(election.num_candidates)]

Second, we need to iterate through all the votes and add appropriate points to candidates.

.. code-block:: python

   for vote in election.votes:
       for c in range(election.num_candidates):
           scores[vote[c]] += election.num_candidates - 1 - c



**Solution:**
The complete function looks as follows:

.. code-block:: python

   def compute_borda_scores(election) -> list:
       """ Returns list with all Borda scores """
       scores = [0 for _ in range(election.num_candidates)]
       for vote in election.votes:
           for c in range(election.num_candidates):
               scores[vote[c]] += election.num_candidates - 1 - c
       return scores

Compute Distance between Two Elections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Objective:**
Compute the EMD-Positionwise distance between two ordinal elections.

To compute a distance, use the ``compute_distance`` function, which takes two elections and a ``distance_id`` as input.

.. code-block:: python

   distances, mapping = mapof.compute_distance(
                                       election_1,
                                       election_2,
                                       distance_id='emd-positionwise')

This function returns a tuple containing the distance and the mapping that witnesses this distance. If a given distance does not use a mapping, it returns ``None`` instead.

**Solution:**
We start by generating two elections, and then we compute the distance:

.. code-block:: python

   election_1 = mapof.generate_ordinal_election(
                                           culture_id='ic',
                                           num_voters=5,
                                           num_candidates=3)
   election_2 = mapof.generate_ordinal_election(
                                           culture_id='ic',
                                           num_voters=5,
                                           num_candidates=3)
   distance, mapping = mapof.compute_distance(
                                           election_1,
                                           election_2,
                                           distance_id='emd-positionwise')

