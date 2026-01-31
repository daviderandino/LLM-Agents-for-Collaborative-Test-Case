import pytest
from data.input_code.d01_bank import *

# -------------------- __init__ --------------------
@pytest.mark.parametrize(
    "initial_balance, expected_balance, expected_active",
    [
        (0, 0, True),          # TC01
    ],
)
def test_init_success(initial_balance, expected_balance, expected_active):
    acc = BankAccount(initial_balance)
    assert acc.balance == expected_balance
    assert acc.is_active == expected_active

def test_init_negative_balance():
    # TC02
    with pytest.raises(ValueError):
        BankAccount(-10)

# -------------------- deposit --------------------
@pytest.mark.parametrize(
    "initial_balance, is_active, amount, expected_balance",
    [
        (0, True, 50, 50),    # TC03
    ],
)
def test_deposit_success(initial_balance, is_active, amount, expected_balance):
    acc = BankAccount(initial_balance)
    acc.is_active = is_active
    result = acc.deposit(amount)
    assert result == expected_balance
    assert acc.balance == expected_balance

@pytest.mark.parametrize(
    "initial_balance, is_active, amount, exc",
    [
        (0, True, 0, ValueError),      # TC04
        (100, False, 10, ValueError),  # TC05
    ],
)
def test_deposit_exceptions(initial_balance, is_active, amount, exc):
    acc = BankAccount(initial_balance)
    acc.is_active = is_active
    with pytest.raises(exc):
        acc.deposit(amount)

# -------------------- withdraw --------------------
@pytest.mark.parametrize(
    "initial_balance, is_active, amount, expected_balance",
    [
        (100, True, 30, 70),   # TC06
    ],
)
def test_withdraw_success(initial_balance, is_active, amount, expected_balance):
    acc = BankAccount(initial_balance)
    acc.is_active = is_active
    result = acc.withdraw(amount)
    assert result == expected_balance
    assert acc.balance == expected_balance

@pytest.mark.parametrize(
    "initial_balance, is_active, amount, exc",
    [
        (100, True, 0, ValueError),      # TC07
        (50, True, 60, ValueError),      # TC08
        (100, False, 10, ValueError),    # TC09
    ],
)
def test_withdraw_exceptions(initial_balance, is_active, amount, exc):
    acc = BankAccount(initial_balance)
    acc.is_active = is_active
    with pytest.raises(exc):
        acc.withdraw(amount)

# -------------------- freeze_account --------------------
def test_freeze_account():
    # TC10
    acc = BankAccount(100)
    acc.freeze_account()
    assert acc.is_active is False

# -------------------- unfreeze_account --------------------
def test_unfreeze_account():
    # TC11
    acc = BankAccount(100)
    acc.is_active = False
    acc.unfreeze_account()
    assert acc.is_active is True