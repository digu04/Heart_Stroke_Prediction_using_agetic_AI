from agents.reasoning_agent import generate_medical_reasoning

sample_prediction = 1
sample_risk = 82.7

sample_features = {
    "Age": 55,
    "Sex": "M",
    "ChestPainType": "TA",
    "RestingBP": 150,
    "Cholesterol": 250,
    "FastingBS": 1,
    "RestingECG": "ST",
    "MaxHR": 130,
    "ExerciseAngina": "Y",
    "Oldpeak": 2.5,
    "ST_Slope": "Flat"
}

out = generate_medical_reasoning(sample_prediction, sample_risk, sample_features)
print(out)
