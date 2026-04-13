# `@classmethod` in Python — Reference Notes

---

## What is `@classmethod` and how does it differ from a regular method?

A regular method receives the **instance** as its first argument (`self`).
A class method receives the **class itself** as its first argument (`cls`).

```python
class Dog:
    species = "Canis lupus familiaris"

    def bark(self):              # regular — needs an instance
        print(f"{self.name} barks")

    @classmethod
    def describe(cls):           # classmethod — needs only the class
        print(f"All dogs are {cls.species}")

Dog.describe()       # no instance needed — called on the class directly
```

---

## Three types of methods — when to use which

```python
class BankAccount:
    _total = 0

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        BankAccount._total += 1

    # 1. Regular method — logic needs a specific instance's data
    def deposit(self, amount):
        self.balance += amount

    # 2. Class method — logic needs the class, not a specific instance
    #    Most common uses: validators, factory methods
    @classmethod
    def create_zero_balance(cls, owner):
        return cls(owner=owner, balance=0)   # cls = BankAccount

    @classmethod
    def total_accounts(cls):
        return cls._total

    # 3. Static method — utility that belongs here but needs neither
    @staticmethod
    def is_valid_amount(amount):
        return isinstance(amount, (int, float)) and amount >= 0
```

| Method type | First arg | Needs instance? | Common use |
|---|---|---|---|
| Regular | `self` | yes | instance data / behaviour |
| `@classmethod` | `cls` | no | factories, validators, class-level data |
| `@staticmethod` | neither | no | utility functions that belong in the class |

---

## Why Pydantic validators use `@classmethod` specifically

Pydantic runs validators **during object construction** — before the instance fully exists. So there is no `self` to receive yet. `@classmethod` is used because it only needs the class, not a completed instance.

```python
from pydantic import BaseModel, field_validator

class PaymentRequest(BaseModel):
    amount: float
    currency: str

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, v):
        # cls = PaymentRequest class
        # v   = the raw value being validated
        # self does NOT exist yet — instance is still being built
        if v.upper() not in {"INR", "USD", "EUR"}:
            raise ValueError(f"{v} not supported")
        return v.upper()   # coerces "inr" → "INR"
```

Execution order:

```
PaymentRequest(amount=500, currency="inr")
    ↓
Pydantic intercepts — runs normalize_currency(cls, "inr") before building instance
    ↓  returns "INR"
Instance is now created with currency = "INR"
```

---

## Does a classmethod factory automatically call `__init__`?

Yes — because `cls(...)` is literally the same as calling the class directly.

```python
@classmethod
def create_zero_balance(cls, owner):
    return cls(owner=owner, balance=0)
    # cls = BankAccount
    # so this is: BankAccount(owner=owner, balance=0)
    # which triggers __init__ — exactly like a normal call
```

Full execution path:

```
BankAccount.create_zero_balance("Priya")
    ↓
cls(owner="Priya", balance=0)
    ↓  cls is BankAccount
BankAccount(owner="Priya", balance=0)
    ↓  calling a class always triggers __init__
__init__(self, owner="Priya", balance=0) runs
    ↓
self.owner = "Priya"
self.balance = 0
BankAccount._total_accounts += 1    ← increments here, every time
```

Both of these do identical things under the hood:

```python
acc1 = BankAccount("Raj", 1000)                  # direct
acc2 = BankAccount.create_zero_balance("Priya")  # via factory

# Both trigger __init__, both increment _total_accounts
print(BankAccount._total_accounts)   # → 2
```

The factory is not magic — it's just a readable wrapper around a normal class call with pre-set arguments. If you pass a keyword `__init__` doesn't know about, Python raises `TypeError` immediately — the factory has no special privileges.

---

## One-line mental models

- `self` → "I need data from this specific object"
- `cls` → "I need the class itself — no object exists yet (or needed)"
- `@staticmethod` → "This function belongs here logically but needs nothing from the class or instance"
- Pydantic `@classmethod` on validators → "Instance is still being built — `self` doesn't exist yet, so we use `cls`"
- Factory classmethod → "`cls(...)` = calling the class = triggers `__init__` = same as normal construction"
