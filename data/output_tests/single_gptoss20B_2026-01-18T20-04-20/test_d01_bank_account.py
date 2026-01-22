import pytest
from data.input_code.d01_bank_account import BankAccount


def test_init_negative_balance_raises():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(initial_balance=-10)


def test_init_zero_balance():
    account = BankAccount(initial_balance=0)
    assert account.balance == 0
    assert account.is_active is True


def test_init_positive_balance():
    account = BankAccount(initial_balance=100)
    assert account.balance == 100
    assert account.is_active is True


@pytest.mark.parametrize(
    "amount,expected_balance",
    [(50, 50), (100, 100), (1, 1)],
)
def test_deposit_success(amount, expected_balance):
    account = BankAccount()
    result = account.deposit(amount)
    assert result == expected_balance
    assert account.balance == expected_balance
    assert account.is_active is True


@pytest.mark.parametrize(
    "amount",
    [0, -5, -100],
)
def test_deposit_invalid_amount_raises(amount):
    account = BankAccount()
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(amount)
    # balance should remain unchanged
    assert account.balance == 0


def test_deposit_frozen_account_raises():
    account = BankAccount()
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(10)
    assert account.balance == 0


@pytest.mark.parametrize(
    "amount,expected_balance",
    [(30, 70), (100, 0), (1, 99)],
)
def test_withdraw_success(amount, expected_balance):
    account = BankAccount(initial_balance=100)
    result = account.withdraw(amount)
    assert result == expected_balance
    assert account.balance == expected_balance
    assert account.is_active is True


@pytest.mark.parametrize(
    "amount",
    [0, -10, -1],
)
def test_withdraw_invalid_amount_raises(amount):
    account = BankAccount(initial_balance=50)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(amount)
    # balance should remain unchanged
    assert account.balance == 50


def test_withdraw_insufficient_funds_raises():
    account = BankAccount(initial_balance=20)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(30)
    assert account.balance == 20


def test_withdraw_frozen_account_raises():
    account = BankAccount(initial_balance=50)
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(10)
    assert account.balance == 50


def test_freeze_and_unfreeze_toggle():
    account = BankAccount()
    account.freeze_account()
    assert account.is_active is False
    account.unfreeze_account()
    assert account.is_active is True
    # Freeze again to ensure idempotence
    account.freeze_account()
    assert account.is_active is False
    account.unfreeze_account()
    assert account.is_active is True


def test_balance_unchanged_after_failed_operations():
    account = BankAccount(initial_balance=100)
    # Failed deposit
    with pytest.raises(ValueError):
        account.deposit(-5)
    # Failed withdraw
    with pytest.raises(ValueError):
        account.withdraw(200)
    # Freeze/unfreeze
    account.freeze_account()
    account.unfreeze_account()
    assert account.balance == 100
    assert account.is_active is True


def test_deposit_and_withdraw_sequence():
    account = BankAccount()
    # Deposit 200
    account.deposit(200)
    assert account.balance == 200
    # Withdraw 50
    account.withdraw(50)
    assert account.balance == 150
    # Deposit 25
    account.deposit(25)
    assert account.balance == 175
    # Withdraw 175
    account.withdraw(175)
    assert account.balance == 0


def test_multiple_freeze_unfreeze():
    account = BankAccount()
    account.freeze_account()
    account.freeze_account()  # should remain frozen
    assert account.is_active is False
    account.unfreeze_account()
    account.unfreeze_account()  # should remain active
    assert account.is_active is True


def test_deposit_large_amount_and_withdraw_equal_balance():
    account = BankAccount()
    large_amount = 10**12
    account.deposit(large_amount)
    assert account.balance == large_amount
    account.withdraw(large_amount)
    assert account.balance == 0
    # After withdrawal, try to withdraw again to trigger insufficient funds
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(1)
    assert account.balance == 0
    # Ensure deposit zero still raises
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(0)
    # Ensure withdraw zero still raises
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(0)
    # Ensure negative amounts raise
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(-1)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(-1)
    # Ensure balance unchanged after failed operations
    assert account.balance == 0
    assert account.is_active is True