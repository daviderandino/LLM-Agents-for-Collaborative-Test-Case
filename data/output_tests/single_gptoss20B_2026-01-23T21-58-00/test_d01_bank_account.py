import pytest
from data.input_code.d01_bank_account import BankAccount


def test_init_negative_balance_raises():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(-1)


def test_init_zero_balance():
    acc = BankAccount()
    assert acc.balance == 0
    assert acc.is_active is True


def test_init_positive_balance():
    acc = BankAccount(100)
    assert acc.balance == 100
    assert acc.is_active is True


def test_deposit_positive():
    acc = BankAccount(50)
    new_balance = acc.deposit(25)
    assert new_balance == 75
    assert acc.balance == 75


def test_deposit_zero_or_negative_raises():
    acc = BankAccount()
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        acc.deposit(0)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        acc.deposit(-10)


def test_deposit_when_frozen_raises():
    acc = BankAccount()
    acc.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        acc.deposit(10)


def test_withdraw_positive_less_than_balance():
    acc = BankAccount(100)
    new_balance = acc.withdraw(30)
    assert new_balance == 70
    assert acc.balance == 70


def test_withdraw_exact_balance():
    acc = BankAccount(50)
    new_balance = acc.withdraw(50)
    assert new_balance == 0
    assert acc.balance == 0


def test_withdraw_zero_or_negative_raises():
    acc = BankAccount(10)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        acc.withdraw(0)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        acc.withdraw(-5)


def test_withdraw_insufficient_funds_raises():
    acc = BankAccount(20)
    with pytest.raises(ValueError, match="Insufficient funds"):
        acc.withdraw(25)


def test_withdraw_when_frozen_raises():
    acc = BankAccount(30)
    acc.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        acc.withdraw(10)


def test_freeze_and_unfreeze():
    acc = BankAccount(10)
    acc.freeze_account()
    assert acc.is_active is False
    acc.unfreeze_account()
    assert acc.is_active is True


def test_multiple_freeze_unfreeze():
    acc = BankAccount(10)
    acc.freeze_account()
    acc.freeze_account()  # idempotent
    assert acc.is_active is False
    acc.unfreeze_account()
    acc.unfreeze_account()  # idempotent
    assert acc.is_active is True


def test_deposit_after_unfreeze():
    acc = BankAccount(5)
    acc.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        acc.deposit(5)
    acc.unfreeze_account()
    acc.deposit(5)
    assert acc.balance == 10


def test_withdraw_after_unfreeze():
    acc = BankAccount(5)
    acc.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        acc.withdraw(3)
    acc.unfreeze_account()
    acc.withdraw(3)
    assert acc.balance == 2