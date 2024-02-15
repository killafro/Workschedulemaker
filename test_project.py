import pytest
from project import minimum_workers_check
from project import is_valid_day
from project import get_worker_name

from unittest.mock import patch


def test_get_worker_name():
    with patch("builtins.input", side_effect=["Malik"]):
        result = get_worker_name()
    assert result == "Malik"

    with patch("builtins.input", side_effect=["David"]):
        result = get_worker_name()
    assert result == "David"
    with patch("builtins.input", side_effect=["Carter"]):
        result = get_worker_name()
    assert result == "Carter"

    with patch("builtins.input", side_effect=[""]):
        result = get_worker_name()
    assert result == ""

def test_is_valid_day():
    assert is_valid_day("1") == True
    assert is_valid_day("2") == True
    assert is_valid_day("3") == True
    assert is_valid_day("4") == True
    assert is_valid_day("5") == True
    assert is_valid_day("6") == True
    assert is_valid_day("7") == True
    assert is_valid_day("10") == False
    assert is_valid_day("test") == False
    assert is_valid_day("0") == False
    assert is_valid_day("") == False
    assert is_valid_day(" ") == False
    assert is_valid_day("...") == False

def test_minimum_workers_check():

    assert minimum_workers_check(10,5) == True
    assert minimum_workers_check(8,5) == True
    assert minimum_workers_check(2,1) == True
    assert minimum_workers_check(4,2) == True
    with pytest.raises(SystemExit):
            minimum_workers_check(5,10)
    with pytest.raises(SystemExit):
            minimum_workers_check(7,11)
    with pytest.raises(SystemExit):
            minimum_workers_check(1,2)

