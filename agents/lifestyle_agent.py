# agents/lifestyle_agent.py

import os
from groq import Groq

# Load API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set!")

client = Groq(api_key=GROQ_API_KEY)

# Fast, cheap, best for recommendations
MODEL_NAME = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """
You are a heart-health lifestyle assistant.

Your responsibilities:
- Suggest heart-healthy diet items
- Recommend beginner-friendly exercises
- Give stress and sleep improvement tips
- Offer safe lifestyle improvements
- Avoid any medical diagnosis
- Use simple, encouraging language
"""

def lifestyle_recommendations(features: dict, risk: float):
    """
    Creates diet, exercise, and lifestyle guidance for heart disease risk reduction.
    """

    user_message = f"""
The patient's risk is {risk}%.

Their health features:
{features}

Provide:
1. 5 heart-healthy diet recommendations  
2. 5 safe exercise suggestions  
3. Stress reduction tips  
4. Sleep improvement advice  
5. Foods and habits to avoid  
6. Simple steps the patient can start today  
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]
    )
    print("DEBUG RESPONSE:", response.choices)  # Temporary debug
    
    return response.choices[0].message.content
