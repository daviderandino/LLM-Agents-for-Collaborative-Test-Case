import pytest
from data.input_code.01_bank import *

@pytest.mark.parametrize(
    "initial_balance, expected",
    [
        (-10, ValueError),
        (0, {"balance": 0, "is_active": True}),
        (100, {"balance": 100, "is_active": True}),
    ],
)
def test_bank_account_init(initial_balance, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            BankAccount(initial_balance)
    else:
        account = BankAccount(initial_balance)
        assert account.balance == expected["balance"]
        assert account.is_active == expected["is_active"]

@pytest.mark.parametrize(
    "initial_balance, amount, expected",
    [
        (50, 25, 75),          # T4_DEPOSIT_POS
        (50, 0, ValueError),   # T6_DEPOSIT_ZERO
    ],
)
def test_bank_account_deposit(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            account.deposit(amount)
    else:
        result = account.deposit(amount)
        assert result == expected

def test_bank_account_deposit_frozen():
    account = BankAccount(50)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(25)

@pytest.mark.parametrize(
    "initial_balance, amount, expected",
    [
        (100, 30, 70),          # T7_WITHDRAW_POS
        (50, 60, ValueError),   # T8_WITHDRAW_OVER
        (50, 0, ValueError),    # T10_WITHDRAW_ZERO
    ],
)
def test_bank_account_withdraw(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            account.withdraw(amount)
    else:
        result = account.withdraw(amount)
        assert result == expected

def test_bank_account_withdraw_frozen():
    account = BankAccount(50)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(10)

import pytest
from data.input_code.01_bank import *

@pytest.mark.parametrize(
    "initial_balance, amount, expected",
    [
        (10, -5, ValueError),   # Negative deposit
        (10, -1, ValueError),   # Negative deposit
    ],
)
def test_bank_account_deposit_negative(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            account.deposit(amount)
    else:
        result = account.deposit(amount)
        assert result == expected

@pytest.mark.parametrize(
    "initial_balance, amount, expected",
    [
        (10, -5, ValueError),   # Negative withdrawal
        (10, -1, ValueError),   # Negative withdrawal
    ],
)
def test_bank_account_withdraw_negative(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            account.withdraw(amount)
    else:
        result = account.withdraw(amount)
        assert result == expected

def test_bank_account_freeze_unfreeze_behavior():
    account = BankAccount(100)
    assert account.is_active
    account.freeze_account()
    assert not account.is_active
    account.unfreeze_account()
    assert account.is_active

def test_bank_account_freeze_does_not_change_balance():
    account = BankAccount(50)
    balance_before = account.balance
    account.freeze_account()
    assert account.balance == balance_before

def test_bank_account_unfreeze_does_not_change_balance():
    account = BankAccount(50)
    balance_before = account.balance
    account.unfreeze_account()
    assert account.balance == balance_before

def test_bank_account_deposit_after_unfreeze():
    account = BankAccount(20)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(10)
    account.unfreeze_account()
    result = account.deposit(10)
    assert result == 30

def test_bank_account_withdraw_after_unfreeze():
    account = BankAccount(30)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(5)
    account.unfreeze_account()
    result = account.withdraw(5)
    assert result == 25

def test_bank_account_multiple_freeze():
    account = BankAccount(10)
    account.freeze_account()
    account.freeze_account()
    assert not account.is_active

def test_bank_account_multiple_unfreeze():
    account = BankAccount(10)
    account.freeze_account()
    account.unfreeze_account()
    account.unfreeze_account()
    assert account.is_active

def test_bank_account_zero_balance_freeze_unfreeze():
    account = BankAccount(0)
    account.freeze_account()
    assert not account.is_active
    account.unfreeze_account()
    assert account.is_active