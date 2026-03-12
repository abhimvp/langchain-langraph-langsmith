# Foundation: Introduction to LangGraph - Python

- One type of LLM Application we can build is Agent.
- You can create agents by allowing an LLM to determine the control flow of application.
- Agents can automate a wide range of tasks that were previously impossible.
- You might need an Agent to always call a specific tool first or to use different prompts based on it's state.

- **LangGraph** - A framework for building agentic and multi-agent applications.It's core design philosophy is to help developers add better precision and more control into agentic workflows making them suitable for the complexity of real-world systems.

- Module 1 - Fundamentals of Agents - Introduce LangGraph and build a few generalist agent architectures.
- Module 2 - we'll show how to work with messages to exchange information within your agent & how to use memory to save your agents internal state.
- Module 3 - we'll cover how to add human in the loop to approve specific actions or review your agent's work.
- Module 4 - Build this all into a research assistant that can produce customizable knowledge outputs like reports or wikis or summaries using various type of tools we give it, such as web search or documents that are relevant to your application.
  - we'll build this all using LangGraph's features for parallelization and human review.

- Added [notebooks](https://github.com/langchain-ai/langchain-academy) into langchain-academy-main.

```bash
abhis@Tinku MINGW64 ~/Desktop/langchain-langraph-langsmith/foundations/langgraph/langchain-academy-langgraph (main)
$ uv venv langgraph-foundations
Using CPython 3.12.7
Creating virtual environment at: langgraph-foundations
Activate with: source langgraph-foundations/Scripts/activate

abhis@Tinku MINGW64 ~/Desktop/langchain-langraph-langsmith/foundations/langgraph/langchain-academy-langgraph (main)
$ source langgraph-foundations/Scripts/activate

(langgraph-foundations)
abhis@Tinku MINGW64 ~/Desktop/langchain-langraph-langsmith/foundations/langgraph/langchain-academy-langgraph (main)
$ uv pip install -r requirements.txt
Using Python 3.12.7 environment at: langgraph-foundations
Resolved 177 packages in 7.40s
      Built wikipedia==1.4.0
Prepared 20 packages in 3.39s
Installed 177 packages in 3.90s

(langgraph-foundations) 
abhis@Tinku MINGW64 ~/Desktop/langchain-langraph-langsmith/foundations/langgraph/langchain-academy-langgraph (main)
$ cp example.env .env
```
