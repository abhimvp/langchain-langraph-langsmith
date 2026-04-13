# LangGraph & Python OOP — Concepts Reference

> A personal reference built from first-principles learning.
> Format: concept → question that led to it → clear answer with code where needed.

---

## Table of Contents

1. [The Runnable Protocol](#1-the-runnable-protocol)
2. [RunnableLambda & RunnableGenerator](#2-runnablelambda--runnablegenerator)
3. [The Adapter Pattern — why that word](#3-the-adapter-pattern--why-that-word)
4. [Python Callable — what it really means](#4-python-callable--what-it-really-means)
5. [LangGraph Node Arguments — state, config, runtime](#5-langgraph-node-arguments--state-config-runtime)
6. [OOP Concepts in Practice](#6-oop-concepts-in-practice)
7. [TypedDict vs dataclass vs Pydantic BaseModel](#7-typeddict-vs-dataclass-vs-pydantic-basemodel)
8. [Graph State — which one to pick and why](#8-graph-state--which-one-to-pick-and-why)
9. [The Big Picture — how layers connect](#9-the-big-picture--how-layers-connect)

---

## 1. The Runnable Protocol

**What is the Runnable protocol and why does it exist?**

`Runnable` is an abstract base class in LangChain that defines a universal interface every composable unit must implement. Its purpose is to make every piece of the ecosystem — LLMs, retrievers, prompts, your own functions — speak the same language so they can be composed together.

Methods it defines:

- `invoke(input)` — run once, return result
- `batch(inputs)` — run on a list of inputs
- `stream(input)` — yield output chunks
- `ainvoke`, `abatch`, `astream` — async versions of all three

**Why does this matter?**

Because of this shared interface, you can chain any Runnable with any other using the `|` pipe operator:

```python
chain = prompt | llm | output_parser
# prompt, llm, and output_parser are all Runnables
# they compose because they all honour the same interface
```

**Is Runnable a class or an interface?**

In Python terms it's an Abstract Base Class (ABC). In spirit it's an interface — it defines the contract, not the implementation. Subclasses must fill in the actual logic.

---

## 2. RunnableLambda & RunnableGenerator

**What is RunnableLambda?**

A wrapper that promotes any Python callable (function, lambda, class with `__call__`) into a full Runnable. LangGraph does this automatically when you call `add_node()`.

What it adds to your plain function for free:

- `batch()` — run on multiple inputs without you writing the loop
- `ainvoke()` / `abatch()` — async support even if your function is sync
- Tracing — every call emits a span to LangSmith automatically
- Streaming hooks — feeds into the graph's event stream

```python
from langchain_core.runnables import RunnableLambda

def double(x: int) -> int:
    return x * 2

r = RunnableLambda(double)
r.invoke(5)         # → 10
r.batch([1, 2, 3])  # → [2, 4, 6]   ← you didn't write this
await r.ainvoke(5)  # → 10           ← you didn't write this either
```

**When does LangGraph wrap my function automatically?**

Always — when you call `graph.add_node("name", my_function)`. You never call `RunnableLambda` yourself in LangGraph. It happens under the hood.

**What is RunnableGenerator and when should I use it instead?**

Use `RunnableGenerator` when your node is a generator function (uses `yield`). It lets output flow chunk-by-chunk to callers using `.stream()`. If your node just `return`s a value, `RunnableLambda` is the right fit.

| | `RunnableLambda` | `RunnableGenerator` |
|---|---|---|
| Function type | regular `def` or `async def` | generator (`yield`) |
| Output | single return value | chunks streamed progressively |
| Use case | most nodes | nodes that stream tokens/events |

---

## 3. The Adapter Pattern — why that word

**Why do people call RunnableLambda an "adapter"?**

The word comes from a classic OOP design pattern called the **Adapter Pattern**: *convert the interface of something into the interface a client expects.*

Real-world analogy: a plug adapter. Your Indian charger doesn't fit a UK socket. The plastic adapter in between doesn't change what the charger does — it just gives it the right shape to plug in.

`RunnableLambda` is that adapter:

- Your plain Python function = the Indian charger (works fine, wrong shape)
- LangGraph's graph engine = the UK socket (expects a Runnable interface)
- `RunnableLambda` = the adapter (wraps your function, makes it fit)

Your function doesn't change at all. It just gets a new outer shell with `invoke()`, `batch()`, `stream()`.

---

## 4. Python Callable — what it really means

**Is "callable" just another word for function?**

No. In Python, a callable is anything you can put `()` after and call. That includes three things:

```python
# 1. A regular function
def double(x):
    return x * 2

# 2. A lambda
triple = lambda x: x * 3

# 3. A class instance that defines __call__
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):        # ← this makes it callable
        return x * self.factor

times4 = Multiplier(4)
times4(10)   # → 40   called like a function
```

`RunnableLambda` accepts all three. When docs say "wraps a Python callable" they mean any of the above.

**What is `__call__` and why does it matter?**

It's a Python dunder method (double-underscore method). When you define `__call__` on a class, instances of that class become callable — you can use `()` on them as if they were functions. This is the OOP mechanism behind "callable objects."

---

## 5. LangGraph Node Arguments — state, config, runtime

**What are the three arguments LangGraph can inject into a node?**

LangGraph inspects your function's signature using reflection and injects only what you declared.

```python
def plain_node(state: State):
    # minimum — just the state
    return {"result": "done"}

def node_with_config(state: State, config: RunnableConfig):
    # config carries thread_id, tags, metadata
    thread_id = config.get("configurable", {}).get("thread_id")
    return {"result": thread_id}

def node_with_runtime(state: State, runtime: Runtime[Context]):
    # runtime carries store, stream_writer, execution_info, server_info
    print(runtime.context.user_id)
    return {"result": "done"}
```

**What is each argument for?**

| Argument | Type | Contains | When to use it |
|---|---|---|---|
| `state` | your `TypedDict` / `dataclass` / `BaseModel` | shared graph memory | always — every node gets this |
| `config` | `RunnableConfig` | `thread_id`, tags, metadata, callbacks | when you need run-level config or to pass config to an LLM call |
| `runtime` | `Runtime` | `store`, `stream_writer`, `execution_info`, `server_info`, `context` | advanced — cross-thread memory, streaming directly, execution metadata |

---

## 6. OOP Concepts in Practice

**What is an Abstract Class / Interface?**

A class that defines *what methods must exist* but doesn't implement them. You cannot instantiate it directly — Python raises `TypeError`. Subclasses must fill in every abstract method.

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):

    @abstractmethod
    def charge(self, amount: float) -> dict:
        pass   # no implementation — subclass must define this

    def validate(self, amount: float) -> bool:
        return amount > 0   # this IS implemented — shared by all subclasses

# PaymentGateway()  ← TypeError, can't instantiate abstract class
```

**What is Inheritance?**

When a class derives from another class and gets its interface plus any implemented methods for free. The subclass must implement any abstract methods.

```python
class StripeGateway(PaymentGateway):   # inherits from PaymentGateway

    def charge(self, amount: float) -> dict:
        self.validate(amount)    # ← using inherited method
        return {"status": "success", "gateway": "stripe"}
```

**What is Encapsulation?**

Bundling data and the methods that operate on it into one unit, and controlling access to internal details.

```python
@dataclass
class PaymentDetails:
    amount: float
    _raw_card: str = None     # single _ = "don't touch directly" (convention)
    __cvv: str = None         # double __ = Python mangles name, harder to access

    def masked_card(self):
        return f"****{self._raw_card[-4:]}"   # controlled exposure
```

Python's privacy levels:

| Syntax | Meaning | Actually blocked? |
|---|---|---|
| `card` | public | no — anyone reads/writes |
| `_card` | protected | no — convention only, accessible |
| `__card` | private | mostly — Python renames to `_ClassName__card` |

> Python's philosophy: "we are all consenting adults." It signals intent but doesn't enforce like Java's `private`.

**What is Polymorphism?**

The same code working on many different types because they all honour the same interface. You write code against the abstraction, not the concrete class.

```python
class CheckoutService:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway   # accepts ANY PaymentGateway subclass

    def process(self, amount: float):
        return self.gateway.charge(amount)   # works for Stripe, Razorpay, anything

# Same CheckoutService, different gateway — code never changes
CheckoutService(StripeGateway()).process(500)
CheckoutService(RazorpayGateway()).process(500)
CheckoutService(OldBankAdapter()).process(500)
```

**What is the Adapter Pattern?**

A structural pattern where you wrap an incompatible class to make it fit an interface, without modifying the original.

```python
class OldBankSDK:                        # old system, can't change it
    def make_payment(self, rupees, email): ...
    def cancel_payment(self, ref): ...    # returns 1/0, not True/False

class OldBankAdapter(PaymentGateway):    # adapter: wraps old, looks like new
    def __init__(self):
        self._sdk = OldBankSDK()

    def charge(self, amount):
        ref = self._sdk.make_payment(amount, "")   # translates call
        return {"status": "success", "transaction_id": ref}

    def refund(self, txn_id, amount):
        return self._sdk.cancel_payment(txn_id) == 1   # translates return type
```

---

## 7. TypedDict vs dataclass vs Pydantic BaseModel

**Why do all three exist — what problem does each solve?**

All three give structure to data. A plain Python dict has no shape — wrong keys, wrong types, Python doesn't care until things break at runtime. These three are three different ways to impose structure, each with different trade-offs.

**When to use `TypedDict`**

- Data stays inside your application — you control it
- It's a dict being passed around — no methods needed
- Performance matters — zero runtime overhead, it IS a plain dict at runtime
- Default choice for LangGraph graph state

```python
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]   # Annotated attaches reducer
    user_id: str
    step_count: int
```

**When to use `dataclass`**

- You need an object with both data AND methods
- You need clean default values
- Internal application objects — config, context, settings
- LangGraph runtime `Context` — the documented way

```python
from dataclasses import dataclass, field

@dataclass
class UserContext:
    user_id: str
    org_id: str
    is_premium: bool = False
    flags: list = field(default_factory=list)   # mutable default — needs field()

    def can_access(self, feature: str) -> bool:
        return feature in self.flags or self.is_premium
```

> `@dataclass` auto-generates `__init__`, `__repr__`, `__eq__` — no boilerplate.
> Use `field(default_factory=list)` for mutable defaults (list, dict) — never `flags: list = []`.

**When to use `Pydantic BaseModel`**

- Data comes from outside your system — API requests, JSON, user input, env vars
- You need validation with clear error messages
- You need coercion — e.g. `"inr"` → `"INR"`, `"4111 1111"` → `"41111111"`
- FastAPI endpoint bodies — FastAPI uses Pydantic natively
- LLM structured output parsing

```python
from pydantic import BaseModel, field_validator

class PaymentRequest(BaseModel):
    amount: float
    currency: str

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, v):
        allowed = {"INR", "USD", "EUR"}
        if v.upper() not in allowed:
            raise ValueError(f"{v} not supported")
        return v.upper()   # coerces to uppercase automatically
```

**Quick comparison table**

| | `TypedDict` | `dataclass` | `Pydantic BaseModel` |
|---|---|---|---|
| Runtime overhead | zero — it's a dict | minimal | higher — validates on every set |
| Default values | no | yes, clean | yes |
| Methods | no | yes | yes |
| Validation | no | no | yes — with clear errors |
| Coercion | no | no | yes |
| Best for | internal dict-passing (graph state) | internal objects with behaviour | external data boundaries |

---

## 8. Graph State — which one to pick and why

**What does the LangGraph documentation recommend?**

- `TypedDict` — default. Use this first.
- `dataclass` — upgrade to this when you need default values on state fields.
- `Pydantic BaseModel` — use only when you genuinely need validation inside the graph. It's slower.

**Why is TypedDict the default for graph state specifically?**

LangGraph merges partial dict updates from node outputs on every step. With a long-running agent this can be hundreds of merges. `TypedDict` is a plain dict at runtime — zero overhead per merge. `Pydantic` validates on every update, which adds up.

**When does Pydantic actually earn its cost in a graph?**

- Your nodes call LLMs or external APIs — a 2-second API call makes Pydantic's validation cost negligible
- Multiple nodes write to the same state key and you need to catch bad values immediately
- State has nested complex objects that need recursive validation

**What's the smart production pattern?**

Use each type at the layer it fits best — don't force one type everywhere:

```python
# Pydantic at the API boundary — catch bad input before it enters the graph
class ChatRequest(BaseModel):
    user_id: str
    message: str

# TypedDict for graph state — fast internal execution
class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str

# dataclass for runtime context injected into nodes
@dataclass
class UserContext:
    user_id: str
    is_premium: bool = False

# Flow:
# HTTP POST → Pydantic validates → TypedDict runs fast inside graph
# → Pydantic validates LLM output if needed → return response
```

---

## 9. The Big Picture — how layers connect

**How does LangGraph/LangChain relate to Python OOP concepts?**

It's a direct, 1-to-1 mapping:

| OOP concept | LangChain/LangGraph equivalent |
|---|---|
| Abstract class / Interface | `Runnable` — defines the contract |
| Inheritance | `RunnableLambda(Runnable)` — inherits and implements |
| Adapter pattern | `RunnableLambda(your_fn)` — wraps plain function to fit the interface |
| Callable / `__call__` | any `def`, `lambda`, or class with `__call__` LangGraph accepts |
| Abstraction / Framework | `StateGraph`, `add_node`, `compile()` — hides the Runnable machinery |

**What is the overall layering in a production LangGraph application?**

```
You write:          graph.invoke({"messages": [...]})
                    ↓
LangGraph layer:    routes nodes, merges state, handles checkpointing
                    ↓
Runnable layer:     RunnableLambda wraps your functions, adds batch/async/tracing
                    ↓
Python runtime:     manages memory, executes compiled code
                    ↓
Operating system:   schedules CPU, manages I/O
                    ↓
Hardware:           transistors flipping on and off
```

Every layer hides the chaos below it. You write clean Python. Everything underneath keeps running without you needing to know it exists. This is what abstraction means in practice — not just in textbooks.

**Why did the LangChain team build it this way?**

So that an LLM, a retriever, a prompt template, and your custom function can all be treated identically by the framework. Swap Stripe for Razorpay in the payment example — the checkout service never changed. Same idea: swap one LLM node for another, the graph executor never changes. The protocol is the glue.

---

*Built from a learning session covering: Runnable protocol, RunnableLambda/Generator, Adapter pattern, Python callables, OOP fundamentals (abstract classes, inheritance, encapsulation, polymorphism, adapter), TypedDict vs dataclass vs Pydantic, and LangGraph graph state design decisions.*
