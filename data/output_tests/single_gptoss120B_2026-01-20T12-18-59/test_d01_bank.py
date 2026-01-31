import pytest
from data.input_code.d01_bank import BankAccount


def test_init_negative_balance_raises():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(initial_balance=-1)


@pytest.mark.parametrize("initial_balance", [0, 100])
def test_init_valid_balances(initial_balance):
    account = BankAccount(initial_balance=initial_balance)
    assert account.balance == initial_balance
    assert account.is_active is True


@pytest.mark.parametrize("amount", [0, -10])
def test_deposit_non_positive_raises(amount):
    account = BankAccount()
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(amount)


def test_deposit_success_and_balance_update():
    account = BankAccount(initial_balance=50)
    new_balance = account.deposit(25)
    assert new_balance == 75
    assert account.balance == 75


def test_deposit_when_frozen_raises():
    account = BankAccount()
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(10)


@pytest.mark.parametrize("amount", [0, -5])
def test_withdraw_non_positive_raises(amount):
    account = BankAccount(initial_balance=100)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(amount)


def test_withdraw_success_and_balance_update():
    account = BankAccount(initial_balance=80)
    new_balance = account.withdraw(30)
    assert new_balance == 50
    assert account.balance == 50


def test_withdraw_insufficient_funds_raises():
    account = BankAccount(initial_balance=20)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(30)


def test_withdraw_when_frozen_raises():
    account = BankAccount(initial_balance=100)
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(10)


def test_freeze_and_unfreeze_behavior():
    account = BankAccount()
    account.freeze_account()
    assert account.is_active is False
    with pytest.raises(ValueError):
        account.deposit(10)
    account.unfreeze_account()
    assert account.is_active is True
    # Now deposit should work
    account.deposit(10)
    assert account.balance == 10