import queue
from queue import Queue

import numpy as np


# def get_all_leaves_names(node):
#     if node.leaf:
#         return [node.election_id]
#     output = []
#     for i in range(len(node.children)):
#         output.append(get_all_leaves_names(node.children[i]))
#     return list(chain.from_iterable(output))


# def get_all_leaves_nodes(node):
#     if node.leaf:
#         return [node]
#     output = []
#     for i in range(len(node.children)):
#         output.append(get_all_leaves_nodes(node.children[i]))
#     return list(chain.from_iterable(output))


def _get_all_nodes(root):
    all_nodes = []
    q = queue.Queue()
    q.put(root)
    while not q.empty():
        node = q.get()
        all_nodes.append(node)
        for child in node.children:
            q.put(child)
    return all_nodes


# def get_bracket_notation(node):
#     if node.leaf:
#         return str(node.election_id)
#     output = ''
#     for i in range(len(node.children)):
#         output += str(get_bracket_notation(node.children[i]))
#     return '(' + output + ')'


# def get_all_inner_nodes(node):
#     if node.leaf:
#         return []
#     output = [[node]]
#     for i in range(len(node.children)):
#         output.append(get_all_inner_nodes(node.children[i]))
#     return list(chain.from_iterable(output))


class Node:

    total_num_leaf_descendants = 0

    def __init__(self, election_id):

        self.election_id = election_id
        self.parent = None
        self.children = []
        self.leaf = True
        self.reverse = False

        self.left = 0
        self.right = 0

        self.num_leaf_descendants = None
        self.depth = None
        self.scheme = {}
        self.scheme_1 = {}
        self.scheme_2 = {}
        self.vector = []

    def __str__(self):
        return self.election_id

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        self.leaf = False


# def _generate_patterns(num_nodes, num_internal_nodes):
#     # Step 1: Mixing the patterns
#     patterns = ['M0' for _ in range(num_nodes-num_internal_nodes)] + \
#                ['M1' for _ in range(num_internal_nodes)]
#     np.random.shuffle(patterns)
#     return patterns


# def _generate_tree(num_nodes, num_internal_nodes, patterns):
#     """ Algorithm from: A linear-time embedding_id for the generation of trees """
#
#     sequence = []
#     sizes = []
#     larges = []
#     ctr = 0
#     inner_ctr = 0
#     for i, pattern in enumerate(patterns):
#         if pattern == 'M0':
#             sequence.append('x' + str(ctr))
#             sizes.append(1)
#             ctr += 1
#         elif pattern == 'M1':
#             sequence.append('v' + str(inner_ctr))
#             sequence.append('()1')   # instead of 'o'
#             sequence.append('f1')
#             sequence.append('f1')
#             sizes.append(4)
#             larges.append(i)
#             inner_ctr += 1
#
#     num_classical_edges = 0
#     num_semi_edges = 2*num_internal_nodes
#     num_multi_edges = num_internal_nodes
#     num_trees = 1
#     pos = 1
#     num_edges = num_nodes - num_trees - num_semi_edges - num_classical_edges
#
#     pos_to_insert = []
#     for i, elem in enumerate(sequence):
#         if elem == '()1':
#             pos_to_insert.append(i)
#
#     choices = list(np.random.choice([i for i in range(len(pos_to_insert))],
#                                     size=num_edges, replace=True))
#     choices.sort(reverse=True)
#
#     for choice in choices:
#         sizes[larges[choice]] += 1
#         sequence.insert(pos_to_insert[choice], 'f1')
#
#     for i in range(len(pos_to_insert)):
#         sequence.remove('()1')
#
#     return sequence, sizes


# def _turn_pattern_into_tree(pattern):
#     stack = []
#     for i, element in enumerate(pattern):
#         if 'x' in element or 'v' in element:
#             stack.append(Node(element))
#         if 'f' in element:
#             parent = stack.pop()
#             child = stack.pop()
#             parent.add_child(child)
#             stack.append(parent)
#     return stack[0]


# def cycle_lemma(sequence):
#
#     pos = 0
#     height = 0
#     min = 0
#     pos_min = 0
#     for element in sequence:
#         if 'x' in element or 'v' in element:
#             if height <= min:
#                 pos_min = pos
#                 min = height
#             height += 1
#         if 'f' in element:
#             height -= 1
#         pos += 1
#
#     # rotate
#     for _ in range(pos_min):
#         element = sequence.pop(0)
#         sequence.append(element)
#
#     return sequence


