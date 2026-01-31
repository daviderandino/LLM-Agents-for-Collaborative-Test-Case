import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize(
    "initial_balance, expected_exception",
    [
        (100, None),          # Happy path initialization
        (-50, ValueError),    # Negative initial balance catch
    ],
)
def test_bank_account_init(initial_balance, expected_exception):
    if expected_exception is None:
        # Should not raise an exception
        account = BankAccount(initial_balance=initial_balance)
        assert account.balance == initial_balance
        assert account.is_active is True
    else:
        with pytest.raises(expected_exception):
            BankAccount(initial_balance=initial_balance)

@pytest.mark.parametrize(
    "amount, expected, freeze",
    [
        (50, 150, False),   # Happy path deposit
        (50, ValueError, True),   # Frozen account deposit catch
        (0, ValueError, False),   # Non-positive deposit amount catch
    ],
)
def test_bank_account_deposit(amount, expected, freeze):
    account = BankAccount(initial_balance=100)
    if freeze:
        account.freeze_account()
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            account.deposit(amount)
    else:
        result = account.deposit(amount)
        assert result == expected
        assert account.balance == expected

@pytest.mark.parametrize(
    "amount, expected, freeze",
    [
        (50, 50, False),    # Happy path withdrawal
        (50, ValueError, True),   # Frozen account withdrawal catch
        (0, ValueError, False),   # Non-positive withdrawal amount catch
        (150, ValueError, False), # Insufficient funds catch
    ],
)
def test_bank_account_withdraw(amount, expected, freeze):
    account = BankAccount(initial_balance=100)
    if freeze:
        account.freeze_account()
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            account.withdraw(amount)
    else:
        result = account.withdraw(amount)
        assert result == expected
        assert account.balance == 100 - amount

def test_bank_account_freeze():
    account = BankAccount(initial_balance=100)
    account.freeze_account()
    assert account.is_active is False

def test_bank_account_unfreeze():
    account = BankAccount(initial_balance=100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active is True