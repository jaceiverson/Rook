import pytest

from rook import Card


def test_good_creation():
    card = Card("black", 1, 15, 15)
    assert card.suit == "black"
    assert card.number == 1
    assert card.pvalue == 15
    assert card.tvalue == 15
    assert card.trump == False


# write tests to test each parameter of the class looking for the value error
def test_bad_creation_suit():
    with pytest.raises(ValueError):
        card = Card("blue", 1, 15, 15)


def test_bad_creation_number():
    with pytest.raises(ValueError):
        card = Card("black", 0, 15, 15)


def test_bad_creation_pvalue():
    with pytest.raises(ValueError):
        card = Card("black", 1, 25, 15)


def test_bad_creation_tvalue():
    with pytest.raises(ValueError):
        card = Card("black", 1, 15, 1)


def test_bad_creation_trump():
    with pytest.raises(ValueError):
        card = Card("black", 1, 15, 15, "no")
