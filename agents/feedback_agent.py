# agents/feedback_agent.py

import os
from groq import Groq

# Use Groq cloud API (works on Render)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set!")

client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """
You are a patient-support feedback agent.

Your job:
- Read the user's feedback or question
- Provide a clear, helpful response based on the patient's context
- Improve clarity, tone, or detail if requested
- Never give a medical diagnosis
- Always answer safely and politely
"""


def feedback_agent_process(user_message: str, context: dict):
    """
    context contains:
       prediction, risk, features, reasoning, lifestyle
    """
    import json

    prompt = f"""
Patient Context:
{json.dumps(context, indent=2)}

User Feedback:
{user_message}

Your helpful response:
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message.content
