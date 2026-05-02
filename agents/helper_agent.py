# agents/helper_agent.py

import os
import json
from groq import Groq

# Use Groq cloud API (works on Render)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set!")

client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """
You are a medical input-processing agent.

STRICT RULES:
- You MUST output ONLY the required JSON.
- Every field MUST have a VALID value.
- NO extra words, no comments, no explanations.
- NEVER output text like "Fine", "Normal", "Maybe".
- FastingBS MUST be 0 or 1 ONLY.
- ExerciseAngina MUST be "Y" or "N".
- ChestPainType must be one of: "ATA", "NAP", "TA".
- RestingECG must be "Normal" or "ST".
- ST_Slope must be "Up" or "Flat".

MANDATORY JSON FORMAT:
{
  "Age": 0,
  "Sex": "M",
  "ChestPainType": "ATA",
  "RestingBP": 0,
  "Cholesterol": 0,
  "FastingBS": 0,
  "RestingECG": "Normal",
  "MaxHR": 0,
  "ExerciseAngina": "N",
  "Oldpeak": 0.0,
  "ST_Slope": "Up"
}

Return ONLY the JSON. No extra text.
"""


def helper_agent_process(input_text: str):
    prompt = SYSTEM_PROMPT + "\nUser Input:\n" + input_text + "\nJSON Output:"

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"User Input:\n{input_text}\nJSON Output:"},
        ]
    )

    raw = response.choices[0].message.content

    # Try to extract JSON
    try:
        json_start = raw.find("{")
        json_end = raw.rfind("}") + 1
        json_str = raw[json_start:json_end]
        data = json.loads(json_str)
        return data
    except Exception as e:
        return {"error": "Invalid JSON returned by model", "raw_output": raw}
