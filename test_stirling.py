from stirling import stirling


def test_1_choose_1():
    elements = [1]
    actual = tuple(stirling(elements, num_sets=1))
    # yapf: disable
    expected = (
        ((1, ), ),
    )
    # yapf: enable
    assert actual == expected


def test_six_choose_three():
    elements = [1, 2, 3, 4, 5, 6]
    expected_count = 90
    actual = tuple(stirling(elements, num_sets=3))
    actual_count = len(actual)
    assert actual_count == expected_count