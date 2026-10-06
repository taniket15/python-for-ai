"""
Extra 5 — Classes (self, __init__, exceptions)
==============================================
An optional warm-up for complete Python beginners.

TS / JS  ->  Python
-------------------
    constructor(owner: string, balance = 0)   def __init__(self, owner: str, balance: int = 0):
    this.x                                    self.x
    (every method gets `this` for free)       every method takes `self` as its FIRST parameter
    throw new Error("msg")                    raise ValueError("msg")
    toString()                                def __str__(self) -> str:
    new BankAccount("Ada")                    BankAccount("Ada")     (no `new`)

Run:  uv run python src/extra/ex5_classes.py
"""
from _check import eq, raises, run


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Build a BankAccount:
#   acct = BankAccount("Ada")        # balance starts at 0
#   acct = BankAccount("Ada", 100)   # or with a starting balance
#   acct.deposit(50)                 # adds to the balance
#   acct.withdraw(30)                # subtracts; raise ValueError if there isn't enough money
#   acct.balance                     # the current balance (a plain attribute)
#   str(acct)                        # "Ada: $120"
class BankAccount:
    def __init__(self, owner: str, balance: int = 0):
        raise NotImplementedError  # TODO

    def deposit(self, amount: int) -> None:
        raise NotImplementedError  # TODO

    def withdraw(self, amount: int) -> None:
        raise NotImplementedError  # TODO

    def __str__(self) -> str:
        raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def test_q1_bank_account():
    eq(BankAccount("Ada").balance, 0)
    acct = BankAccount("Ada", 100)
    acct.deposit(50)
    acct.withdraw(30)
    eq(acct.balance, 120)
    eq(str(acct), "Ada: $120")
    raises(ValueError, acct.withdraw, 1000)
    eq(acct.balance, 120)  # a failed withdraw doesn't change the balance


if __name__ == "__main__":
    run(globals())
