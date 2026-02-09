from agents.lifestyle_agent import lifestyle_recommendations

sample_features = {
    "Age": 55,
    "Sex": "M",
    "RestingBP": 150,
    "Cholesterol": 250,
    "ExerciseAngina": "Y",
    "Oldpeak": 2.5
}

output = lifestyle_recommendations(sample_features, 82.7)
print(output)       # ← VERY IMPORTANT
