from stirling import stirling
from itertools import chain
import hypothesis.strategies as ST
from hypothesis import given


def test_1_element_1_group():
    elements = [1]
    actual = tuple(stirling(elements, num_sets=1))
    # yapf: disable
    expected = (
        ((1, ), ),
    )
    # yapf: enable
    assert actual == expected


def test_2_elements_1_group():
    elements = [0, 1]
    actual = tuple(stirling(elements, num_sets=1))
    # yapf: disable
    expected = (
        ((0, 1), ),
    )
    # yapf: enable
    assert actual == expected


def test_2_elements_2_group():
    elements = [0, 1]
    actual = tuple(stirling(elements, num_sets=2))
    # yapf: disable
    expected = (
        ((0,), (1,) ),
    )
    # yapf: enable
    assert actual == expected


def test_six_choose_three():
    elements = [1, 2, 3, 4, 5, 6]
    expected_count = 90
    actual = tuple(stirling(elements, num_sets=3))
    actual_count = len(actual)
    assert actual_count == expected_count


@ST.composite
def elements_and_num_partitions(draw, elements=ST.integers()):
    values = draw(
        ST.sets(elements, min_size=1, max_size=10)
    )  # This max_size is important because if it's too large things can take a loooong time
    num_groups = draw(ST.integers(min_value=1, max_value=len(values)))
    return (values, num_groups)


@given(elements_and_num_partitions())
def test_correct_number_of_groups(params):
    elements, num_partitions = params
    for partioning in tuple(stirling(elements, num_partitions)):
        assert len(partioning) == num_partitions


@given(elements_and_num_partitions())
def test_all_elements_present_in_partitioning(params):
    elements, num_partitions = params
    for partitioning in stirling(elements, num_partitions):
        partitioned_elements = tuple(chain(*partitioning))
        assert len(partitioned_elements) == len(elements)
        assert set(partitioned_elements) == elements
