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
