import pytest
from data.input_code.d01_bank import *

def _make_account(initial_balance=0, is_active=True):
    """Helper to create a BankAccount with optional active state."""
    acct = BankAccount(initial_balance)
    if not is_active:
        acct.freeze_account()
    return acct

@pytest.mark.parametrize(
    "initial_balance, expected",
    [
        (0, {"balance": 0, "is_active": True}),
        (100, {"balance": 100, "is_active": True}),
    ],
)
def test_init_success(initial_balance, expected):
    acct = BankAccount(initial_balance)
    assert acct.balance == expected["balance"]
    assert acct.is_active == expected["is_active"]

def test_init_negative():
    with pytest.raises(ValueError):
        BankAccount(-10)

@pytest.mark.parametrize(
    "initial_balance, amount, expected_balance",
    [
        (10, 50, 60),
        (10, 1000000000000, 1000000000010),
        (10, 1000000000001, 1000000000011),
        (10, 10.5, 20.5),
    ],
)
def test_deposit_success(initial_balance, amount, expected_balance):
    acct = _make_account(initial_balance)
    result = acct.deposit(amount)
    assert result == expected_balance
    assert acct.balance == expected_balance

@pytest.mark.parametrize(
    "initial_balance, amount, exc_type",
    [
        (10, 0, ValueError),
        (10, -1, ValueError),
        (10, None, TypeError),
        (10, [], TypeError),
    ],
)
def test_deposit_invalid_amount(initial_balance, amount, exc_type):
    acct = _make_account(initial_balance)
    with pytest.raises(exc_type):
        acct.deposit(amount)

def test_deposit_inactive():
    acct = _make_account(10, is_active=False)
    with pytest.raises(ValueError):
        acct.deposit(10)

def test_deposit_after_freeze_unfreeze():
    acct = _make_account(10, is_active=False)
    acct.unfreeze_account()
    result = acct.deposit(5)
    assert result == 15
    assert acct.balance == 15

@pytest.mark.parametrize(
    "initial_balance, amount, expected_balance",
    [
        (10, 5, 5),
        (1000000000000, 500000000000, 500000000000),
        (20.5, 5.5, 15.0),
    ],
)
def test_withdraw_success(initial_balance, amount, expected_balance):
    acct = _make_account(initial_balance)
    result = acct.withdraw(amount)
    assert result == expected_balance
    assert acct.balance == expected_balance

@pytest.mark.parametrize(
    "initial_balance, amount, exc_type",
    [
        (10, 0, ValueError),
        (10, -1, ValueError),
        (10, 20, ValueError),          # insufficient funds
        (10, None, TypeError),
        (10, "", TypeError),
    ],
)
def test_withdraw_invalid_amount(initial_balance, amount, exc_type):
    acct = _make_account(initial_balance)
    with pytest.raises(exc_type):
        acct.withdraw(amount)

def test_withdraw_inactive():
    acct = _make_account(10, is_active=False)
    with pytest.raises(ValueError):
        acct.withdraw(5)

def test_withdraw_after_freeze_unfreeze():
    acct = _make_account(10, is_active=False)
    acct.unfreeze_account()
    result = acct.withdraw(5)
    assert result == 5
    assert acct.balance == 5

def test_freeze_account():
    acct = _make_account(10)
    acct.freeze_account()
    assert acct.is_active is False

def test_unfreeze_account():
    acct = _make_account(10, is_active=False)
    acct.unfreeze_account()
    assert acct.is_active is True