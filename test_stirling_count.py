import pytest

from stirling import stirling_count

# each row is an 'n', and each colums in the 'n' is a 'k'. Taken from https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind
# yapf: disable
RAW = [
 [1],
  [0,  1],
  [0,  1,  1],
  [0,  1,  3,  1],
  [0,  1,  7,  6,  1],
  [0,  1,  15,  25,  10,  1],
  [0,  1,  31,  90,  65,  15,  1,],
  [0,  1,  63,  301,  350,  140,  21,  1,],
  [0,  1,  127,  966,  1701,  1050,  266,  28,  1],
  [0,  1,  255,  3025,  7770,  6951,  2646,  462,  36,  1],
  [0,  1,  511,  9330,  34105,  42525,  22827,  5880,  750,  45,  1 ],
]
# yapf: enable

VALUES = [(n_index, k_index, value) for n_index, n_row in enumerate(RAW)
          for k_index, value in enumerate(n_row)]


@pytest.fixture(params=VALUES)
def canned(request):
    return request.param


def test_stirling_count(canned):
    n, k, expected = canned
    actual = stirling_count(n, k)
    assert actual == expected