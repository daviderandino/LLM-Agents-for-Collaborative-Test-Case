import pytest
from data.input_code.d01_bank_account import *

# ---------- __init__ ----------
@pytest.mark.parametrize(
    "initial_balance, expected_balance, expect_exception",
    [
        (100, 100, None),   # positive balance
        (0, 0, None),       # zero balance
        (-10, None, ValueError),  # negative balance
    ],
)
def test_bank_account_init(initial_balance, expected_balance, expect_exception):
    if expect_exception:
        with pytest.raises(expect_exception):
            BankAccount(initial_balance)
    else:
        acc = BankAccount(initial_balance)
        assert acc.balance == expected_balance
        assert acc.is_active is True


# ---------- deposit ----------
@pytest.mark.parametrize(
    "initial_balance, amount, freeze_before, expected_balance, expect_exception",
    [
        (100, 50, False, 150, None),          # normal deposit
        (100, 50, True, None, ValueError),    # deposit on frozen account
        (100, 0, False, None, ValueError),    # zero amount
        (100, -20, False, None, ValueError),  # negative amount
    ],
)
def test_bank_account_deposit(
    initial_balance, amount, freeze_before, expected_balance, expect_exception
):
    acc = BankAccount(initial_balance)
    if freeze_before:
        acc.freeze_account()
    if expect_exception:
        with pytest.raises(expect_exception):
            acc.deposit(amount)
    else:
        result = acc.deposit(amount)
        assert result == expected_balance
        assert acc.balance == expected_balance


# ---------- withdraw ----------
@pytest.mark.parametrize(
    "initial_balance, amount, freeze_before, expected_balance, expect_exception",
    [
        (100, 20, False, 80, None),            # normal withdraw
        (100, 20, True, None, ValueError),     # withdraw on frozen account
        (100, 0, False, None, ValueError),     # zero amount
        (100, -10, False, None, ValueError),   # negative amount
        (100, 200, False, None, ValueError),   # insufficient funds
    ],
)
def test_bank_account_withdraw(
    initial_balance, amount, freeze_before, expected_balance, expect_exception
):
    acc = BankAccount(initial_balance)
    if freeze_before:
        acc.freeze_account()
    if expect_exception:
        with pytest.raises(expect_exception):
            acc.withdraw(amount)
    else:
        result = acc.withdraw(amount)
        assert result == expected_balance
        assert acc.balance == expected_balance


# ---------- freeze / unfreeze ----------
def test_freeze_and_unfreeze():
    acc = BankAccount(50)
    # freeze
    acc.freeze_account()
    assert acc.is_active is False
    # operations should now raise
    with pytest.raises(ValueError):
        acc.deposit(10)
    with pytest.raises(ValueError):
        acc.withdraw(10)
    # unfreeze
    acc.unfreeze_account()
    assert acc.is_active is True
    # now operations succeed
    assert acc.deposit(10) == 60
    assert acc.withdraw(20) == 40