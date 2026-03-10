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
