import pytest
from data.input_code.d01_bank_account import *

# ---------- __init__ tests ----------
def test_init_negative_balance():
    with pytest.raises(ValueError):
        BankAccount(-10)

def test_init_zero_balance():
    acc = BankAccount(0)
    assert acc.balance == 0
    assert acc.is_active is True

def test_init_positive_balance():
    acc = BankAccount(100)
    assert acc.balance == 100
    assert acc.is_active is True

# ---------- deposit tests ----------
@pytest.mark.parametrize(
    "initial_balance, amount, freeze, expected",
    [
        (50, 25, False, 75),          # positive amount
        (50, 10, True, ValueError),   # frozen account
        (50, -5, False, ValueError),  # non‑positive amount
        (50, None, False, TypeError), # None amount
        (50, "", False, TypeError),   # empty string amount
        (50, [], False, TypeError),   # empty list amount
    ],
)
def test_deposit(initial_balance, amount, freeze, expected):
    acc = BankAccount(initial_balance)
    if freeze:
        acc.freeze_account()
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            acc.deposit(amount)
    else:
        result = acc.deposit(amount)
        assert result == expected

# ---------- withdraw tests ----------
@pytest.mark.parametrize(
    "initial_balance, amount, freeze, expected",
    [
        (50, 20, False, 30),          # sufficient funds
        (50, 10, True, ValueError),   # frozen account
        (50, 0, False, ValueError),   # non‑positive amount
        (50, 60, False, ValueError),  # insufficient funds
    ],
)
def test_withdraw(initial_balance, amount, freeze, expected):
    acc = BankAccount(initial_balance)
    if freeze:
        acc.freeze_account()
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            acc.withdraw(amount)
    else:
        result = acc.withdraw(amount)
        assert result == expected

# ---------- freeze_account test ----------
def test_freeze_account():
    acc = BankAccount(50)
    acc.freeze_account()
    assert acc.is_active is False

# ---------- unfreeze_account test ----------
def test_unfreeze_account():
    acc = BankAccount(50)
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True