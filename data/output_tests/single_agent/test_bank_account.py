import pytest
from data.input_code.bank_account import BankAccount


# ---------- Constructor Tests ----------
def test_initial_balance_default():
    account = BankAccount()
    assert account.balance == 0
    assert account.is_active is True


def test_initial_balance_positive():
    account = BankAccount(100)
    assert account.balance == 100
    assert account.is_active is True


def test_initial_balance_negative_raises():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(-50)


# ---------- Deposit Tests ----------
@pytest.mark.parametrize(
    "initial,deposit,expected_balance",
    [
        (0, 50, 50),
        (100, 25, 125),
        (1_000_000, 999_999, 1_999_999),
    ],
)
def test_deposit_success(initial, deposit, expected_balance):
    account = BankAccount(initial)
    new_balance = account.deposit(deposit)
    assert new_balance == expected_balance
    assert account.balance == expected_balance


@pytest.mark.parametrize(
    "amount",
    [0, -10, -0.01],
)
def test_deposit_invalid_amount_raises(amount):
    account = BankAccount()
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(amount)


def test_deposit_on_frozen_account_raises():
    account = BankAccount()
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(10)


# ---------- Withdraw Tests ----------
@pytest.mark.parametrize(
    "initial,withdraw,expected_balance",
    [
        (100, 50, 50),
        (200, 200, 0),
        (1_000_000, 999_999, 1),
    ],
)
def test_withdraw_success(initial, withdraw, expected_balance):
    account = BankAccount(initial)
    new_balance = account.withdraw(withdraw)
    assert new_balance == expected_balance
    assert account.balance == expected_balance


@pytest.mark.parametrize(
    "amount",
    [0, -5, -0.01],
)
def test_withdraw_invalid_amount_raises(amount):
    account = BankAccount(100)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(amount)


def test_withdraw_insufficient_funds_raises():
    account = BankAccount(50)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(100)


def test_withdraw_on_frozen_account_raises():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(10)


# ---------- Freeze / Unfreeze Tests ----------
def test_freeze_and_unfreeze_toggle():
    account = BankAccount(100)
    assert account.is_active is True

    account.freeze_account()
    assert account.is_active is False

    account.unfreeze_account()
    assert account.is_active is True


def test_multiple_freeze_unfreeze_cycles():
    account = BankAccount(100)
    for _ in range(5):
        account.freeze_account()
        assert account.is_active is False
        account.unfreeze_account()
        assert account.is_active is True


def test_freeze_does_not_change_balance():
    account = BankAccount(200)
    account.freeze_account()
    assert account.balance == 200
    account.unfreeze_account()
    assert account.balance == 200


# ---------- Combined Operation Tests ----------
def test_deposit_and_withdraw_sequence():
    account = BankAccount(100)
    account.deposit(50)          # 150
    account.withdraw(30)         # 120
    account.deposit(20)          # 140
    account.withdraw(140)        # 0
    assert account.balance == 0


def test_operations_after_freeze_and_unfreeze():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(10)
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(10)

    account.unfreeze_account()
    # After unfreezing, operations should succeed
    assert account.deposit(10) == 110
    assert account.withdraw(20) == 90


# ---------- Edge Case Tests ----------
def test_deposit_and_withdraw_large_amounts():
    large_amount = 10**12
    account = BankAccount(large_amount)
    # Deposit a large amount
    new_balance = account.deposit(large_amount)
    assert new_balance == large_amount * 2
    # Withdraw a large amount
    new_balance = account.withdraw(large_amount * 2)
    assert new_balance == 0


def test_withdraw_exact_balance():
    account = BankAccount(75)
    new_balance = account.withdraw(75)
    assert new_balance == 0
    assert account.balance == 0


def test_deposit_and_withdraw_float_precision():
    account = BankAccount(0.0)
    account.deposit(0.1)
    account.deposit(0.2)
    # Due to floating point arithmetic, use pytest.approx
    assert account.balance == pytest.approx(0.3)
    account.withdraw(0.1)
    assert account.balance == pytest.approx(0.2)