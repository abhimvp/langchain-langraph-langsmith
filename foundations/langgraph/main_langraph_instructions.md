# when building langgraph workflows/graphs: follow these rules mainly: Best practices

- [Use pydantic models for graph state](https://docs.langchain.com/oss/python/langgraph/use-graph-api#use-pydantic-models-for-graph-state)
  - `Note`: The main documented way to specify the schema of a graph is by using a `TypedDict`. If you want to provide default values in your state, use a `dataclass`. We also support using a Pydantic `BaseModel` as your graph state if you want recursive data validation (though note that Pydantic is less performant than a TypedDict or dataclass).

- All About LangGraph - [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api#graphs) - LangGraph models agent workflows as graphs - LangGraph’s underlying graph algorithm uses message passing to define a general program. When a Node completes its operation, it sends messages along one or more edges to other node(s). These recipient nodes then execute their functions, pass the resulting messages to the next set of nodes, and the process continues.

- nodes do the work, edges tell what to do next.

- To build your graph, you first define the `state`, you then add `nodes` and `edges`, and then you `compile` it.
  - You MUST compile your graph before you can use it - `graph = graph_builder.compile(...)`
  - have an idea about serialization/deserialization of Langchain - use dot notation to access message attributes.

- LangGraph has a pre-built `MessagesState`!

`MessagesState` is defined:

- With a pre-build single `messages` key
- This is a list of `AnyMessage` objects
- It uses the `add_messages` [reducer](https://docs.langchain.com/oss/python/langgraph/graph-api#reducers)
- We'll usually use [MessagesState](https://docs.langchain.com/oss/python/langgraph/graph-api#messagesstate) because it is less verbose than defining a custom `TypedDict`, as shown above.

```python
from langgraph.graph import MessagesState

class MessagesState(MessagesState):
    # Add any keys needed beyond messages, which is pre-built 
    pass
```

- Typically, there is more state to track than just messages, so we see people subclass this state and add more fields, like:

```python
from langgraph.graph import MessagesState

class State(MessagesState):
    documents: list[str]
```

- In LangGraph, `nodes` are Python functions (either synchronous or asynchronous) that accept the following arguments:
  - state —The state of the graph
  - config —A `RunnableConfig` object that contains configuration information like `thread_id` and `tracing` information like `tags`
  - runtime —A `Runtime` object that contains runtime context and other information like `store`, `stream_writer`, `execution_info`, and `server_info`

- Behind the scenes, functions are converted to `RunnableLambda`, which add batch and async support to your function, along with native tracing and debugging.
If you add a node to a graph without specifying a name, it will be given a default name equivalent to the function name.
