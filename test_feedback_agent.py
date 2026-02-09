# test_feedback_agent.py

from agents.feedback_agent import feedback_agent_process

context = {
    "prediction": 1,
    "risk": 72.5,
    "features": {"Age": 55, "Cholesterol": 250, "MaxHR": 120},
    "reasoning": "This means the patient has elevated risk...",
    "lifestyle": "Eat more vegetables and walk daily..."
}

print("\n--- FEEDBACK AGENT TEST START ---\n")

user_question = "Can you explain in simpler words why my cholesterol is dangerous?"
out = feedback_agent_process(user_question, context)

print(out)
