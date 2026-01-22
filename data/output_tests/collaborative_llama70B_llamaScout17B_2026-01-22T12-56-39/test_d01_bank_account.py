import pytest
from data.input_code.d01_bank_account import *

def test_init_success():
    account = BankAccount(100)
    assert account.balance == 100

@pytest.mark.parametrize('initial_balance', [-50])
def test_init_error(initial_balance):
    with pytest.raises(ValueError):
        BankAccount(initial_balance)

def test_deposit_success():
    account = BankAccount(100)
    result = account.deposit(50)
    assert result == 150

@pytest.mark.parametrize('amount', [0, -50])
def test_deposit_error_nonpos(amount):
    account = BankAccount(100)
    with pytest.raises(ValueError):
        account.deposit(amount)

def test_deposit_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(50)

def test_withdraw_success():
    account = BankAccount(100)
    result = account.withdraw(50)
    assert result == 50

@pytest.mark.parametrize('amount', [0, -50])
def test_withdraw_error_nonpos(amount):
    account = BankAccount(100)
    with pytest.raises(ValueError):
        account.withdraw(amount)

def test_withdraw_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(50)

def test_withdraw_error_insuff():
    account = BankAccount(100)
    with pytest.raises(ValueError):
        account.withdraw(150)

def test_freeze_account():
    account = BankAccount(100)
    account.freeze_account()
    assert not account.is_active

def test_unfreeze_account():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active