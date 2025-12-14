import pytest
from data.input_code.bank_account import BankAccount

def test_withdrawal_on_frozen_account():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError) as excinfo:
        account.withdraw(50)
    assert str(excinfo.value) == "Account is frozen"

def test_account_unfreezing():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active is True
    account.deposit(50)
    assert account.balance == 150

def test_account_freezing_and_unfreezing():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError) as excinfo:
        account.deposit(50)
    assert str(excinfo.value) == "Account is frozen"
    account.unfreeze_account()
    account.deposit(50)
    assert account.balance == 150

def test_initial_balance():
    with pytest.raises(ValueError) as excinfo:
        BankAccount(-100)
    assert str(excinfo.value) == "Initial balance cannot be negative"

def test_is_active():
    account = BankAccount(100)
    assert account.is_active is True

def test_balance_deposit():
    account = BankAccount(100)
    account.deposit(50)
    assert account.balance == 150

def test_balance_withdrawal():
    account = BankAccount(100)
    account.withdraw(50)
    assert account.balance == 50

def test_freeze_account():
    account = BankAccount(100)
    account.freeze_account()
    assert account.is_active is False

def test_unfreeze_account():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active is True

def test_deposit_negative_amount():
    account = BankAccount(100)
    with pytest.raises(ValueError) as excinfo:
        account.deposit(-50)
    assert str(excinfo.value) == "Deposit amount must be positive"

def test_withdraw_negative_amount():
    account = BankAccount(100)
    with pytest.raises(ValueError) as excinfo:
        account.withdraw(-50)
    assert str(excinfo.value) == "Withdrawal amount must be positive"

def test_insufficient_funds():
    account = BankAccount(100)
    with pytest.raises(ValueError) as excinfo:
        account.withdraw(150)
    assert str(excinfo.value) == "Insufficient funds"