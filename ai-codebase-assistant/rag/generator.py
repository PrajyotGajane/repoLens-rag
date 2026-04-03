from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(query: str, context: str):
    print("\n[TRACE] Generating answer...\n")

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a senior software engineer analyzing a codebase."
            },
            {
                "role": "user",
                "content": f"""
QUESTION:
{query}

CONTEXT:
{context}
"""
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

def generate_answer_stream(query: str, context: str):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        stream=True,
        messages=[
            {"role": "system", "content": "You are a senior software engineer analyzing a codebase."},
            {
                "role": "user",
                "content": f"""
QUESTION:
{query}

CONTEXT:
{context}
"""
            }
        ]
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content