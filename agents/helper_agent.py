# agents/helper_agent.py

import json
import subprocess

OLLAMA_MODEL = "llama3:8b"

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


def call_ollama(prompt: str):
    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode("utf-8")

def helper_agent_process(input_text: str):
    prompt = SYSTEM_PROMPT + "\nUser Input:\n" + input_text + "\nJSON Output:"
    response = call_ollama(prompt)

    # Try to extract JSON
    try:
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        json_str = response[json_start:json_end]
        data = json.loads(json_str)
        return data
    except Exception as e:
        return {"error": "Invalid JSON returned by model", "raw_output": response}
