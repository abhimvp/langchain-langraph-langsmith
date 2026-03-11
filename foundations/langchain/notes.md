# Brief course notes step-by-step for reference later

## module - 1 : Intro to AI agents

- Initialize and interact with a chat model through Langchain - create_agent abstraction
- Then Explore how to add system prompts to your new agent as well as few prompt engineering techniques that we find useful.
- Introduce Agent to Tools
- Add Short term memory to your agents. This will allow your agent to retain memory of previous messages.
- introduce images and audio as input to your agent
- Build a personal assistant chef AGENT - that provides recipes from the internet based on the leftover ingredients you have on hand.

### Lesson 1: Foundation Models

Notebook Reference: 1.1_foundational_models.ipynb

- The Foundation of an agent is the model within it. This is the thinking brain of the system. It's the conductor of Orchestra.
- Initialise and Invoke the model - [Official Docs Reference](https://docs.langchain.com/oss/python/langchain/models#initialize-a-model)
  - we can customize our model - by adjusting a few parameters
    - `temperature` : controls the randomness of the model's output. Higher values (e.g., 0.8) make the output more diverse and creative, while lower values (e.g., 0.2) make it more focused and deterministic.
    - `max_tokens` : limits the maximum number of tokens in the generated response. This can help control the length of the output and manage costs when using API-based models.
    - `timeout`: Maximum time (in seconds) to wait for a response before cancelling the request.
    - `max_retries`: Maximum number of retry attempts for failed requests.
- List of [Chat Model Integrations](https://docs.langchain.com/oss/python/integrations/chat)

Notebook Reference: 1.1_prompting.ipynb

- How can we begin tailoring(Agent) it towards your specific use case? - By using system prompts - we can customize the performance of a chat model
- System prompts are instructions or guidelines provided to a language model to influence its behavior and responses. They can be used to set the context, define the tone, or specify the format of the output.
- Prompt engineering is the process of designing and refining prompts to achieve desired outputs from language models. It involves crafting effective instructions and examples to guide the model's responses.
- Rather than providing the structure to the model within the prompt. we can actually provide it an `output schema`(Using Pydantic - `Base Model`) - pass it to the response_format of create_agent - which will fill out for us by the LLM.

### Lesson 2: Tools

Notebook Reference: 1.2_tools.ipynb

- what seperates the agents from the standard chatbot is it's ability to take actions, perceive the output of those actions, and react accordingly.
- The actions that an agent can take are defined by the tools that we provide it.Tools can allow our agent to access data, execute tasks, even call our agents.
- [Tools](https://docs.langchain.com/oss/python/langchain/tools) are external functions or APIs that an agent can call to perform specific tasks or retrieve information. They allow the agent to interact with the outside world and access resources beyond its own capabilities.

Notebook Reference: 1.2_web_search.ipynb

- Add a web search tool

### Lesson 3: Short-Term memory

Notebook Reference: 1.3_memory.ipynb

- A pretty basic feature we've come to expect from any chatbot we've ever interacted with is it's ability to maintain memory over the lenght of a conversation.
- Short term memory allows our agent to remember previous interactions within a single thread or conversation. This can be crucial for maintaining context and providing more coherent and relevant responses.
- With our langchain agent, we're tracking messages in STATE, which you can think of as the memory of our agent.The problem is the STATE isn't being saved from one run to another, so in effect, our agent's memory is being wiped.
  - We need to somehow save our STATE that the agent can remember previous messages. We do that by using what's a called a `Check Pointer` - [About it](https://docs.langchain.com/oss/python/langchain/short-term-memory#usage).
  - To add short-term memory (thread-level persistence) to an agent, you need to specify a `checkpointer` when `creating` an `agent`.
  - checkpointer saves a snapshot of the state at the end of each run, and then groups it would utter runs with the same `thread id`.
  - The checkpointer we use is imported from langGraph library - called InMemorySaver , we initialize our agent with it. see the code example below.

```py
# LangChain’s agent manages short-term memory as a part of your agent’s state.

# By storing these in the graph’s state, the agent can access the full context for a given conversation while maintaining separation between different threads.

# State is persisted to a database (or memory) using a checkpointer so the thread can be resumed at any time.

# Short-term memory updates when the agent is invoked or a step (like a tool call) is completed, and the state is read at the start of each step.

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


agent = create_agent(
    "gpt-5",
    tools=[get_user_info],
    checkpointer=InMemorySaver(),
)

agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    {"configurable": {"thread_id": "1"}},
)
```

- We define our `thread ID` so that we group these checkpoints of our state together.
- **Now invoke the agent using this common thread id** - it retains the memory of our previous conversation and appended it to it's list of messages. So we now have an agent with memory.
- **In [production](https://docs.langchain.com/oss/python/langchain/short-term-memory#in-production), use a checkpointer backed by a database** - `pip install langgraph-checkpoint-postgres`

- The documentation all the different ways to manage memory and provide/make the context neccessary available to LLM - we need to figure out which needs to be used depending on our use-case.

### Lesson 4: Multimodal Messages

Notebook Reference: 1.4_multimodal_messages.ipynb

- These days the LLMs doesn't take inputs only from text but also from other models which can take inputs and providing outputs in image, audio or video formats.
- In this lesson, we'll explore how to provide image and audio input to our agents - so they can see and hear the world around them.
- [choosing a model](https://developers.openai.com/api/docs/models)
- First things first, we'll be encoding our image and audio files in base64.
- About [multimodal](https://docs.langchain.com/oss/python/langchain/messages#multimodal).
- We can also provide the model with a `multimodal output schema` - which is a pydantic model that specifies the expected format of the output, including any multimodal components. The model will then generate responses that conform to this schema, allowing us to easily parse and utilize the multimodal data in our applications.

### Lesson 5: Personal Chef(Project)

Notebook Reference: 1.5_personal_chef.ipynb

## module - 2 : Advanced Agent

- Learn About MCP, how to provide agent with runtime context and customize it's state, so it keeps track of more than just messages in memory.
- Learn about multi-agent systems - to allow applications to handle longer and larger tasks.

### Lesson 1: Model Context Protocol

Notebook Reference: 2.1_mcp.ipynb

- [langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters) enables agents to use tools defined across one or more MCP servers.
- MCP? - model context protocol - defined by Anthropic - An Open protoco that standardizes how your LLM applications connect to and work with your tools and data sources.
- The MCP Host hosts an MCP Client, which communicates to the MCP Server. IN our case, the MCP Host is AI Agent.
- The MCP Servers can expose `Tools`, `Resources` like read-only data or `Prompt`-Templates to the client.
- **Build our Own MCP Server from scratch** - `module-2/resources/2.1_mcp_server.py` -
- MCP Servers - 3rd party - [ones](https://mcp.so/servers)
- we have seen how we can connect 3rd party mcp servers and access it's tool and query our questions.
- travel agent mcp & also understand the mcp [transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) & [refer this](https://docs.langchain.com/oss/python/langchain/mcp#transports)

### Lesson 2: Context and State

Notebook Reference: 2.2_runtime_context.ipynb
Notebook Reference: 2.2_state.ipynb

- we can create a context schema to fill in and pass to the agent, which the agent can draw from to inform it's actions - but the context can't be passed to the model directly
- instead it's passed to the tool cause in an object called tool runtime. [More About it](https://docs.langchain.com/oss/python/langchain/tools#access-context)
- we therefore need to make a tool call for our agent to be able to access that information
- context is immutable - means the agent can't update or change itself - may the agent needs to learn what language and where i'm fom during conversation itself - then we can do that using [AGENTS STATE](https://docs.langchain.com/oss/python/langchain/tools#short-term-memory-state).
