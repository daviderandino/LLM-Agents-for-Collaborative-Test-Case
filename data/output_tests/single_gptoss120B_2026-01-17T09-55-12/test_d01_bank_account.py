import pytest
from data.input_code.d01_bank_account import BankAccount

def test_initial_balance_negative_raises():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(initial_balance=-10)

@pytest.mark.parametrize("initial_balance", [0, 100])
def test_initial_balance_sets_balance_and_active(initial_balance):
    account = BankAccount(initial_balance=initial_balance)
    assert account.balance == initial_balance
    assert account.is_active is True

def test_deposit_success_and_returned_balance():
    account = BankAccount(50)
    new_balance = account.deposit(25)
    assert new_balance == 75
    assert account.balance == 75

@pytest.mark.parametrize("amount", [0, -5])
def test_deposit_invalid_amount_raises(amount):
    account = BankAccount(10)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(amount)

def test_deposit_when_frozen_raises():
    account = BankAccount(10)
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(5)

def test_withdraw_success_and_returned_balance():
    account = BankAccount(100)
    new_balance = account.withdraw(40)
    assert new_balance == 60
    assert account.balance == 60

@pytest.mark.parametrize("amount", [0, -3])
def test_withdraw_invalid_amount_raises(amount):
    account = BankAccount(20)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(amount)

def test_withdraw_insufficient_funds_raises():
    account = BankAccount(30)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(31)

def test_withdraw_when_frozen_raises():
    account = BankAccount(50)
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(10)

def test_freeze_and_unfreeze_behavior():
    account = BankAccount(10)
    account.freeze_account()
    assert account.is_active is False
    with pytest.raises(ValueError):
        account.deposit(5)
    account.unfreeze_account()
    assert account.is_active is True
    # after unfreeze, operations should succeed
    account.deposit(5)
    assert account.balance == 15
    account.withdraw(5)
    assert account.balance == 10