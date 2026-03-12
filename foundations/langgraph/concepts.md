# Concepts

- LangGraph is very low-level, and focused entirely on **agent orchestration**
- LangGraph is an orchestration framework for complex agentic systems and is more low-level and controllable than LangChain agents. On the other hand, LangChain provides a standard interface to interact with models and other components, useful for straight-forward chains and retrieval flows.
- About [`TypedDict`](https://typing.python.org/en/latest/spec/typeddict.html): defines a structural type for dictionaries with a fixed set of string keys and specific value types, enabling enhanced static type checking in Python. It ensures that dictionary instances contain required keys and that their values match defined types.
  - Alternative to `dataclass`: Ideal for JSON-like data structures where you need structural validation without the overhead of creating objects.

```py
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int
    is_active: bool  # Optional: Default to total=True (all keys required)

# Usage
user1: User = {"name": "Alice", "age": 30, "is_active": True}
# user2: User = {"name": "Bob"}  # Error: Missing keys

```

- About `Literal` : The [Literal](https://typing.python.org/en/latest/spec/literal.html) type is a powerful tool for static type checking, as it restricts the possible values a variable can have to a predefined set of literals (e.g., specific strings, integers, or boolean values).

```python
from typing import Literal

# Define a type alias for possible game modes
GameMode = Literal["easy", "medium", "hard"]

def start_game(mode: GameMode) -> None:
    if mode == "easy":
        print("Starting easy game...")
    elif mode == "medium":
        print("Starting medium game...")
    elif mode == "hard":
        print("Starting hard game...")

start_game("easy")      # Valid
# start_game("extreme") # Type checker error: "extreme" is not a valid literal

```

- LangGraph - [GRAPH API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [`Runnable`](https://reference.langchain.com/python/langchain-core/runnables/base/Runnable) : A unit of work that can be invoked, batched, streamed, transformed and composed.
  - Key Methods:
    - invoke/ainvoke: Transforms a single input into an output.
    - batch/abatch: Efficiently transforms multiple inputs into outputs.
    - stream/astream: Streams output from a single input as it's produced.
    - astream_log: Streams output and selected intermediate results from an input.

- About [LangSmith studio](https://docs.langchain.com/langsmith/studio#local-development-server) - which helps us to visualize our graphs and see the state being transformed at each node and the state.
  - Studio is a specialized agent IDE that enables visualization, interaction, and debugging of agentic systems that implement the Agent Server API protocol.
- Did run our simple_graph in Langsmith Studio - Go to studio folder and run `langgraph dev`

## LangGraph: Why use `Annotated` and `add_messages`?

In LangGraph, the `State` is the single source of truth. By default, LangGraph **overwrites** the value of a key when a node returns a new value. To change this behavior (e.g., to append to a chat history), we use `Annotated`.

### 1. The Anatomy of the Type Hint

```python
messages: Annotated[list[AnyMessage], add_messages]

```

- **The Type (`list[AnyMessage]`)**: Tells Python/IDE that this field holds a list of messages.
- **The Reducer (`add_messages`)**: Tells LangGraph **how** to update this field. This is the "instruction manual" for the state.

---

### 2. Why not just `append()` manually?

If you try to manually manage the list inside your nodes instead of using a reducer, you run into three major issues:

#### A. The Overwrite Trap

Without a reducer, LangGraph performs a simple assignment: `state['messages'] = new_value`.

- **Current State:** `[Msg1, Msg2]`
- **Node Returns:** `{"messages": [Msg3]}`
- **Result:** `[Msg3]` (**Msg1 and Msg2 are deleted!**)
  With `Annotated`, LangGraph sees the `add_messages` instruction and performs: `state['messages'] = add_messages(current, new)`.

#### B. The Parallel Conflict (Race Conditions)

In complex graphs, two nodes might run at the same time.

- **Node A** finishes and returns `[Msg_A]`.
- **Node B** finishes and returns `[Msg_B]`.
- **Without Reducer:** The last node to finish wins; the other message is lost.
- **With Reducer:** LangGraph queues the updates and runs the reducer for both, ensuring both `Msg_A` and `Msg_B` are preserved.

#### C. Beyond Simple Appending

The `add_messages` reducer is smarter than a simple `.append()`. It checks the **ID** of messages:

- If a message has a **new ID**, it is appended.
- If a message has an **existing ID**, it replaces the old one (useful for "editing" or streaming status updates).

---

### 3. Comparison Table

| Feature                 | Default (No `Annotated`)         | With `Annotated` + `add_messages`  |
| ----------------------- | -------------------------------- | ---------------------------------- |
| **Logic**               | `State = New`                    | `State = Reducer(Old, New)`        |
| **Action**              | **Overwrite**                    | **Merge / Append**                 |
| **Node Responsibility** | Must return the _entire_ history | Only returns the _new_ messages    |
| **Best For**            | Status flags, settings, counters | Chat history, logs, document lists |

---

### Summary for Reference

> **`Annotated`** is the "metadata tag" that tells LangGraph: _"Don't just replace this variable; use this specific function (`add_messages`) to merge the update into the existing data."_

Would you like me to show you how to write a **custom reducer** function if you ever need logic more specific than just adding messages?
