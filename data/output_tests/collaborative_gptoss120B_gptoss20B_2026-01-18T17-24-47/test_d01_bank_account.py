import pytest
from data.input_code.d01_bank_account import *

# ---------- __init__ ----------
@pytest.mark.parametrize(
    "initial_balance, expected",
    [
        (0, {"balance": 0, "is_active": True}),
        (500, {"balance": 500, "is_active": True}),
    ],
)
def test_init_success(initial_balance, expected):
    acc = BankAccount(initial_balance)
    assert acc.balance == expected["balance"]
    assert acc.is_active == expected["is_active"]


def test_init_negative():
    with pytest.raises(ValueError):
        BankAccount(-100)


# ---------- deposit ----------
@pytest.mark.parametrize(
    "initial_balance, amount, expected_balance",
    [
        (200, 150, 350),
    ],
)
def test_deposit_success(initial_balance, amount, expected_balance):
    acc = BankAccount(initial_balance)
    result = acc.deposit(amount)
    assert result == expected_balance
    assert acc.balance == expected_balance


def test_deposit_frozen():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.deposit(50)


def test_deposit_negative_amount():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.deposit(-20)


# ---------- withdraw ----------
@pytest.mark.parametrize(
    "initial_balance, amount, expected_balance",
    [
        (300, 120, 180),
    ],
)
def test_withdraw_success(initial_balance, amount, expected_balance):
    acc = BankAccount(initial_balance)
    result = acc.withdraw(amount)
    assert result == expected_balance
    assert acc.balance == expected_balance


def test_withdraw_frozen():
    acc = BankAccount(200)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.withdraw(50)


def test_withdraw_non_positive():
    acc = BankAccount(200)
    with pytest.raises(ValueError):
        acc.withdraw(0)


def test_withdraw_overdraft():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.withdraw(150)


# ---------- freeze_account ----------
def test_freeze_account():
    acc = BankAccount(50)
    acc.freeze_account()
    assert acc.is_active is False


# ---------- unfreeze_account ----------
def test_unfreeze_account():
    acc = BankAccount(50)
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True