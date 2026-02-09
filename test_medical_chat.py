from agents.reasoning_agent import medical_chat

context = {
    "prediction": 1,
    "risk": 82.7,
    "features": {
        "Age": 55,
        "Sex": "M",
        "Cholesterol": 250,
        "ExerciseAngina": "Y"
    }
}

question = "How dangerous is exercise-induced angina?"

print(medical_chat(question, context))
