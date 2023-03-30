import pytest

from ai import check_squirrely_behavior


@pytest.mark.parametrize(
    "buffer, expected",
    [
        ("   ", False),
        ("###", True),
        ("# #", True),
        ("  #", False),
        ("\n##", True),
    ],
)
def test_check_squirrely_behavior(buffer: str, expected: bool):
    assert expected == check_squirrely_behavior(buffer.encode())
