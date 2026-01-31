import pytest
from data.input_code.d01_bank import *

@pytest.fixture
def account():
    """Return a fresh BankAccount with a positive balance."""
    return BankAccount(initial_balance=100)

@pytest.mark.parametrize(
    "initial_balance, expected_exception",
    [
        (100, None),   # Positive initial balance
        (0, None),     # Zero initial balance
        (-10, ValueError),  # Negative initial balance
    ],
)
def test_bank_account_init(initial_balance, expected_exception):
    if expected_exception is None:
        acc = BankAccount(initial_balance=initial_balance)
        assert acc.balance == initial_balance
        assert acc.is_active is True
    else:
        with pytest.raises(expected_exception):
            BankAccount(initial_balance=initial_balance)

@pytest.mark.parametrize(
    "amount, expected_balance",
    [
        (50, 150),   # Valid deposit
    ],
)
def test_deposit_success(account, amount, expected_balance):
    result = account.deposit(amount)
    assert result == expected_balance
    assert account.balance == expected_balance

def test_deposit_frozen(account):
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(50)

@pytest.mark.parametrize(
    "amount, expected_exception",
    [
        (0, ValueError),   # Zero deposit amount
        (-20, ValueError), # Negative deposit amount
    ],
)
def test_deposit_invalid_amount(account, amount, expected_exception):
    with pytest.raises(expected_exception):
        account.deposit(amount)

@pytest.mark.parametrize(
    "amount, expected_balance",
    [
        (20, 80),   # Valid withdrawal
    ],
)
def test_withdraw_success(account, amount, expected_balance):
    result = account.withdraw(amount)
    assert result == expected_balance
    assert account.balance == expected_balance

def test_withdraw_frozen(account):
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(20)

@pytest.mark.parametrize(
    "amount, expected_exception",
    [
        (0, ValueError),    # Zero withdrawal amount
        (-10, ValueError),  # Negative withdrawal amount
        (200, ValueError),  # Insufficient funds
    ],
)
def test_withdraw_invalid_amount(account, amount, expected_exception):
    with pytest.raises(expected_exception):
        account.withdraw(amount)

def test_freeze_account(account):
    account.freeze_account()
    assert account.is_active is False

def test_unfreeze_account(account):
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active is True