# Solutions for ex5_classes.py
# Test them with:  uv run python src/extra/ex5_classes.py --solution


class BankAccount:
    def __init__(self, owner: str, balance: int = 0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: int) -> None:
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        if amount > self.balance:
            raise ValueError("not enough money")
        self.balance -= amount

    def __str__(self) -> str:
        return f"{self.owner}: ${self.balance}"
