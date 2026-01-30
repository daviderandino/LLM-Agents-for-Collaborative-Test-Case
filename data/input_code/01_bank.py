class BankAccount:
    def __init__(self, initial_balance=0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.balance = initial_balance
        self.is_active = True

    def deposit(self, amount):
        if not self.is_active:
            raise ValueError("Account is frozen")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if not self.is_active:
            raise ValueError("Account is frozen")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def freeze_account(self):
        self.is_active = False

    def unfreeze_account(self):
        self.is_active = True