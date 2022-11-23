import operator
from collections.abc import Iterable
from functools import reduce
from itertools import combinations
from math import factorial


def stirling(elements: Iterable, num_sets: int):
    yield from _stirling(set(elements), num_sets)


def _stirling(elements: set, num_sets: int):
    num_elements = len(elements)
    group_size = num_elements - (num_sets - 1)

    while group_size >= num_elements / 2:
        assert group_size != 0
        for lead_group in combinations(elements, group_size):
            remaining_elements = elements.difference(lead_group)
            if num_sets > 1:
                for tail_groups in _stirling(remaining_elements, num_sets - 1):
                    yield (lead_group, ) + tail_groups
            else:
                yield lead_group,
        group_size -= 1


def num_combinations(n, k):
    "Calculate n choose k"
    return factorial(n) / (factorial(k) * factorial(n - k))


def stirling_count(n, k):
    """Calculate the number of stirling second type partitions of n elements into k sets
    
    Based on formula at https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind
    """

    # These are hacks. The math below breaks down a bit for some numbers due to floating point stuff. These
    # checks work around that.
    if n == k:
        return 1

    if k == 0:
        return 0

    components = [
        pow(-1, i) * num_combinations(k, i) * pow((k - i), n)
        for i in range(k + 1)
    ]
    sum = reduce(operator.add, components)
    return int((1 / factorial(k)) * sum)