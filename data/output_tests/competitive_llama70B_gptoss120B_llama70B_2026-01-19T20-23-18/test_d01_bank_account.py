import pytest
from data.input_code.d01_bank_account import *

# -------------------- Initialization Tests --------------------

def test_bank_account_init_success():
    acct = BankAccount(initial_balance=100)
    assert acct.balance == 100
    assert acct.is_active is True

def test_bank_account_init_negative_balance():
    with pytest.raises(ValueError):
        BankAccount(initial_balance=-50)

# -------------------- Deposit Tests --------------------

def test_bank_account_deposit_success():
    acct = BankAccount(initial_balance=100)
    new_balance = acct.deposit(50)
    assert new_balance == 150
    assert acct.balance == 150

@pytest.mark.parametrize(
    "setup_frozen, deposit_amount, expected_exception",
    [
        (True, 50, ValueError),   # frozen account
        (False, 0, ValueError),   # non‑positive amount
        (False, -10, ValueError), # negative amount (also non‑positive)
    ]
)
def test_bank_account_deposit_errors(setup_frozen, deposit_amount, expected_exception):
    acct = BankAccount(initial_balance=100)
    if setup_frozen:
        acct.freeze_account()
    with pytest.raises(expected_exception):
        acct.deposit(deposit_amount)

# -------------------- Withdrawal Tests --------------------

def test_bank_account_withdraw_success():
    acct = BankAccount(initial_balance=100)
    remaining = acct.withdraw(50)
    assert remaining == 50
    assert acct.balance == 50

@pytest.mark.parametrize(
    "setup_frozen, withdraw_amount, expected_exception",
    [
        (True, 50, ValueError),    # frozen account
        (False, 0, ValueError),    # non‑positive amount
        (False, -5, ValueError),   # negative amount
        (False, 150, ValueError),  # insufficient funds
    ]
)
def test_bank_account_withdraw_errors(setup_frozen, withdraw_amount, expected_exception):
    acct = BankAccount(initial_balance=100)
    if setup_frozen:
        acct.freeze_account()
    with pytest.raises(expected_exception):
        acct.withdraw(withdraw_amount)

# -------------------- Freeze/Unfreeze Tests --------------------

def test_bank_account_freeze():
    acct = BankAccount(initial_balance=100)
    acct.freeze_account()
    assert acct.is_active is False

def test_bank_account_unfreeze():
    acct = BankAccount(initial_balance=100)
    acct.freeze_account()          # ensure it starts frozen
    acct.unfreeze_account()
    assert acct.is_active is True