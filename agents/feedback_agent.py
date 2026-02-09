# agents/feedback_agent.py

import subprocess
import json

# FIXED MODEL NAME — this model exists on your system
FEEDBACK_MODEL = "llama3.1:8b"

SYSTEM_PROMPT = """
You are a patient-support feedback agent.

Your job:
- Read the user's feedback or question
- Provide a clear, helpful response based on the patient's context
- Improve clarity, tone, or detail if requested
- Never give a medical diagnosis
- Always answer safely and politely
"""

def call_ollama(prompt: str):
    result = subprocess.run(
        ["ollama", "run", FEEDBACK_MODEL],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode("utf-8")

def feedback_agent_process(user_message: str, context: dict):
    """
    context contains:
       prediction, risk, features, reasoning, lifestyle
    """

    prompt = f"""
{SYSTEM_PROMPT}

Patient Context:
{json.dumps(context, indent=2)}

User Feedback:
{user_message}

Your helpful response:
"""

    response = call_ollama(prompt)
    return response.strip()
