import os
from dotenv import load_dotenv
import openai
from langsmith.wrappers import wrap_openai
from langsmith import traceable

load_dotenv()  # This pulls the variables from your .env file

client = wrap_openai(openai.Client())  # log every OpenAI call automatically


@traceable(run_type="tool")  # trace this as a tool span
def get_context(question: str) -> str:
    # In a real app, this would query a knowledge base or vector store
    return "LangSmith traces are stored for 14 days on the Developer plan."


@traceable  # capture the full pipeline as a single trace
def assistant(question: str) -> str:
    context = get_context(question)
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Replaced gpt-5.2 with the budget-friendly version
        messages=[
            {
                "role": "system",
                "content": f"Answer using the context below.\n\nContext: {context}",
            },
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(assistant("How long are LangSmith traces stored?"))
