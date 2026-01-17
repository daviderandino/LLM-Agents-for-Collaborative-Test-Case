import pytest
from data.input_code.d01_bank_account import BankAccount


def test_init_with_zero_and_positive_balance():
    account_zero = BankAccount()
    assert account_zero.balance == 0
    assert account_zero.is_active

    account_positive = BankAccount(100)
    assert account_positive.balance == 100
    assert account_positive.is_active


def test_init_negative_balance_raises():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(-50)


@pytest.mark.parametrize("amount", [10, 100.5])
def test_deposit_success(amount):
    account = BankAccount(20)
    new_balance = account.deposit(amount)
    assert new_balance == 20 + amount
    assert account.balance == new_balance


@pytest.mark.parametrize("amount", [0, -5, -0.1])
def test_deposit_invalid_amount_raises(amount):
    account = BankAccount()
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(amount)


def test_deposit_when_frozen_raises():
    account = BankAccount()
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(10)


@pytest.mark.parametrize("amount", [5, 20.75])
def test_withdraw_success(amount):
    account = BankAccount(50)
    new_balance = account.withdraw(amount)
    assert new_balance == 50 - amount
    assert account.balance == new_balance


def test_withdraw_exact_balance():
    account = BankAccount(30)
    new_balance = account.withdraw(30)
    assert new_balance == 0
    assert account.balance == 0


@pytest.mark.parametrize("amount", [0, -10, -1.5])
def test_withdraw_invalid_amount_raises(amount):
    account = BankAccount(20)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(amount)


def test_withdraw_insufficient_funds_raises():
    account = BankAccount(15)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(20)


def test_withdraw_when_frozen_raises():
    account = BankAccount(50)
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(10)


def test_freeze_and_unfreeze_behavior():
    account = BankAccount(100)
    # Initially active
    assert account.is_active

    # Freeze account
    account.freeze_account()
    assert not account.is_active
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(10)
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(10)

    # Unfreeze account
    account.unfreeze_account()
    assert account.is_active
    # Operations should now succeed
    account.deposit(20)
    account.withdraw(30)
    assert account.balance == 100 + 20 - 30
    assert account.is_active