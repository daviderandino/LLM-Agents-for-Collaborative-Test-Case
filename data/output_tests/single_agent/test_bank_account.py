import pytest
from data.input_code.bank_account import BankAccount


def test_initial_balance_success():
    account = BankAccount(100)
    assert account.balance == 100
    assert account.is_active is True

    zero_account = BankAccount()
    assert zero_account.balance == 0
    assert zero_account.is_active is True


def test_initial_balance_negative():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(-10)


@pytest.mark.parametrize(
    "amount,expected_balance",
    [
        (50, 50),
        (100, 150),
        (0.75, 0.75),
    ],
)
def test_deposit_success(amount, expected_balance):
    account = BankAccount()
    new_balance = account.deposit(amount)
    assert new_balance == expected_balance
    assert account.balance == expected_balance


@pytest.mark.parametrize(
    "amount",
    [
        0,
        -5,
        -0.01,
    ],
)
def test_deposit_invalid_amount(amount):
    account = BankAccount()
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(amount)
    assert account.balance == 0  # balance unchanged


@pytest.mark.parametrize(
    "amount,expected_balance",
    [
        (30, 70),
        (50, 50),
        (0.25, 0.75),
    ],
)
def test_withdraw_success(amount, expected_balance):
    account = BankAccount(100)
    new_balance = account.withdraw(amount)
    assert new_balance == expected_balance
    assert account.balance == expected_balance


@pytest.mark.parametrize(
    "amount",
    [
        0,
        -10,
        -0.5,
    ],
)
def test_withdraw_invalid_amount(amount):
    account = BankAccount(100)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(amount)
    assert account.balance == 100  # balance unchanged


def test_withdraw_insufficient_funds():
    account = BankAccount(50)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(100)
    assert account.balance == 50  # balance unchanged


def test_freeze_and_unfreeze_behavior():
    account = BankAccount(200)
    # Initially active
    assert account.is_active is True

    # Freeze account
    account.freeze_account()
    assert account.is_active is False

    # Operations while frozen should fail
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(10)
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(10)
    assert account.balance == 200  # balance unchanged

    # Unfreeze account
    account.unfreeze_account()
    assert account.is_active is True

    # Operations should now succeed
    new_balance = account.deposit(20)
    assert new_balance == 220
    assert account.balance == 220

    new_balance = account.withdraw(30)
    assert new_balance == 190
    assert account.balance == 190


def test_freeze_unfreeze_idempotent():
    account = BankAccount(100)
    # Freeze twice
    account.freeze_account()
    account.freeze_account()
    assert account.is_active is False

    # Unfreeze twice
    account.unfreeze_account()
    account.unfreeze_account()
    assert account.is_active is True


def test_balance_unchanged_on_failed_operations():
    account = BankAccount(100)
    # Deposit failure
    with pytest.raises(ValueError):
        account.deposit(-5)
    assert account.balance == 100

    # Withdraw failure due to insufficient funds
    with pytest.raises(ValueError):
        account.withdraw(200)
    assert account.balance == 100

    # Freeze and attempt operation
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(10)
    assert account.balance == 100


def test_multiple_freeze_unfreeze_cycles():
    account = BankAccount(50)
    # Cycle 1
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(10)
    account.unfreeze_account()
    account.deposit(10)
    assert account.balance == 60

    # Cycle 2
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(5)
    account.unfreeze_account()
    account.withdraw(5)
    assert account.balance == 55


def test_deposit_and_withdraw_with_floats():
    account = BankAccount(0.0)
    account.deposit(0.333)
    assert pytest.approx(account.balance, 0.001) == 0.333
    account.withdraw(0.133)
    assert pytest.approx(account.balance, 0.001) == 0.2


def test_deposit_and_withdraw_large_amounts():
    large_amount = 1_000_000_000
    account = BankAccount(large_amount)
    account.deposit(large_amount)
    assert account.balance == large_amount * 2
    account.withdraw(large_amount)
    assert account.balance == large_amount
    account.withdraw(large_amount)
    assert account.balance == 0
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(1)
    assert account.balance == 0