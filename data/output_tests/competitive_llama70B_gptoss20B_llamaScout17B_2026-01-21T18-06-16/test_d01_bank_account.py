import pytest
from data.input_code.d01_bank_account import BankAccount

# ---------- Initialization Tests ----------
@pytest.mark.parametrize(
    "initial_balance, expected_exception",
    [
        (100, None),          # Happy path
        (-50, ValueError),    # Negative balance
    ],
)
def test_bank_account_init(initial_balance, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            BankAccount(initial_balance=initial_balance)
    else:
        account = BankAccount(initial_balance=initial_balance)
        assert account.balance == initial_balance
        assert account.is_active is True

# ---------- Deposit Tests ----------
@pytest.mark.parametrize(
    "amount, initial_balance, freeze, expected_balance, expected_exception",
    [
        (50, 100, False, 150, None),          # Happy path deposit
        (50, 100, True, None, ValueError),    # Frozen account deposit
        (0, 100, False, None, ValueError),    # Non-positive deposit
    ],
)
def test_bank_account_deposit(amount, initial_balance, freeze, expected_balance, expected_exception):
    account = BankAccount(initial_balance=initial_balance)
    if freeze:
        account.freeze_account()
    if expected_exception:
        with pytest.raises(expected_exception):
            account.deposit(amount)
    else:
        result = account.deposit(amount)
        assert result == expected_balance
        assert account.balance == expected_balance

# ---------- Withdraw Tests ----------
@pytest.mark.parametrize(
    "amount, initial_balance, freeze, expected_balance, expected_exception",
    [
        (50, 100, False, 50, None),           # Happy path withdrawal
        (50, 100, True, None, ValueError),    # Frozen account withdrawal
        (0, 100, False, None, ValueError),    # Non-positive withdrawal
        (150, 100, False, None, ValueError),  # Insufficient funds
    ],
)
def test_bank_account_withdraw(amount, initial_balance, freeze, expected_balance, expected_exception):
    account = BankAccount(initial_balance=initial_balance)
    if freeze:
        account.freeze_account()
    if expected_exception:
        with pytest.raises(expected_exception):
            account.withdraw(amount)
    else:
        result = account.withdraw(amount)
        assert result == expected_balance
        assert account.balance == expected_balance

# ---------- Freeze / Unfreeze Tests ----------
def test_bank_account_freeze():
    account = BankAccount(initial_balance=100)
    account.freeze_account()
    assert account.is_active is False

def test_bank_account_unfreeze():
    account = BankAccount(initial_balance=100)
    account.freeze_account()
    assert account.is_active is False
    account.unfreeze_account()
    assert account.is_active is True