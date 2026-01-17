import pytest
from data.input_code.d01_bank_account import BankAccount


def test_init_default():
    account = BankAccount()
    assert account.balance == 0
    assert account.is_active is True


def test_init_negative_balance():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(-10)


def test_deposit_positive():
    account = BankAccount()
    new_balance = account.deposit(100)
    assert new_balance == 100
    assert account.balance == 100


def test_deposit_zero_and_negative():
    account = BankAccount()
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(0)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(-5)


def test_deposit_when_frozen():
    account = BankAccount()
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(10)


def test_withdraw_positive():
    account = BankAccount(200)
    new_balance = account.withdraw(50)
    assert new_balance == 150
    assert account.balance == 150


def test_withdraw_zero_and_negative():
    account = BankAccount(100)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(0)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(-20)


def test_withdraw_insufficient_funds():
    account = BankAccount(30)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(50)


def test_withdraw_when_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(10)


def test_freeze_and_unfreeze_toggle():
    account = BankAccount()
    assert account.is_active is True
    account.freeze_account()
    assert account.is_active is False
    account.unfreeze_account()
    assert account.is_active is True


def test_multiple_freeze_unfreeze():
    account = BankAccount()
    account.freeze_account()
    account.freeze_account()  # should remain frozen
    assert account.is_active is False
    account.unfreeze_account()
    account.unfreeze_account()  # should remain active
    assert account.is_active is True


def test_balance_and_return_values():
    account = BankAccount()
    assert account.deposit(50) == 50
    assert account.withdraw(20) == 30
    assert account.balance == 30


def test_freeze_unfreeze_cycle_operations():
    account = BankAccount(100)

    # Freeze and attempt operations
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(10)
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(10)

    # Unfreeze and perform valid operations
    account.unfreeze_account()
    assert account.deposit(20) == 120
    assert account.withdraw(30) == 90

    # Freeze again and test failures
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(5)
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(5)

    # Unfreeze and test edge cases
    account.unfreeze_account()
    assert account.deposit(10) == 100
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(200)
    assert account.withdraw(100) == 0

    # Test zero and negative amounts after unfreeze
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(0)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(0)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(-5)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(-5)
    assert account.balance == 0
    assert account.is_active is True