# Brief course notes step by step to refer later

## Module - 1: Introduction

- Let's look into agents & see why building custom agents - with domain specific workflows and focus on high reliability - is really important.
- see how langgraph makes it easy to build custom agents.
- langGraph models agent workflows as graphs.
- look into langgraph's core abstractions State, Node and Edges.
- Build graphs around chat models.
- Discuss tools and messages which are core components of workflows that use chat models.
- see looping in workflows and see how this enables the general `ReAct` agent architecture.
- add memory to it.

- Lesson 1: Motivation

### Lesson 2: Simple Graph - simple-graph.ipynb

- First thing to do when defining a `graph` is define the `state` of the graph.
- `state` is just the object that we pass between the `nodes` and `edges` of our graph.
- Defined `state` as simple dictionary using `TypedDict` - it has one key `graph_state`.
- next we need to define our `nodes` which are just python functions and each of the nodes takes in `state`. we can extract the value of `graph_state` key & each node will override the value of prior state value.
- `edges` are how we connect the nodes.
- we will have a `normal_edge` between start and node_1.
- `conditional_edges` are used want to optionally route between nodes 2 and 3.
  - it's implemented as a function that returns the next node to visit based upon some logic.
- we build the graph using the `StateGraph` - `from langgraph.graph import StateGraph`
- Initialize the Graph with the `State` we defined. `builder = StateGraph(State)`
- Then add Nodes to the graph - `builder.add_node("node_1",node_1)` - The "node_1" is the name of the node and node_1 is the function we defined.
- Now we define the logic:
  - we go from START to node_1 -> `builder.add_edge(START,"node_1")` - this is the starting node of our graph - `Normal edge`
  - then set a `conditional edge` between node 1 & 2-3 -> `builder.add_conditional_edges("node_1",decide_mood) - decide_mood is a conditional edge which has some logic that returns which node to go next.
  - then add both node 2 and 3 to END from conditional edge - `builder.add_edge("node_2",END)`
- Then we compile our graph - `graph = builder.compile()`
- we can display the graph as well.

- _In short: nodes do the work, edges tell what to do next._

- Now the graph implements [`runnable`](https://reference.langchain.com/python/langchain-core/runnables/base/Runnable) protocol - a standard way to execute langchain components. Provide different methods on how we want to run our graphs like invoke, stream ...etc
