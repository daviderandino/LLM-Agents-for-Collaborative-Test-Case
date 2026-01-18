import pytest
from data.input_code.d01_bank_account import *

# -------------------- Initialization Tests --------------------

@pytest.mark.parametrize('initial_balance, expected_balance, expect_exception', [
    (100, 100, None),          # Happy path
    (-100, None, ValueError),  # Negative balance should raise
])
def test_bank_account_init(initial_balance, expected_balance, expect_exception):
    if expect_exception:
        with pytest.raises(expect_exception):
            BankAccount(initial_balance)
    else:
        acc = BankAccount(initial_balance)
        assert acc.balance == expected_balance
        assert acc.is_active is True


# -------------------- Deposit Tests --------------------

@pytest.mark.parametrize(
    'initial_balance, freeze, amount, expected_balance, expect_exception',
    [
        (100, False, 50, 150, None),          # successful deposit
        (100, True, 50, None, ValueError),    # deposit on frozen account
        (100, False, 0, None, ValueError),    # non‑positive deposit amount
    ]
)
def test_bank_account_deposit(initial_balance, freeze, amount, expected_balance, expect_exception):
    acc = BankAccount(initial_balance)
    if freeze:
        acc.freeze_account()
    if expect_exception:
        with pytest.raises(expect_exception):
            acc.deposit(amount)
    else:
        result = acc.deposit(amount)
        assert result == expected_balance
        assert acc.balance == expected_balance


# -------------------- Withdraw Tests --------------------

@pytest.mark.parametrize(
    'initial_balance, freeze, amount, expected_balance, expect_exception',
    [
        (100, False, 50, 50, None),           # successful withdrawal
        (100, True, 50, None, ValueError),    # withdraw on frozen account
        (100, False, 0, None, ValueError),    # non‑positive withdrawal amount
        (100, False, 200, None, ValueError),  # insufficient funds
    ]
)
def test_bank_account_withdraw(initial_balance, freeze, amount, expected_balance, expect_exception):
    acc = BankAccount(initial_balance)
    if freeze:
        acc.freeze_account()
    if expect_exception:
        with pytest.raises(expect_exception):
            acc.withdraw(amount)
    else:
        result = acc.withdraw(amount)
        assert result == expected_balance
        assert acc.balance == expected_balance


# -------------------- Freeze / Unfreeze Tests --------------------

def test_bank_account_freeze():
    acc = BankAccount(100)
    acc.freeze_account()
    assert acc.is_active is False

def test_bank_account_unfreeze():
    acc = BankAccount(100)
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True