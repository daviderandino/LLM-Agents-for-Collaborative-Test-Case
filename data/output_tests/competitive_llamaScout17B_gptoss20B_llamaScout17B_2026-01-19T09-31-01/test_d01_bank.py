import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize(
    "initial_balance,expected_exception",
    [
        (100, None),   # T1_INIT_OK
        (0, None),     # T2_INIT_ZERO
        (-10, ValueError),  # T3_INIT_NEG
    ],
)
def test_bank_account_init(initial_balance, expected_exception):
    if expected_exception is None:
        account = BankAccount(initial_balance=initial_balance)
        assert account.balance == initial_balance
        assert account.is_active is True
    else:
        with pytest.raises(expected_exception):
            BankAccount(initial_balance=initial_balance)

@pytest.mark.parametrize(
    "amount,expected_result",
    [
        (50, 150),   # T4_DEP_OK
        (0, ValueError),   # T6_DEP_ZERO
        (-20, ValueError), # T7_DEP_NEG
    ],
)
def test_bank_account_deposit(amount, expected_result):
    account = BankAccount(initial_balance=100)
    if isinstance(expected_result, type) and issubclass(expected_result, Exception):
        with pytest.raises(expected_result):
            account.deposit(amount)
    else:
        result = account.deposit(amount)
        assert result == expected_result

def test_bank_account_deposit_on_frozen_account():
    account = BankAccount(initial_balance=100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(50)  # T5_DEP_FROZEN

@pytest.mark.parametrize(
    "amount,expected_result",
    [
        (20, 80),    # T8_WD_OK
        (0, ValueError),   # T10_WD_ZERO
        (-10, ValueError), # T11_WD_NEG
        (200, ValueError), # T12_WD_INSUFF
    ],
)
def test_bank_account_withdraw(amount, expected_result):
    account = BankAccount(initial_balance=100)
    if isinstance(expected_result, type) and issubclass(expected_result, Exception):
        with pytest.raises(expected_result):
            account.withdraw(amount)
    else:
        result = account.withdraw(amount)
        assert result == expected_result

def test_bank_account_withdraw_on_frozen_account():
    account = BankAccount(initial_balance=100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(20)  # T9_WD_FROZEN

def test_bank_account_freeze_and_unfreeze():
    account = BankAccount(initial_balance=50)
    # Freeze account
    account.freeze_account()
    assert account.is_active is False
    # Unfreeze account
    account.unfreeze_account()
    assert account.is_active is True