def _add_num_leaf_descendants(node):
    """ add total number of descendants to each internal node """

    if node.leaf:
        node.num_leaf_descendants = 1
    else:
        node.num_leaf_descendants = 0
        for child in node.children:
            node.num_leaf_descendants += _add_num_leaf_descendants(child)

    return node.num_leaf_descendants


# def _add_scheme(node):
#
#     for starting_pos in node.scheme_1:
#
#         pos = starting_pos
#         for child in node.children:
#             if pos in child.scheme_1:
#                 child.scheme_1[pos] += node.scheme_1[starting_pos]
#             else:
#                 child.scheme_1[pos] = node.scheme_1[starting_pos]
#             pos += child.num_leaf_descendants
#
#     for starting_pos in node.scheme_2:
#         pos = starting_pos
#         for child in node.children:
#             if pos in child.scheme_2:
#                 child.scheme_2[pos] += node.scheme_2[starting_pos]
#             else:
#                 child.scheme_2[pos] = node.scheme_2[starting_pos]
#             pos -= child.num_leaf_descendants
#
#     if node.leaf:
#         _construct_vector_from_scheme(node)
#     else:
#         for child in node.children:
#             _add_scheme(child)


def _construct_vector_from_scheme(node):

    x = node.scheme_1
    y = node.scheme_2
    node.scheme = {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}

    weight = 1. / sum(node.scheme.values())

    node.vector = [0 for _ in range(Node.total_num_leaf_descendants)]
    for key in node.scheme:

        node.vector[int(key)] += node.scheme[key] * weight

def _caterpillar(num_leaves):
    root = Node('root')
    tmp_root = root
    ctr = 1

    while num_leaves > 2:
        leaf = Node(ctr)
        ctr += 1
        inner_node = Node(ctr)
        ctr += 1
        tmp_root.add_child(leaf)
        tmp_root.add_child(inner_node)
        tmp_root = inner_node
        num_leaves -= 1

    leaf_1 = Node(ctr)
    ctr += 1
    leaf_2 = Node(ctr)
    tmp_root.add_child(leaf_1)
    tmp_root.add_child(leaf_2)

    return root



def _balanced(num_leaves):
    root = Node('root')
    ctr = 1

    q = Queue()
    q.put(root)

    while ctr < 2*num_leaves-1:
        tmp_root = q.get()
        for _ in range(2):
            inner_node = Node(ctr)
            ctr += 1
            tmp_root.add_child(inner_node)
            q.put(inner_node)

    return root


def get_gs_caterpillar_matrix(num_candidates):
    return get_gs_caterpillar_vectors(num_candidates).transpose()


def get_gs_caterpillar_vectors(num_candidates):
    return get_frequency_matrix_from_tree(_caterpillar(num_candidates))


def set_left_and_right(node):
    for i, child in enumerate(node.children):
        left = 0
        right = 0
        for j, other_child in enumerate(node.children):
            if j < i:
                left += other_child.num_leaf_descendants
            elif j > i:
                right += other_child.num_leaf_descendants
        child.left = left
        child.right = right

    for child in node.children:
        set_left_and_right(child)


def get_frequency_matrix_from_tree(root) -> np.ndarray:
    """
    Returns the frequency matrix of the tree rooted at root.

    Parameters
    ----------
        root : Node
            The root of the tree.

    Returns
    -------
        np.ndarray
            The frequency matrix of the tree.
    """
    _add_num_leaf_descendants(root)

    m = int(root.num_leaf_descendants)

    f = {}
    all_nodes = _get_all_nodes(root)
    for node in all_nodes:
        f[str(node.election_id)] = [0 for _ in range(m)]
    set_left_and_right(root)

    f[root.election_id][0] = 1

    for node in all_nodes:
        if node.election_id != root.election_id:
            for t in range(m):
                value_1 = 0
                if t-node.left >= 0:
                    value_1 = 0.5*f[node.parent.election_id][t - node.left]
                value_2 = 0
                if t-node.right >= 0:
                    value_2 = 0.5*f[node.parent.election_id][t - node.right]
                f[str(node.election_id)][t] = value_1 + value_2

    vectors = []
    for i in range(m):
        name = 'x' + str(i)
        vectors.append(f[name])
    return np.array(vectors)

