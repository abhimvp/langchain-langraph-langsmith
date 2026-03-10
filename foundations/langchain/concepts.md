# Concepts

This file is your personal glossary for LangChain. As you encounter new terms and concepts while learning about LangChain, take the time to define them in your own words here. This will help solidify your understanding and create a quick reference for future use.

- `LLMs` are powerful AI tools that can interpret and generate text like humans.
- Models are the reasoning engine of agents. They drive the agent’s decision-making process, determining which tools to call, how to interpret results, and when to provide a final answer.
  - The `quality` and `capabilities` of the model you choose directly impact your agent’s baseline reliability and performance. Different models excel at different tasks - some are better at following complex instructions, others at structured reasoning, and some support larger context windows for handling more information.
- `init_chat_model` : Initialize a chat model from any supported provider using a unified interface.
- `LangChain` provides a prebuilt agent architecture and model integrations to help you get started quickly and seamlessly incorporate LLMs into your agents and applications. [Create-an-agent](https://docs.langchain.com/oss/python/langchain/overview#create-an-agent)
- [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview) are implementations of LangChain agents. If you don’t need these capabilities or would like to customize your own for your agents and autonomous applications, start with LangChain.
- One way to conduce the perceived latency of our system is by [streaming](https://docs.langchain.com/oss/python/langchain/streaming/overview) tokens to the user as they appear, rather than printing all the answer at once.
- `Context engineering` is providing the right information and tools in the right format so the LLM can accomplish a task. This is the number one job of AI Engineers. This lack of “right” context is the number one blocker for more reliable agents, and LangChain’s agent abstractions are uniquely designed to facilitate context engineering.
- [System-prompt](https://docs.langchain.com/oss/python/langchain/context-engineering#system-prompt) - Base instructions from the developer to the LLM.
- refer the docs of [create_agent](https://reference.langchain.com/python/langchain/agents/factory/create_agent) - which gives us an idea of what all arguments we can pass to get the desired output from our agent.
