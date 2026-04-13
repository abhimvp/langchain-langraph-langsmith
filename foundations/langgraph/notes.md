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

### Lesson 3: LangSmith Studio

- Go to module-1/studio - we have bunch of python scripts - indicates various graph we are working with in studio.
- we can load this studio directory as a project in LangSmith Studio - To start the local development server(Studio), run the following command in your terminal in the /studio directory each module. - `langgraph dev`

```bash
(lc-foundations)
abhis@Tinku MINGW64 ~/Desktop/langchain-langraph-langsmith/foundations/langgraph/langchain-academy-langgraph/module-1/studio (main)
$ langgraph dev
INFO:langgraph_api.cli:

        Welcome to

╦  ┌─┐┌┐┌┌─┐╔═╗┬─┐┌─┐┌─┐┬ ┬
║  ├─┤││││ ┬║ ╦├┬┘├─┤├─┘├─┤
╩═╝┴ ┴┘└┘└─┘╚═╝┴└─┴ ┴┴  ┴ ┴

- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs

This in-memory server is designed for development and testing.
For production use, please use LangSmith Deployment.
```

- we can see 3 different graphs available in our langsmith studio - which we have configured in `langgraph.json` file & picks up the env keys from .env defined in the studio folder as configured.

### Lesson 4: Chain

Notebook reference: chain.ipynb

- let's build chains - which combines few more concepts - `chat messages` - `chat models` - `binding tools to our LLM` and `executing tool calls` all in LangGraph.
- `Messages`:
  - chat models interact with [messages](https://docs.langchain.com/oss/python/langchain/messages#basic-usage).
  - Langchain supports various types of messages.
    - HumanMessage : message from the user
    - AIMessage : message from the chat model
    - SystemMessage : message for the chat model to instruct behavior
    - ToolMessage : message from a Tool call.
- we can create a list of messages and pass it to the chat model & get an AI Message back out with some content and response metadata.
- `Tools`:
  - which are needed whenever you want a model to control parts of your code or call out to external API's.
  - we can create a function for our model to call as tool and then give it to the chat model with the use of `bind_tools` and pass that function to it.Now the llm has access to awareness of that function.
- Now we want to append the output of chat model to the state, so it preserves a full history of conversation.This motivated the idea of reducer functions.
- when we define our state and LangGraph, we have single key messages and we can actually Annotate it with what we call reducer function, which tells langgraph to actually append to this messages list, when it receives a new message.

### Lesson 5: Router

Notebook reference: router.ipynb

- Now we will add a node that will call our tool & add a conditional edge that lets you look at chat model output and make a decision - route to [tool node](https://reference.langchain.com/python/langgraph/agents) or end it.

### Lesson 6 : Agent

Notebook reference: agent.ipynb

- Self explanatory

### Lesson 7: Agent with Memory

Notebook reference: agent-memory.ipynb

## Module - 2: State and Memory

Memory is a central component in building agentic applications with a high-quality user experience. End users expect agents to remember previous interactions in order to be effective.

- langgraph gives a lot of control over memory in your application.
- explore the concept of memory and see how to add persistence to your graph.
- also the message history can be long, resulting in very high token usage.
- see how we can manage message history to mitigate this problem includes filtering, trimming, summarization to condense long interactions into succinct summaries, also deal with databases for memory.

- **UPTO NOW**

- `act` - let the model call specific tools
- `observe` - pass the tool output back to the model
- `reason` - let the model reason about the tool output to decide what to do next (e.g., call another tool or just respond directly)
- `persist state` - use an in memory checkpointer to support long-running conversations with interruptions

### Lesson 1: State Schema

Notebook Reference: state-schema.ipynb
