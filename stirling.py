import operator
from collections.abc import Hashable, Iterable
from functools import reduce
from itertools import combinations, islice
from math import ceil, factorial

# TODO: Ensure that we work with non-orderable items. If we don't, we can do so by assigning
# an indexing to the elements (arbitrarily) and de-referencing those indexes after partitioning.


def stirling(elements: Iterable[Hashable], num_sets: int):
    """Generate the Stirling (second type) partitions for some elements.

    Args:
        elements (Iterable): The elements to partition.
        num_sets (int): The number of sets to partition into.

    Yields:
        tuple[tuple[Hashable]]: _description_
    """
    # All this really does is convert `elements` into a set and call the recursive solver.
    yield from _stirling(set(elements), num_sets)


def _stirling(elements: set, num_sets: int, max_group_size=None):
    num_elements = len(elements)
    
    # The largest group we deal with is the one that forces all other groups to be size 1.
    group_size = num_elements - (num_sets - 1)

    # But the caller may require that we only deal with groups up to a certain size.
    if max_group_size is not None:
        group_size = min(group_size, max_group_size)

    # The smallest group size is ceil(num-elements / num_sets).
    #
    # TODO: This almost works. We still have the problem where there are equal-sized groups in the partitioning, e.g.
    # 6-into-2. The lead group will end up duplicating things already produced by the recursive call. Memoization? Smarter
    # termination of the looping over combinations? Not sure yet. Take a look at limiting the looping (e.g. with islice) of
    # `combinations()` below.
    min_group_size = ceil(num_elements / num_sets)

    # At any level of recursion, we deal with all groups up to half the size of the total
    # input. Smaller groups are dealt with in recursive calls.
    while group_size >= min_group_size:
        assert group_size != 0

        # The lead group will be all combinations of the current group size
        for lead_group in islice(combinations(elements, group_size), stirling_count(num_elements, group_size)):
            # We use the remaining elements (i.e. those not in the lead group) in the recursion.
            remaining_elements = elements.difference(lead_group)

            # If there are remaining elements to be partitions, we recurse.
            if num_sets > 1:
                for tail_groups in _stirling(remaining_elements, num_sets - 1, group_size):
                    yield (lead_group, ) + tail_groups

            # Otherwise we're at the base case and terminate recursion.
            else:
                yield lead_group,

        group_size -= 1


def num_combinations(n, k):
    "Calculate the number of ways to choose k elements from n." 
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